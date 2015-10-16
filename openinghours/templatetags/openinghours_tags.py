import datetime

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
    if int(d) == getnow().isoweekday():
        return _("today")
    for w in WEEKDAYS:
        if w[0] == int(d):
            return w[1]


@register.filter(expects_localtime=True)
def toWeekday(dateObjTpl):
    oh, dateObj = dateObjTpl
    now = getnow()
    if dateObj.isoweekday() == now.isoweekday() and (dateObj - now).days == 0:
        return _("today")
    for w in WEEKDAYS:
        if w[0] == int(dateObj.isoweekday()):
            return w[1]


@register.assignment_tag
def isCompanyCurrentlyOpen(companySlug=None, attr=None):
    obj = isOpen(companySlug)
    if obj is False:
        return False
    if attr is not None:
        return getattr(obj, attr) 
    return obj

    
@register.filter(expects_localtime=True) 
def getCompanyNextOpeningHour(companySlug, attr=None):
    ''' 
    `attr` allowes to acces to a attribute of the OpeningHours model. 
    This is handy to access the start time for example...
    ''' 
    obj, ts = nextTimeOpen(companySlug)
    if obj is False:
        return False 
    elif attr is not None:
        return getattr(obj, attr) 
    return obj, ts
    
    
@register.filter(expects_localtime=True) 
def hasCompanyClosingRuleForNow(companySlug, attr=None):
    obj = hasClosingRuleForNow(companySlug)
    if obj is False:
        return False
    if attr is not None:
        return getattr(obj, attr) 
    return obj


@register.filter(expects_localtime=True) 
def getCompanyClosingRuleForNow(companySlug, attr=None):
    ''' this only access the first! closing rule. because closed is closed. '''
    obj = getClosingRuleForNow(companySlug)
    if obj is False:
        return False
    if attr is not None:
        return getattr(obj[0], attr) 
    return obj
               
    
@register.simple_tag
def companyOpeningHoursList(companySlug=None, concise=False):
    ''' Creates a rendered listing of hours. ''' 
    template_name = 'openinghours/companyOpeningHoursList.html'
    days = [] # [{'hours': '9:00am to 5:00pm', 'name': u'Monday'}, {'hours': '9:00am to...

    #If a `companySlug` is not provided, choose the first company.
    if companySlug: 
        ohrs = OpeningHours.objects.filter(company__slug=companySlug)
    else:
        ohrs = Company.objects.first().openinghours_set.all()

    ohrs.order_by('weekday', 'fromHour')

    for o in ohrs:
        days.append({
            'name': o.get_weekday_display(),
            'hours': '%s%s to %s%s' % (
                o.fromHour.strftime('%I:%M').lstrip('0'), 
                o.fromHour.strftime('%p').lower(),
                o.toHour.strftime('%I:%M').lstrip('0'), 
                o.toHour.strftime('%p').lower()
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
        
        days = concise_days

    t = template.loader.get_template(template_name)
    return t.render(template.Context({
        'days': days
    }))
