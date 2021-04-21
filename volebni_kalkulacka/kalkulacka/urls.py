from django.urls import path
from volebni_kalkulacka.kalkulacka.views import *

app_name = "kalkulacka"
urlpatterns = [
    path("kalkulacka_index", kalkulacka_index, name="kalkulacka_index"),
    path("save_vote", kalkulackaSaveVote, name="save_vote"),
    path("get_actual_result_poslanci", kalkulackaGetActualResultsPoslanci, name="get_actual_results_poslanci"),
    path("get_actual_result_strany", kalkulackaGetActualResultsStrany, name="get_actual_results_strany"),
]