import datetime

from .models import *

def getClosingRuleForNow(companySlug, now=None):
    '''
    Access the closing rules for a company
    '''
    if now is None:
        now = datetime.datetime.now()
    cr = ClosingRules.objects.filter(company__slug=companySlug, start__lte=now, end__gte=now)
    return cr
    
    
def hasClosingRuleForNow(companySlug, now=None):
    '''
    Has the company closing rules to evaluate?
    '''
    cr = getClosingRuleForNow(companySlug, now)
    return cr.count()
    
    
def isOpen(companySlug, now=None):
    '''
    Is the company currently open? Pass "now" to test with a specific timestamp.
    This method is used as stand alone and helper.
    '''
    if now is None:
        now = datetime.datetime.now()
    print "isOpen", now, now.isoweekday()
    
    if hasClosingRuleForNow(companySlug, now):
        return False
        
    nowTime = datetime.time(now.hour, now.minute, now.second)
    
    ohs = OpeningHours.objects.filter(company__slug=companySlug)
    for oh in ohs:
        is_open = False
        if (oh.weekday == now.isoweekday() and oh.fromHour <= nowTime and 
                ((oh.toHour >= nowTime and oh.toHour <= datetime.time(23, 59, 59)) or 
                ( oh.toHour >= datetime.time(0, 0, 0) and oh.toHour <= nowTime ) ) ):
            #print "regular case, same day between bounds", oh
            is_open = oh
            
        if (oh.weekday == (now.isoweekday()-1)%7 and oh.fromHour >= nowTime and oh.toHour >= nowTime and oh.toHour < oh.fromHour):
            is_open = oh
            #print " 'Special' case after midnight", oh
        
        if is_open is not False:
            return oh
    return False
    

def isClosed(companySlug, now=None):
    ''' Inverse function for isOpen. '''
    return not isOpen(companySlug, now)
    
    
def nextTimeOpen(companySlug):
    ''' 
    Returns the next possible opening hours object ( aka when is the company open for the next time?).
    '''
    if isClosed(companySlug):
        now = datetime.datetime.now()
        nowTime = datetime.time(now.hour, now.minute, now.second)
        foundOpeningHours = False
        for i in range(8):
            if i>0:
                lWeekday = (now.isoweekday()+i)%7
                print lWeekday, i
                ohs = OpeningHours.objects.filter(company__slug=companySlug, weekday=lWeekday).order_by('weekday','fromHour')
                if ohs.count():
                    for oh in ohs:
                        # we have a match
                        futureNow = now + datetime.timedelta(days=i)
                        tmpNow = datetime.datetime(futureNow.year, futureNow.month, futureNow.day, oh.fromHour.hour, oh.fromHour.minute, oh.fromHour.second)
                        if isOpen(companySlug, now=tmpNow):
                            foundOpeningHours = oh
                            break
                    if foundOpeningHours is not False:
                        return foundOpeningHours
    return False
