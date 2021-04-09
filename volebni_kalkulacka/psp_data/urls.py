from django.urls import path
from volebni_kalkulacka.psp_data.views import *

app_name = "psp_data"
urlpatterns = [
    path("run_import", run_import, name="run_import"),
    path("run_initial_import", run_initial_import, name="run_initial_import"),
]