from django.urls import path
from volebni_kalkulacka.hlasovani.views import *

app_name = "hlasovani"
urlpatterns = [
    path("hlasovani_index", Hlasovani_index.as_view(), name="hlasovani_index"),
    path('hlasovani_detail/<int:pk>', Hlasovani_detail.as_view(), name="hlasovani_detail")
]