from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, ImageField, DateTimeField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for Volebni kalkulacka."""

    #: First and last name do not cover name patterns around the globe
    email = CharField("Email", max_length=255) 
    first_name = CharField("Firstname", blank=True, max_length=255)
    last_name = CharField("Surname", blank=True, max_length=255)
    profile_image = ImageField(null=True, blank=True)


    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
