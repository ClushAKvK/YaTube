from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from ExtUserFriedship.models import Friendship
# Register your models here.


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('creator', 'friend', 'created', 'accepted')
    search_fields = ('creator__username', 'friend__username')
    list_filter = (
        ('created', DateFieldListFilter),
        'accepted',
    )
