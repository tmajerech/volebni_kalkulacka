
from django.views import generic
from django.http import HttpResponse

from dataImport.dataImport import runImport


def run_import(request):
    print('start')
    runImport()
    print('end')
    return HttpResponse('ok')