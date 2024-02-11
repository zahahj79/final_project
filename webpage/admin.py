from django.contrib import admin
from .models import Data


class WebAdmin(admin.ModelAdmin):
    list_display = ('location','date','time','temperature')
    ordering = ('location','-date','-time',)


admin.site.register(Data,WebAdmin)
