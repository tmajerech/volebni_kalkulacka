from .forms import *
from django.views import generic

from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.db import connection
from django.db.models import Avg
from django.contrib.auth.decorators import login_required

from volebni_kalkulacka.psp_data.helpers import get_current_election_period
from volebni_kalkulacka.psp_data.models import Poslanec, Organy
from volebni_kalkulacka.poslanec.models import Ratings



class Poslanec_index(generic.ListView):
    model = Poslanec
    template_name = 'pages/poslanec_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        id_org = get_current_election_period()

        sql = """

        CREATE TEMPORARY TABLE t1 AS
            SELECT AVG(rating) AS rating, id_poslanec
            FROM poslanec_ratings
			GROUP BY id_poslanec
        ;

        SELECT p.id_poslanec, o.zkratka, p.foto, p.id_osoba, os.pred, os.za, os.jmeno, os.prijmeni, t1.rating
        FROM 
            psp_data_poslanec AS p 
            INNER JOIN psp_data_osoby as os
	        ON p.id_osoba = os.id_osoba

            INNER JOIN psp_data_zarazeni AS z 
            ON p.id_osoba = z.id_osoba

            INNER JOIN psp_data_organy as o
            ON z.id_of = o.id_organ

            LEFT JOIN t1
            ON t1.id_poslanec = p.id_poslanec

        WHERE 
            p.id_obdobi = %s
            and z.cl_funkce = 0
            and z.do_o IS NULL
            and o.organ_id_organ = %s
            and o.id_typ_organu = 1

        ORDER BY 
            o.zkratka, os.prijmeni
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
        member_of = Organy.objects.filter(zarazeni__id_osoba=poslanec_single.id_osoba,
                                          zarazeni__do_o=None).values_list('nazev_organu_cz', flat=True)
        party = Organy.objects.filter(
            zarazeni__id_osoba=poslanec_single.id_osoba,
            zarazeni__do_o=None,
            organ_id_organ=id_org,
            id_typ_organu=1,  # 1 stands for political party //Typ orgánu, viz typ_organu:id_typ_organu
        ).values_list('zkratka', flat=True).first()
        ratings = Ratings.objects.filter(id_poslanec=poslanec_single.id_poslanec)
        rating = ratings.aggregate(Avg('rating'))
        
        if self.request.user.is_authenticated:
          user_rated = Ratings.objects.filter(id_poslanec=poslanec_single.id_poslanec, id_user=self.request.user)   
          if user_rated:
            context['user_rated'] = user_rated.first().rating
        
        context['rating'] = rating['rating__avg']
        context['member_of'] = member_of
        context['party'] = party
        return context


@login_required
def saveStarRating(request):
  # if not request.is_ajax() or not request.method == 'POST':
  #   return HttpResponseNotAllowed(['POST'])
  user = request.user 
  new_rating = request.POST.get('new_rating')
  poslanec_id = request.POST.get('id_poslanec')
  poslanec = Poslanec.objects.get(pk=poslanec_id)
  rating = Ratings.objects.filter(id_user=user, id_poslanec=poslanec_id).first()

  if(rating is None):
    rating = Ratings(id_user=user, id_poslanec=poslanec_id)
  rating.rating = new_rating 
  rating.save()

  ratings = Ratings.objects.filter(id_poslanec=poslanec_id)
  avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']

  data = {
    'user_rated':new_rating,
    'avg_rating':avg_rating
  }

  return JsonResponse(data)


@login_required
def removeStarRating(request):
  # if not request.is_ajax() or not request.method == 'POST':
  #   return HttpResponseNotAllowed(['POST'])
  user = request.user 
  poslanec_id = request.POST.get('id_poslanec')
  poslanec = Poslanec.objects.get(pk=poslanec_id)
  rating = Ratings.objects.filter(id_user=user, id_poslanec=poslanec_id).first()
  rating.delete()

  ratings = Ratings.objects.filter(id_poslanec=poslanec_id)
  avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']

  data = {
    'avg_rating':avg_rating
  }

  return JsonResponse(data)