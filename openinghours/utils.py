import datetime

from .models import *

def getClosingRuleForNow(companySlug, now=None):
    if now is None:
        now = datetime.datetime.now()
    cr = ClosingRules.objects.filter(company__slug=companySlug, start__lte=now, end__gte=now)
    return cr
    
    
def hasClosingRuleForNow(companySlug, now=None):
    cr = getClosingRuleForNow(companySlug, now)
    return cr.count()
    
    
def isOpen(companySlug):
    '''
    Is the company currently open?
    '''
    now = datetime.datetime.now()
    
    nowTime = datetime.time(datetime.datetime.now().hour, 
            datetime.datetime.now().minute, 
            datetime.datetime.now().second)
    
    # Regular case before midnight
    matches = OpeningHours.objects.filter(company__slug=companySlug, 
            weekday=now.isoweekday(), 
            fromHour__lte=nowTime, 
            toHour__gte=nowTime).count()
    
    # "Special" case after midnight ( eg. Friday 22:00:00 .. 02:00:00)
    matches += OpeningHours.objects.filter(company__slug=companySlug, 
                weekday=(now.isoweekday()-1)%7, 
                fromHour__gte=nowTime, 
                toHour__gte=nowTime).count()

    if matches:
        if hasClosingRuleForNow(companySlug, now):
            matches = 0
    return bool(matches)


def isClosed(companySlug):
    ''' Inverse function for isOpen. '''
    return not isOpen(companySlug)
    
    
def nextTimeOpen():
    pass

