from django.contrib import admin
from openinghours.models import (OpeningHours, ClosingRules, Company,
    OPENINGHOURS_PREMISES_MODEL)


admin.site.register(OpeningHours)
admin.site.register(ClosingRules)
if OPENINGHOURS_PREMISES_MODEL == 'openinghours.models.Company':
    admin.site.register(Company)
