from django.contrib import admin
from .models import *


# class YourModelAdmin(admin.ModelAdmin):
#    list_display = ['some', 'fields', ]
#    search_fields = ['some', 'fieds', ]


# admin.site.register(models.YourModel, YourModelAdmin)

admin.site.register(OpeningHours)
admin.site.register(ClosingRules)
admin.site.register(Company)
