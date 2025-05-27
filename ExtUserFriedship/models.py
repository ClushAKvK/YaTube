from django.db import models
from django.utils.timezone import now

from ExtUser.models import ExtUser

# Create your models here.


class Friendship(models.Model):
    created = models.DateTimeField(
        'Date_of_created_friendship',
        default=now
    )
    creator = models.ForeignKey(
        ExtUser,
        related_name='Friendship_creator',
        on_delete=models.CASCADE
    )
    friend = models.ForeignKey(
        ExtUser,
        related_name='Friends_set',
        on_delete=models.CASCADE
    )
    accepted = models.BooleanField(
        default=False,
        blank=False,
        null=False
    )

    def __str__(self):
        return "Creator: {0}; Friend: {1}".format(str(self.creator), str(self.friend))
