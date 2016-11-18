# -*- coding: utf-8 -*-
from django.contrib import admin
from openinghours.models import OpeningHours, ClosingRules, Company
from openinghours.app_settings import PREMISES_MODEL


class OpeningHoursInline(admin.TabularInline):
    model = OpeningHours
    extra = 0


class ClosingRulesInline(admin.StackedInline):
    model = ClosingRules
    extra = 0


class CompanyAdmin(admin.ModelAdmin):
    inlines = [OpeningHoursInline, ClosingRulesInline]
    search_fields = ['name', 'slug']

# OPENINGHOURS_PREMISES_MODEL users need to register
# their own admin from their app
if PREMISES_MODEL == 'openinghours.Company':
    admin.site.register(Company, CompanyAdmin)
