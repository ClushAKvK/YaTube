from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.utils.timezone import now
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **fields):
        if not username:
            raise ValueError('Username is required.')
        if not email:
            raise ValueError('Email is required.')

        user = self.model(
            username=username,
            email=UserManager.normalize_email(email),
            **fields
        )
        user.set_password(password)
        user.save(using=self._db)

        ExtUserProfile.objects.create(
            user=user
        ).save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None, **fields):
        fields.setdefault('is_admin', True)
        fields.setdefault('is_staff', True)
        fields.setdefault('is_superuser', True)

        return self.create_user(username=username, email=email, password=password, **fields)


class ExtUser(AbstractUser):
    username = models.CharField(
        'Username',
        max_length=50,
        unique=True,
        null=False,
        blank=False
    )

    email = models.EmailField(
        'Email',
        max_length=255,
        unique=True,
        null=False,
        blank=False
    )

    location = models.CharField(
        'Location',
        max_length=255,
        unique=False,
        null=True,
        blank=True
    )

    gender = models.CharField(
        max_length=5,
        null=False,
        blank=False,
        choices=(
            ('M', 'Man'),
            ('W', 'Woman')
        )
    )

    orientation = models.CharField(
        max_length=8,
        null=False,
        blank=False,
        choices=(
            ('S', 'Straight'),
            ('G', 'Gay'),
        )
    )

    birthday = models.DateField(
        'Birthday',
        null=True,
        blank=True,
        default=now
    )

    is_active = models.BooleanField(
        'Active',
        default=True
    )

    is_admin = models.BooleanField(
        'Admin',
        default=False
    )

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def create_message(self, message, recipient):
        from ExtUserCorrespondence.models import ExtUserMessage, ExtUserDialog
        new_message = ExtUserMessage.objects.create(
            owner=self,
            recipient=recipient,
            message=message
        )
        new_message.save()

        dialog = ExtUserDialog.objects.filter(friends=self).filter(friends=recipient)

        if len(dialog) > 0:
            dialog[0].messages.add(new_message)
            del dialog
        else:
            dialog = ExtUserDialog.objects.create()
            dialog.friends.add(self, recipient)
            dialog.messages.add(new_message)

        return new_message

    def create_friendship(self, friend):
        from ExtUserFriedship.models import Friendship
        try:
            friendship = Friendship.objects.get(creator=friend, friend=self)
            friendship.accepted = True
            friendship.save()

            return friendship
        except Exception as e:
            print(e)
            new_friendship = Friendship.objects.create(
                creator=self,
                friend=friend
            )

        return new_friendship

    def get_friends(self):
        from ExtUserFriedship.models import Friendship

        return Friendship.objects.filter(creator=self, accepted=True), \
            Friendship.objects.filter(friend=self, accepted=True)

    def get_sent_requests_for_friendship(self):
        from ExtUserFriedship.models import Friendship

        return Friendship.objects.filter(creator=self, accepted=False), \
            Friendship.objects.filter(friend=self, accepted=True)

    def get_requests_for_friendships(self):
        from ExtUserFriedship.models import Friendship

        return Friendship.objects.filter(friend=self, accepted=False)

    def get_dialog(self, friend):
        from ExtUserCorrespondence.models import ExtUserDialog
        return ExtUserDialog.objects.filter(friend1=self, friend2=friend)

    def get_messages(self, recipient=None):
        from ExtUserCorrespondence.models import ExtUserMessage
        if recipient is not None:
            return ExtUserMessage.objects.filter(owner=self, recipient=recipient)
        return ExtUserMessage.objects.all()

    def delete_friendship(self, friend):
        from ExtUserFriedship.models import Friendship
        like = Friendship.objects.filter(creator=self, friend=friend)
        if len(like) == 0:
            like = Friendship.objects.filter(creator=friend, friend=self)

        if like[0].accepted is True:
            like[0].delete()
            Friendship.objects.create(creator=friend, friend=self)
        else:
            like[0].delete()
        return True

    def accept_friendship(self, friend):
        from ExtUserFriedship.models import Friendship
        new_friendship = Friendship.objects.get(creator=friend, friend=self, accepted=False)
        new_friendship.accepted = True
        new_friendship.save()

    def get_like_on_user(self, requestUser):
        from ExtUserFriedship.models import Friendship
        like = Friendship.objects.filter(creator=self, friend=requestUser)
        if len(like) == 0:
            like = Friendship.objects.filter(creator=requestUser, friend=self, accepted=True)

        result = lambda like: True if len(like) > 0 else False

        return result(like)

    def refresh_token(self):
        Token.objects.get(user=self).delete()
        token = Token.objects.create(user=self)

        return token

    def get_my_visitors(self):
        from Visitor.models import Visitor

        return Visitor.objects.filter(reqUser=self)

    def get_own_visitors(self):
        from Visitor.models import Visitor

        return Visitor.objects.filter(visitor=self)

    def create_visit(self, reqUser):
        from Visitor.models import Visitor

        if len(Visitor.objects.filter(visitor=self, reqUser=reqUser)) == 0:
            Visitor.objects.create(visitor=self, reqUser=reqUser)
        else:
            visit = Visitor.objects.get(visitor=self, reqUser=reqUser)
            visit.visitDate = now()
            visit.save()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'location', 'gender', 'orientation']
    objects = UserManager()

    class Meta:
        verbose_name = 'ExtUser'
        verbose_name_plural = 'ExtUsers'
        db_table = 'ExtUser'


class ExtUserProfile(models.Model):
    user = models.OneToOneField(
        ExtUser,
        unique=True,
        related_name='profile'
    )

    photo = models.ImageField(
        'Avatar',
        upload_to='avatars/',
        default='avatars/ic_profile_default.png'
    )

    language = models.CharField(
        'Language',
        max_length=255,
        null=True,
        blank=True
    )

    base = models.TextField(
        'BaseInformation',
        max_length=9999,
        null=True,
        blank=True
    )

    summary = models.TextField(
        'SummaryInformation',
        max_length=9999,
        null=True,
        blank=True
    )

    life = models.TextField(
        'InformationOfLife',
        max_length=9999,
        null=True,
        blank=True
    )

    good = models.TextField(
        'InformationOfGoodSkills',
        max_length=9999,
        null=True,
        blank=True
    )

    favorite = models.TextField(
        'Favorites',
        max_length=9999,
        blank=True,
        null=True
    )

    badge = models.TextField(
        'Badge',
        max_length=9999,
        blank=True,
        null=True
    )

    def __str__(self):
        return '%s\'s Profile' % self.user.username
