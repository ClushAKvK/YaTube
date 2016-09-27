from django.db import models
from ExtUser.models import ExtUser
from django.utils.timezone import now

# Create your models here.


class Visitor(models.Model):
    visitor = models.ForeignKey(
        ExtUser,
        related_name='visitor'
    )

    visitDate = models.DateField(
        'Date of visit',
        auto_now_add=now
    )

    reqUser = models.ForeignKey(
        ExtUser,
        related_name='reqUser'
    )

    def __str__(self):
        return self.visitor.username + ' to ' + self.reqUser.username
