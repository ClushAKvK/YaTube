from django.db import models
from ExtUser.models import ExtUser
from django.utils.timezone import now

# Create your models here.


class Friendship(models.Model):
    created = models.DateTimeField(
        'Date_of_created_friendship',
        default=now
    )
    creator = models.ForeignKey(
        ExtUser,
        related_name='Friendship_creator'
    )
    friend = models.ForeignKey(
        ExtUser,
        related_name='Friends_set'
    )
    accepted = models.BooleanField(
        default=False,
        blank=False,
        null=False
    )

    def __str__(self):
        return "Creator: " + str(self.creator) + "; Friend: " + str(self.friend)
