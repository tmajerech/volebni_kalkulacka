from django.urls import path

from volebni_kalkulacka.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    kalkulackaSaveVote,
    kalkulackaGetActualResultsPoslanci,
    kalkulackaGetActualResultsStrany,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("kalkulacka_save_vote", kalkulackaSaveVote, name="kalkulacka_save_vote"),
    path("kalkulacka_get_actual_result_poslanci", kalkulackaGetActualResultsPoslanci, name="kalkulacka_get_actual_results_poslanci"),
    path("kalkulacka_get_actual_result_strany", kalkulackaGetActualResultsStrany, name="kalkulacka_get_actual_results_strany"),
]
