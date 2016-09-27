from django.db import models
from ExtUser.models import ExtUser
from django.utils.timezone import now

# Create your models here.


class ExtUserMessage(models.Model):
    owner = models.ForeignKey(
        ExtUser,
        related_name='owner',
        default=0
    )
    recipient = models.ForeignKey(
        ExtUser,
        related_name='recipient',
        default=0
    )
    message = models.TextField(
        'Message',
        max_length=50000,
        blank=False,
        null=False
    )
    send_date = models.DateTimeField(
        'Send date',
        blank=False,
        null=False,
        default=now
    )
    delivered = models.BooleanField(
        'Delivered',
        blank=False,
        null=False,
        default=False
    )

    def __str__(self):
        return '\nMessage: "' + self.message + '"; Send date: ' \
               + str(self.send_date.date()) + ' ' + str(self.send_date.time())[0:8]


class ExtUserDialog(models.Model):
    friends = models.ManyToManyField(
        ExtUser,
        related_name='CorrespondenceSides',
        blank=False,
    )
    messages = models.ManyToManyField(
        ExtUserMessage,
        related_name='dialogs_messages',
        blank=True,
    )
    create_date = models.DateTimeField(
        'Create date',
        blank=False,
        null=False,
        default=now
    )

    def friends_get(self):
        friends = ''
        for friend in self.friends.all():
            friends += str(friend) + ' and '
        return friends[:-4]

    def __str__(self):
        return 'Dialog '+ str(self.id)
