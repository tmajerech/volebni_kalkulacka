
from django.views import generic
from django.http import HttpResponse

from dataImport.dataImport import runImport, runInitialImport


def run_import(request):
    print('start')
    runImport()
    print('end')
    return HttpResponse('ok')

def run_initial_import(request):
    print('start')
    runInitialImport()
    print('end')
    return HttpResponse('ok')