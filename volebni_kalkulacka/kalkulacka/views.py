from .forms import *
from django.views import generic

from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from volebni_kalkulacka.users.models import User

from django.db import connection

from volebni_kalkulacka.psp_data.models import Hl_Hlasovani, Organy
from volebni_kalkulacka.psp_data.helpers import get_current_election_period




def kalkulacka_index(request):

    template = 'pages/kalkulacka.html'
    args = {}

    #check if user has some valid vote
    if request.session.get('kalkulacka_answers'):
        for period, items in request.session['kalkulacka_answers'].items():
            if items != {}:
                args['has_votes'] = True

    return render(request, template, args)



def kalkulackaSaveVote(request):
    """
    Function to save kalkulacka votes 
    """
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    choice = request.POST.get('choice')
    id_hlasovani = request.POST.get('id_hlasovani')
    period_id = str(Hl_Hlasovani.objects.get(pk=id_hlasovani).id_organ.pk)
    
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        kalkulacka_answers = user.kalkulacka_answers if user.kalkulacka_answers != None else {period_id: {}}
    else:
        kalkulacka_answers = request.session.get('kalkulacka_answers', {})

    if choice == '':
        if period_id in kalkulacka_answers:
            if id_hlasovani in kalkulacka_answers.get(period_id):
                del kalkulacka_answers[period_id][id_hlasovani]
    else:
        if period_id not in kalkulacka_answers:
            kalkulacka_answers[period_id] = {}

        kalkulacka_answers[period_id][id_hlasovani] = choice

    request.session['kalkulacka_answers'] = kalkulacka_answers
    if request.user.is_authenticated:
        user.kalkulacka_answers = kalkulacka_answers
        user.save()

    return HttpResponse('ok')


def kalkulackaGetActualResultsPoslanci(request):
    """
    Function returning html with actual kalkulacka results for poslanecs
    """
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    current_elechtion_period = get_current_election_period()

    data = {}

    # loop through all periods
    for period_id in request.session['kalkulacka_answers']:
        period_year = Organy.objects.get(pk=period_id).od_organ.split('.')[-1]
        if len(request.session['kalkulacka_answers'][period_id]) == 0:
            continue
        data[period_year] = {}

        period_answers = tuple([(k, v) for k, v in request.session['kalkulacka_answers'][period_id].items()])
        answers_count = len(period_answers)

        sql = f"""
            DROP TABLE IF EXISTS t1;
            CREATE TEMP TABLE t1 AS   
                SELECT count(*) AS matches, id_poslanec 
                FROM psp_data_hl_poslanec
                WHERE (id_hlasovani, REPLACE(REPLACE(vysledek, 'B', 'N'),'C', 'K')) 
                    IN %s
                GROUP BY id_poslanec 
                ORDER BY matches DESC;
            
            DROP TABLE IF EXISTS t2;
            CREATE TEMP TABLE t2 AS 
                SELECT DISTINCT ON (p.id_poslanec) 
                    (cast(t1.matches as decimal(7,2))/%s)*100 AS match_ratio, 
                    t1.id_poslanec, o.zkratka, 
                    os.pred, os.jmeno, os.prijmeni, os.za
                FROM t1
                    INNER JOIN psp_data_poslanec AS p
                    ON p.id_poslanec = t1.id_poslanec

                    INNER JOIN psp_data_osoby AS os
                    ON p.id_osoba = os.id_osoba

                    INNER JOIN psp_data_zarazeni AS z 
                    ON p.id_osoba = z.id_osoba

                    INNER JOIN psp_data_organy as o
                    ON z.id_of = o.id_organ
                WHERE z.cl_funkce = 0
                    AND o.organ_id_organ = {period_id}
                    AND o.id_typ_organu = 1
                ORDER BY 
                    p.id_poslanec, TO_DATE(z.od_o, 'YYYY-MM-DD') ASC
            ;

            SELECT * 
            FROM t2
            ORDER BY match_ratio DESC, prijmeni
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [period_answers, answers_count])
            columns = [x.name for x in cursor.description]

            result = []
            for row in cursor.fetchall():
                row = dict(zip(columns, row))
                result.append(row)

            data[period_year] = result

    context = {}
    context['matching_result'] = data

    return render(request, 'users/kalkulacka_results_poslanci.html', context)


def kalkulackaGetActualResultsStrany(request):
    """
    Function returning html with actual kalkulacka results for parties
    """

    current_election_period = get_current_election_period()
    data = {}

    # loop through all periods
    for period_id in request.session['kalkulacka_answers']:
        period_year = Organy.objects.get(pk=period_id).od_organ.split('.')[-1]
        if len(request.session['kalkulacka_answers'][period_id]) == 0:
            continue
        data[period_year] = {}

        period_answers = tuple([(k, v) for k, v in request.session['kalkulacka_answers'][period_id].items()])
        answers_count = len(period_answers)

        sql = f"""
        --get last last party for each member
        DROP TABLE IF EXISTS osoby_zarazeni;
        CREATE TEMP TABLE osoby_zarazeni AS
            SELECT DISTINCT ON (os.id_osoba) 
                os.id_osoba, o.zkratka, z.od_o, z.do_o, o.od_organ
            FROM 
                psp_data_osoby AS os
                INNER JOIN psp_data_zarazeni AS z 
                ON os.id_osoba = z.id_osoba

                INNER JOIN psp_data_organy AS o
                ON z.id_of = o.id_organ
            WHERE 
                z.cl_funkce = 0
                and o.organ_id_organ = {period_id}
                and o.id_typ_organu = 1
            ORDER BY
                os.id_osoba, TO_DATE(z.od_o, 'YYYY-MM-DD') ASC;

        --get members count in party
        DROP TABLE IF EXISTS tP1;
        CREATE TEMP TABLE tP1 AS
            SELECT 
                COUNT(*) AS members_count, oz.zkratka 
            FROM 
                osoby_zarazeni as oz
			WHERE
				TO_DATE(oz.od_o, 'YYYY-MM-DD') = TO_DATE(oz.od_organ,'DD.MM.YYYY')
            GROUP BY 
                oz.zkratka;

        DROP TABLE IF EXISTS tP2;
        CREATE TEMP TABLE tP2 AS
            SELECT 
                count(*) AS party_total_matches, oz.zkratka FROM psp_data_hl_poslanec as hlp
                INNER JOIN psp_data_poslanec AS p
                ON p.id_poslanec = hlp.id_poslanec

                INNER JOIN osoby_zarazeni AS oz
                ON p.id_osoba = oz.id_osoba

            --need to replace characters because they use multiple with same meaning
            WHERE 
                (id_hlasovani, REPLACE(REPLACE(vysledek, 'B', 'N'),'C', 'K'))IN %s
            GROUP 
                BY oz.zkratka;

        SELECT 
            ((CAST(tP2.party_total_matches as decimal(7,2))/{answers_count})
            /tP1.members_count)*100 AS match_ratio, tP1.zkratka 
        FROM tP2
            INNER JOIN tP1
            ON tP1.zkratka = tP2.zkratka
        ORDER 
            BY match_ratio DESC, tP1.zkratka
            
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [period_answers])
            columns = [x.name for x in cursor.description]

            result = []
            for row in cursor.fetchall():
                row = dict(zip(columns, row))
                result.append(row)

            data[period_year] = result

    context = {}
    context['matching_result'] = data

    return render(request, 'users/kalkulacka_results_strany.html', context)
