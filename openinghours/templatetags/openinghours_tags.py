import datetime

# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode 
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from openinghours.models import *
from openinghours.utils import *


register = template.Library()


@register.filter(expects_localtime=True)
def isoDayToWeekday(d):
    if int(d) == get_now().isoweekday():
        return _("today")
    for w in WEEKDAYS:
        if w[0] == int(d):
            return w[1]


@register.filter(expects_localtime=True)
def toWeekday(dateObjTpl):
    oh, date_obj = dateObjTpl
    now = get_now()
    if date_obj.isoweekday() == now.isoweekday() and (date_obj - now).days == 0:
        return _("today")
    for w in WEEKDAYS:
        if w[0] == int(date_obj.isoweekday()):
            return w[1]


@register.assignment_tag
def isCompanyCurrentlyOpen(company_slug=None, attr=None):
    obj = is_open(company_slug)
    if obj is False:
        return False
    if attr is not None:
        return getattr(obj, attr) 
    return obj

    
@register.filter(expects_localtime=True) 
def getCompanyNextOpeningHour(company_slug, attr=None):
    ''' 
    `attr` allowes to acces to a attribute of the OpeningHours model. 
    This is handy to access the start time for example...
    ''' 
    obj, ts = next_time_open(company_slug)
    if obj is False:
        return False 
    elif attr is not None:
        return getattr(obj, attr) 
    return obj, ts
    
    
@register.filter(expects_localtime=True) 
def has_closing_rule_for_now(company_slug, attr=None):
    obj = has_closing_rule_for_now(company_slug)
    if obj is False:
        return False
    if attr is not None:
        return getattr(obj, attr) 
    return obj


@register.filter(expects_localtime=True) 
def getCompanyClosingRuleForNow(company_slug, attr=None):
    ''' this only access the first! closing rule. because closed is closed. '''
    obj = get_closing_rule_for_now(company_slug)
    if obj is False:
        return False
    if attr is not None:
        return getattr(obj[0], attr) 
    return obj
               
    
@register.simple_tag
def companyOpeningHoursList(company_slug=None, concise=False):
    ''' Creates a rendered listing of hours. ''' 
    template_name = 'openinghours/companyOpeningHoursList.html'
    days = [] # [{'hours': '9:00am to 5:00pm', 'name': u'Monday'}, {'hours': '9:00am to...

    #If a `company_slug` is not provided, choose the first company.
    if company_slug: 
        ohrs = OpeningHours.objects.filter(company__slug=company_slug)
    else:
        try:
            ohrs = Company.objects.first().openinghours_set.all()
        except AttributeError:
            raise Exception("You must define some opening hours to use the opening hours tags.")

    ohrs.order_by('weekday', 'from_hour')

    for o in ohrs:
        days.append({
            'name': o.get_weekday_display(),
            'hours': '%s%s to %s%s' % (
                o.from_hour.strftime('%I:%M').lstrip('0'), 
                o.from_hour.strftime('%p').lower(),
                o.to_hour.strftime('%I:%M').lstrip('0'), 
                o.to_hour.strftime('%p').lower()
            )
        })
    for day in WEEKDAYS:
        if day[1] not in [open_day['name'] for open_day in days]:
            days.append({
                'name': str(day[1]),
                'hours': 'Closed'
            })

    if concise:
        # [{'hours': '9:00am to 5:00pm', 'day_names': u'Monday to Friday'}, {'hours':...
        template_name = 'openinghours/companyOpeningHoursListConcise.html'
        concise_days = []
        current_set = {}
        for day in days:
            if 'hours' not in current_set.keys():
                current_set = {'day_names': [day['name'],], 'hours': day['hours']}
            elif day['hours'] != current_set['hours']:
                concise_days.append(current_set)
                current_set = {'day_names': [day['name'],], 'hours': day['hours']}
            else:
                current_set['day_names'].append(day['name'])
        concise_days.append(current_set)

        for day_set in concise_days:
            if len(day_set['day_names']) > 2:
                day_set['day_names'] = '%s to %s' % (day_set['day_names'][0], day_set['day_names'][-1])
            elif len(day_set['day_names']) > 1:
                day_set['day_names'] = '%s and %s' % (day_set['day_names'][0], day_set['day_names'][-1])
            else:
                day_set['day_names'] = '%s' % day_set['day_names'][0]
        
        days = concise_days

    t = template.loader.get_template(template_name)
    return t.render(template.Context({
        'days': days
    }))
