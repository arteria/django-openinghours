from django import template
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode 
from django.template.loader import render_to_string

 
import datetime
from openinghours.models import *

register = template.Library()


#TODO: https://docs.djangoproject.com/en/1.5/topics/i18n/timezones/#time-zones-in-templates

@register.filter(expects_localtime=True)
def isCompanyCurrentlyOpen(companySlug):
    '''
    Is the company currently open?
    '''
    now = datetime.datetime.now()
    nowTime = datetime.time(datetime.datetime.now().hour,datetime.datetime.now().minute, datetime.datetime.now().second)
    return bool(OpeningHours.objects.filter(company__slug=companySlug, 
            weekday=now.isoweekday(), 
            fromHour__lte=nowTime, 
            toHour__gte=nowTime).count())
    # TODO: closing hours!
    
    
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