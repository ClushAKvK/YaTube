from django.contrib import admin
from ExtUserCorrespondence.models import *
from django.contrib.admin import DateFieldListFilter

# Register your models here.


@admin.register(ExtUserMessage)
class ExtUserMessageAdmin(admin.ModelAdmin):
    list_display = ('owner', 'recipient', 'send_date', 'message', 'delivered')
    search_fields = ('owner__username', 'recipient__username')
    readonly_fields = ('owner', 'recipient', 'send_date', 'message', 'delivered')
    list_filter = (
        ('send_date', DateFieldListFilter),
        'delivered'
    )


@admin.register(ExtUserDialog)
class ExtUserDialogAdmin(admin.ModelAdmin):
    list_display = ('friends_get', 'create_date')
    search_fields = ('create_date', 'friends__username')
    list_filter = (
        ('create_date', DateFieldListFilter),
    )
    readonly_fields = ('friends', 'create_date', 'messages',)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'messages':
            kwargs['queryset'] = ExtUserMessage.objects.all()
        return super(ExtUserDialogAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
