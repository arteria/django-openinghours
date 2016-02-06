from django.contrib import admin
from openinghours.models import OpeningHours, ClosingRules, Company, PREMISES_MODEL


admin.site.register(OpeningHours)
admin.site.register(ClosingRules)
if PREMISES_MODEL == 'openinghours.Company':
    admin.site.register(Company)
