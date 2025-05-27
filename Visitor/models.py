import os

from django.db import models
from django.utils.timezone import now

from ExtUser.models import ExtUser

# Create your models here.

class Visitor(models.Model):
    visitor = models.ForeignKey(
        ExtUser,
        related_name='visitor',
        on_delete=models.CASCADE
    )

    visitDate = models.DateField(
        'Date of visit',
        auto_now_add=now
    )

    reqUser = models.ForeignKey(
        ExtUser,
        related_name='reqUser',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "{0} to {1}".format(self.visitor.username, self.reqUser.username)
