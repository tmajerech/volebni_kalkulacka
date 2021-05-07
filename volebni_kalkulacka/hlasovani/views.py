from .forms import *

from django import template
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.postgres.search import SearchVector
from django.db import connection

from volebni_kalkulacka.psp_data.helpers import get_current_election_period
from volebni_kalkulacka.psp_data.models import Hl_Hlasovani, Hist, Tisky, Poslanec, Hl_Hlasovani_Rating, Bod_Schuze, Schuze


from datetime import datetime

register = template.Library()

class Hlasovani_index(generic.ListView):
    model = Hl_Hlasovani
    template_name = 'pages/hlasovani_index.html'
    context_object_name = 'hlasovani'
    paginate_by = 40

    def get_context_data(self):
        context = super(Hlasovani_index, self).get_context_data()
        
        answered_ids = []
        
        KA = self.request.session.get('kalkulacka_answers')
        if KA:
            for year, answers in KA.items():
                for answer_id, choice in answers.items():
                    #print(answer_id)
                    answered_ids.append(answer_id)

            context['answered_ids']= answered_ids             
        return context

    def get_queryset(self):
        inner_qs = Hl_Hlasovani_Rating.objects.all().values_list('id_hlasovani', flat=True)

        #get ordering and filters from request
        orderingPar = self.request.GET.get('sort')
        filterName = self.request.GET.get('filterName')
        
        queryset = Hl_Hlasovani.objects.filter(id_hlasovani__in=inner_qs)
        if filterName:
            queryset = queryset.annotate(search=SearchVector('nazev_dlouhy')).filter(search__icontains=filterName)

        if self.request.GET.get('filterDate'):
            filterDate = self.request.GET.get('filterDate')
            queryset = queryset.filter(datum=filterDate)

        if orderingPar == 'rating_asc':
            ordering = 'hl_hlasovani_rating__rating'
            queryset = queryset.order_by(ordering)
        elif orderingPar == 'rating_desc':
            ordering = '-hl_hlasovani_rating__rating'
            queryset = queryset.order_by(ordering)
        elif orderingPar == 'date_asc':
            queryset = queryset.extra(select={'datum_ex':"TO_DATE(datum,'DD.MM.YYYY')"}, order_by=['datum_ex'] )
        elif orderingPar == 'date_desc':
            queryset = queryset.extra(select={'datum_ex':"TO_DATE(datum,'DD.MM.YYYY')"}, order_by=['-datum_ex'] )
        else:
            ordering = '-hl_hlasovani_rating__rating'
            queryset = queryset.order_by(ordering)

        return queryset

class Hlasovani_detail(generic.DetailView):
    template_name = 'pages/hlasovani_detail.html'
    model = Hl_Hlasovani
    context_object_name = 'hlasovani_single'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hlasovani_single = kwargs.get('object')
        id_org = hlasovani_single.id_organ.pk
        id_hlasovani = hlasovani_single.id_hlasovani

        sql = f"""
        SELECT DISTINCT ON (p.id_poslanec) o.zkratka, hp.id_poslanec, hp.vysledek,  os.jmeno, os.prijmeni 
        FROM psp_data_hl_poslanec AS hp 
            INNER JOIN psp_data_poslanec AS p 
            ON hp.id_poslanec = p.id_poslanec 
            
            INNER JOIN psp_data_zarazeni AS z
            ON p.id_osoba = z.id_osoba
            
            INNER JOIN psp_data_organy as o
            ON z.id_of = o.id_organ
            
            INNER JOIN psp_data_osoby as os
            ON os.id_osoba = p.id_osoba
            
        WHERE 
            hp.id_hlasovani = {id_hlasovani}
            AND z.cl_funkce = 0 --clenstvi
            AND o.id_typ_organu = 1 --Klub
            AND o.organ_id_organ = {id_org} --id volebniho obdobi

        ORDER BY 
            p.id_poslanec, TO_DATE(z.od_o, 'YYYY-MM-DD') ASC, o.zkratka, os.prijmeni
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = [x.name for x in cursor.description]

            strany = {}
            for row in cursor.fetchall():
                row = dict(zip(columns, row))
                strana = row['zkratka']
                if strana in strany:
                    strany[strana].append(row)
                else:
                    strany[strana] = [row]

        try:
          context['tisk'] = Tisky.objects.get(pk=hlasovani_single.hist.id_tisk)
        except Exception as e:
          pass

        try:
            kalkulacka_answers = self.request.session.get('kalkulacka_answers')
            context['vote'] = kalkulacka_answers.get(str(hlasovani_single.id_organ.pk)).get(str(hlasovani_single.pk))
        except:
            pass

        #get full name of Bod Hlasovani
        id_schuze = Schuze.objects.filter(schuze=hlasovani_single.schuze, id_org=hlasovani_single.id_organ, pozvanka=None).values_list('id_schuze', flat=True)[0]
        nazev_uplny = Bod_Schuze.objects.filter(id_schuze=id_schuze, bod=hlasovani_single.bod, pozvanka=None).first().uplny_naz
        context['nazev_uplny'] = nazev_uplny
        
        context['strany'] = strany

        return context

