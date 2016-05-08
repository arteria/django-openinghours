from django.contrib import admin
from .models import *
from transmeta import canonical_fieldname


# class YourModelAdmin(admin.ModelAdmin):
#    list_display = ['some', 'fields', ]
#    search_fields = ['some', 'fieds', ]


# admin.site.register(models.YourModel, YourModelAdmin)

class ClosingRulesAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(ClosingRulesAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        db_fieldname = canonical_fieldname(db_field)
        return field

admin.site.register(OpeningHours)
admin.site.register(ClosingRules, ClosingRulesAdmin)
admin.site.register(Company)
