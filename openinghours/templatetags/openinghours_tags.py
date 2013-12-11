from django import template
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode 
from django.template.loader import render_to_string

 
import datetime
from openinghours.models import *
from openinghours.utils import *

register = template.Library()


#TODO: https://docs.djangoproject.com/en/1.5/topics/i18n/timezones/#time-zones-in-templates

@register.filter(expects_localtime=True)
def isCompanyCurrentlyOpen(companySlug):
    return isOpen(companySlug)

@register.filter(expects_localtime=True) 
def getCompanyNextOpeningHour(companySlug):
    return nextTimeOpen(companySlug)
    
@register.filter(expects_localtime=True) 
def hasCompanyClosingRuleForNow(companySlug):
    return hasClosingRuleForNow(companySlug)
    
@register.filter
def companyOpeningHoursList(companySlug):
    '''
    ''' 
    ans = []
    #tAns = ''
    ohrs = OpeningHours.objects.filter(company__slug=companySlug).order_by('weekday','fromHour')
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