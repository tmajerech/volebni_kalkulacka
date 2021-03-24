from .forms import *
from django.views import generic

from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from volebni_kalkulacka.psp_data.helpers import get_current_election_period
from volebni_kalkulacka.psp_data.models import Poslanec, Organy

from django.db import connection

class Poslanec_index(generic.ListView):
    model = Poslanec
    template_name = 'pages/poslanec_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        id_org = get_current_election_period()

        sql = """
        SELECT p.id_poslanec, o.zkratka, p.foto, p.id_osoba, os.pred, os.za, os.jmeno, os.prijmeni
        FROM 
            psp_data_poslanec AS p 
            INNER JOIN psp_data_osoby as os
	        ON p.id_osoba = os.id_osoba

            INNER JOIN psp_data_zarazeni AS z 
            ON p.id_osoba = z.id_osoba

            INNER JOIN psp_data_organy as o
            ON z.id_of = o.id_organ

        WHERE 
            p.id_obdobi = %s
            and z.cl_funkce = 0
            and z.do_o IS NULL
            and o.organ_id_organ = %s
            and o.id_typ_organu = 1
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [id_org, id_org])
            columns = [x.name for x in cursor.description]

            poslanec = []
            for row in cursor.fetchall():
                row = dict(zip(columns, row))
                poslanec.append(row)

        context['poslanec'] = poslanec

        return context

class Poslanec_detail(generic.DetailView):
    template_name = 'pages/poslanec_detail.html'
    model = Poslanec
    context_object_name = 'poslanec_single'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        id_org = get_current_election_period()

        poslanec_single = kwargs.get('object')

        member_of = Organy.objects.filter(zarazeni__id_osoba=poslanec_single.id_osoba, zarazeni__do_o=None).values_list('nazev_organu_cz', flat=True)
        party = Organy.objects.filter(
            zarazeni__id_osoba=poslanec_single.id_osoba, 
            zarazeni__do_o=None,
            organ_id_organ=id_org,
            id_typ_organu = 1, #1 stands for political party //Typ orgánu, viz typ_organu:id_typ_organu
            ).values_list('zkratka', flat=True).first()
        
        context['member_of'] = member_of
        context['party'] = party
        return context