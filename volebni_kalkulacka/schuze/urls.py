from django.urls import path
from volebni_kalkulacka.schuze.views import *

app_name = "schuze"
urlpatterns = [
    path("schuze_index", Schuze_index.as_view(), name="schuze_index"),
]