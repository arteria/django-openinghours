from django.contrib import admin
from openinghours.models import OpeningHours, ClosingRules, Company, PREMISES_MODEL

class OpeningHoursAdmin(admin.ModelAdmin):
    raw_id_fields = ('company',)

admin.site.register(OpeningHours, OpeningHoursAdmin)
admin.site.register(ClosingRules)
if PREMISES_MODEL == 'openinghours.Company':
    admin.site.register(Company)
