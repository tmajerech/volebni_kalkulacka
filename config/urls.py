from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("volebni_kalkulacka.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    
    #3rd party
    path('comments/', include('django_comments.urls')),

    # Your stuff: custom urls includes go here
    path("schuze/", include("volebni_kalkulacka.schuze.urls", namespace="schuze")),
    path("poslanec/", include("volebni_kalkulacka.poslanec.urls", namespace="poslanec")),
    path("hlasovani/", include("volebni_kalkulacka.hlasovani.urls", namespace="hlasovani")),
    path("psp_data/", include("volebni_kalkulacka.psp_data.urls", namespace="psp_data")),
    path("kalkulacka/", include("volebni_kalkulacka.kalkulacka.urls", namespace="kalkulacka"))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
