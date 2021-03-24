from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, ImageField, DateTimeField, BooleanField
from django.contrib.postgres.fields import JSONField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for Volebni kalkulacka."""

    #: First and last name do not cover name patterns around the globe
    email = CharField("Email", max_length=255) 
    first_name = CharField("Firstname", blank=True, max_length=255)
    last_name = CharField("Surname", blank=True, max_length=255)
    profile_image = ImageField(null=True, blank=True)

    show_results_publicly = BooleanField(default=False)
    kalkulacka_answers = JSONField(null=True, blank=True)
    kalkulacka_results = JSONField(null=True, blank=True)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
