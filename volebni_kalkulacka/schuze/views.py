from .forms import *
from django.views import generic

from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponseRedirect

from volebni_kalkulacka.psp_data.helpers import get_current_election_period
from volebni_kalkulacka.psp_data.models import Schuze, Bod_Schuze, Organy, Hl_Hlasovani


class Schuze_index(generic.ListView):
    model = Schuze
    template_name = 'pages/schuze_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        id_org = get_current_election_period()

        schuze_numbers = Schuze.objects.filter(pozvanka=1, id_org=id_org).order_by(
            'schuze').values_list('schuze', flat=True)
        schuze = {}

        #this is inefficient
        for schuze_number in schuze_numbers:
            hlasovani_data = Hl_Hlasovani.objects.filter(
                schuze=schuze_number, nazev_dlouhy__isnull=False, bod__gt=0).exclude(nazev_dlouhy__exact=' ').order_by('bod')
            hlasovani = {}

            for hlasovani_single in hlasovani_data:
                hlasovani[hlasovani_single.nazev_dlouhy] = {}

            for hlasovani_single in hlasovani_data:
                hlasovani[hlasovani_single.nazev_dlouhy][hlasovani_single.cislo] = {
                    'vysledek': hlasovani_single.vysledek,
                    'id_hlasovani': hlasovani_single.id_hlasovani
                }

            schuze[schuze_number] = hlasovani

        context['schuze'] = schuze

        return context
