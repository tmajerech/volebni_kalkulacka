from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, ImageField, DateTimeField, BooleanField, JSONField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from allauth.account.adapter import get_adapter
from allauth.account.signals import user_logged_in


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

    def get_hlasovani_ids(self):
        answered_ids = []
        KA = self.kalkulacka_answers
        for year, answers in KA.items():
            for answer_id, choice in answers.items():
                answered_ids.append(answer_id)

        return answered_ids


@receiver(user_logged_in, dispatch_uid="unique")
def user_logged_in_(request, user, **kwargs):
    """
    Sets timezone after user logs in
    """
    if user.kalkulacka_answers:
        request.session['kalkulacka_answers'] = user.kalkulacka_answers
    else:
        user.kalkulacka_answers = request.session.get('kalkulacka_answers')
        user.save()