from django.contrib import admin
from openinghours.models import OpeningHours, ClosingRules, Company


admin.site.register(OpeningHours)
admin.site.register(ClosingRules)
admin.site.register(Company)
