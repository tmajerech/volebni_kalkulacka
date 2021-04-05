from django.db import models
from volebni_kalkulacka.users.models import User

from django.core.validators import MaxValueValidator, MinValueValidator

class Ratings(models.Model):
  id_user = models.ForeignKey(User, db_column='id_user', on_delete=models.DO_NOTHING)
  id_poslanec = models.IntegerField()
  rating = models.DecimalField(max_digits=5, decimal_places=2, db_column='rating')

