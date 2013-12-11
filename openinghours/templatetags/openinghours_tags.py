from django import template
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode 
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

 
import datetime
from openinghours.models import *
from openinghours.utils import *

register = template.Library()


#TODO: https://docs.djangoproject.com/en/1.5/topics/i18n/timezones/#time-zones-in-templates


@register.filter(expects_localtime=True)
def isoDayToWeekday(d):
    if int(d) == datetime.datetime.now().isoweekday():
        return _("today")
    for w in WEEKDAYS:
        if w[0] == int(d):
            return w[1]


@register.filter(expects_localtime=True)
def toWeekday(dateObjTpl):
    oh, dateObj = dateObjTpl
    if dateObj.isoweekday() == datetime.datetime.now().isoweekday() and (dateObj - datetime.datetime.now()).days == 0:
        return _("today")
    for w in WEEKDAYS:
        if w[0] == int(dateObj.isoweekday()):
            return w[1]

@register.filter(expects_localtime=True)
def isCompanyCurrentlyOpen(companySlug, attr=None):
    obj = isOpen(companySlug)
    if obj is False:
        return False
    if attr is not None:
        return getattr(obj, attr) 
    return obj
    
    
@register.filter(expects_localtime=True) 
def getCompanyNextOpeningHour(companySlug, attr=None):
    ''' ''' 
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
               
    
@register.filter
def companyOpeningHoursList(companySlug):
    '''
    ''' 
    ans = []
    #tAns = ''
    ohrs = OpeningHours.objects.filter(company__slug=companySlug).order_by('weekday', 'fromHour')
    for o in ohrs:
        lWD = ''
        for wd in WEEKDAYS: 
            print wd[0], o.weekday, wd[0] == o.weekday
            if wd[0] == o.weekday:
                lWD = wd[1]
                print lWD
                break
        fromT = "%02d:%02d" % (o.fromHour.hour, o.fromHour.minute)
        toT = "%02d:%02d" % (o.toHour.hour, o.toHour.minute)
        ans.append([force_unicode(lWD), fromT, toT])
        
        #tAns += "%s %s - %s <br>" % (force_unicode(lWD), fromT, toT )
    #print tAns
    
    return mark_safe(render_to_string('openinghours/companyOpeningHoursList.html', {'ohrs':ans}))