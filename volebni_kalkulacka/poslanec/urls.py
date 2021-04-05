from django.urls import path
from volebni_kalkulacka.poslanec.views import *

app_name = "poslanec"
urlpatterns = [
    path("poslanec_index", Poslanec_index.as_view(), name="poslanec_index"),
    path('poslanec_detail/<int:pk>', Poslanec_detail.as_view(), name="poslanec_detail"),

    path('save_star_rating', saveStarRating, name="save_star_rating"),
    path('remove_star_rating', removeStarRating, name="remove_star_rating"),
]