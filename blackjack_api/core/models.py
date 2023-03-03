from django.db import models


class Blackjack(models.Model):
    value = models.IntegerField(default=0)
