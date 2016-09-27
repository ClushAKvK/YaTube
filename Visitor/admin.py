from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from Visitor.models import Visitor

# Register your models here.


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('visitor', 'reqUser', 'visitDate')
    search_fields = ('visitor__username', 'reqUser__username')
    list_filter = (
        ('visitDate', DateFieldListFilter),
    )
