from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.http import HttpResponse
from django.shortcuts import render

from django.db import connection

from users.forms import UserEditForm
from volebni_kalkulacka.psp_data.helpers import get_current_election_period

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserEditForm
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return self.request.user



user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()

@login_required
def kalkulackaSaveVote(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    choice = request.POST.get('choice')
    id_hlasovani = request.POST.get('id_hlasovani')
    user = User.objects.get(username=request.user.username)
    kalkulacka_answers = user.kalkulacka_answers if user.kalkulacka_answers != None else {}

    if choice == '':
        if id_hlasovani in kalkulacka_answers:
            del kalkulacka_answers[id_hlasovani]
    else:
        kalkulacka_answers[id_hlasovani] = choice

    user.kalkulacka_answers = kalkulacka_answers
    user.save()

    return HttpResponse('ok')

@login_required
def kalkulackaGetActualResultsPoslanci(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    current_elechtion_period = get_current_election_period()

    user = User.objects.get(username=request.user.username)
    kalkulacka_answers = tuple([(k, v) for k, v in user.kalkulacka_answers.items()]) 
    answers_count = len(kalkulacka_answers)
    data = {}

    sql = """

        CREATE TEMP TABLE t1 AS   
            SELECT count(*) AS match_ratio, id_poslanec 
            FROM psp_data_hl_poslanec
            WHERE (id_hlasovani, vysledek) IN %s
            GROUP BY id_poslanec 
            ORDER BY match_ratio DESC;
        

        SELECT (cast(t1.match_ratio as decimal(7,2))/%s)*100 AS match_ratio, t1.id_poslanec, o.zkratka, 
            os.pred, os.jmeno, os.prijmeni, os.za
        FROM t1
            INNER JOIN psp_data_poslanec AS p
            ON p.id_poslanec = t1.id_poslanec

            INNER JOIN psp_data_osoby AS os
            ON p.id_poslanec = os.id_osoba

            INNER JOIN psp_data_zarazeni AS z 
            ON p.id_osoba = z.id_osoba

            INNER JOIN psp_data_organy as o
            ON z.id_of = o.id_organ

        WHERE z.cl_funkce = 0
            and o.organ_id_organ = %s
            and o.id_typ_organu = 1
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, [kalkulacka_answers, answers_count, current_elechtion_period])
        columns = [x.name for x in cursor.description]

        result = []
        for row in cursor.fetchall():
            row = dict(zip(columns, row))
            result.append(row)
        
        data['matching_result'] = result

    return render(request, 'users/kalkulacka_results_poslanci.html', data)




@login_required
def kalkulackaGetActualResultsStrany(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    current_elechtion_period = get_current_election_period()

    user = User.objects.get(username=request.user.username)
    kalkulacka_answers = tuple([(k, v) for k, v in user.kalkulacka_answers.items()]) 
    answers_count = len(kalkulacka_answers)
    data = {}

    sql = """

    CREATE TEMP TABLE t1 AS --pocet poslancu ve stranach
        SELECT COUNT(*) AS members_count, o.zkratka FROM psp_data_osoby AS os
            INNER JOIN psp_data_zarazeni AS z 
            ON os.id_osoba = z.id_osoba

            INNER JOIN psp_data_organy AS o
            ON z.id_of = o.id_organ
        

        WHERE z.cl_funkce = 0
            and o.organ_id_organ = 172
            and o.id_typ_organu = 1
            and z.do_o is NULL
        
        GROUP BY o.zkratka;

    CREATE TEMP TABLE t2 AS
        SELECT count(*) AS party_total_matches, o.zkratka FROM psp_data_hl_poslanec as hlp
            INNER JOIN psp_data_poslanec AS p
            ON p.id_poslanec = hlp.id_poslanec

            INNER JOIN psp_data_osoby AS os
            ON p.id_poslanec = os.id_osoba

            INNER JOIN psp_data_zarazeni AS z 
            ON p.id_osoba = z.id_osoba

            INNER JOIN psp_data_organy as o
            ON z.id_of = o.id_organ

        WHERE (id_hlasovani, vysledek) IN ((67020,'A'),(67022, 'K'))
            and z.cl_funkce = 0
            and o.organ_id_organ = 172
            and o.id_typ_organu = 1
        GROUP BY o.zkratka;

    SELECT ((CAST(t2.party_total_matches as decimal(7,2))/2)/t1.members_count)*100 AS match_ratio, t1.zkratka 
    FROM t2
    INNER JOIN t1
    ON t1.zkratka = t2.zkratka
    ORDER BY match_ratio DESC
        
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, [kalkulacka_answers, answers_count, current_elechtion_period])
        columns = [x.name for x in cursor.description]

        result = []
        for row in cursor.fetchall():
            row = dict(zip(columns, row))
            result.append(row)
        
        data['matching_result'] = result

    return render(request, 'users/kalkulacka_results_strany.html', data)