from .forms import *
from django.views import generic

from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from volebni_kalkulacka.psp_data.helpers import get_current_election_period
from volebni_kalkulacka.psp_data.models import Hl_Hlasovani, Hist, Tisky, Poslanec, Hl_Hlasovani_Rating

from django.db import connection

from django import template

register = template.Library()

class Hlasovani_index(generic.ListView):
    model = Hl_Hlasovani
    template_name = 'pages/hlasovani_index.html'
    context_object_name = 'hlasovani'
    paginate_by = 40

    def get_queryset(self):
        inner_qs = Hl_Hlasovani_Rating.objects.all().values_list('id_hlasovani', flat=True)
        queryset = Hl_Hlasovani.objects.filter(id_hlasovani__in=inner_qs).order_by('-hl_hlasovani_rating__rating')
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
        SELECT o.zkratka, hp.id_poslanec, hp.vysledek,  os.jmeno, os.prijmeni 
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
            AND (
                TO_DATE(z.do_o, 'YYYY-MM-DD') = TO_DATE(o.do_organ,'DD.MM.YYYY')
                OR 
                z.do_o IS null
                )

        ORDER BY 
            o.zkratka, os.prijmeni
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

        context['strany'] = strany

        return context

