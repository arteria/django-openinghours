import datetime

from django.conf import settings


try:
    from threadlocals.threadlocals import get_current_request
except ImportError:
    get_current_request = None


from openinghours.models import OpeningHours, ClosingRules, Company


def get_now():
    ''' '''
    now = datetime.datetime.now()
    # Allow access global request and read a timestamp from query...
    # I'm not exactly sure what you were trying to do here so I left it. - JJ
    if 'get_current_request' is not None:
        request = get_current_request()
        try:
            _now = request.GET.get('openinghours-now', None)
            now = datetime.datetime.strptime(_now, '%Y%m%d%H%M%S')
        except AttributeError:
            pass  
    return now


def get_closing_rule_for_now(company_slug):
    '''
    Access the all closing rules for a company
    '''
    now = get_now()
    if company_slug:
        cr = ClosingRules.objects.filter(company__slug=company_slug, start__lte=now, end__gte=now)
    else:
        cr = Company.objects.first().closingrules_set.filter(start__lte=now, end__gte=now)
    return cr
    
    
def has_closing_rule_for_now(company_slug):
    '''
    Has the company closing rules to evaluate?
    '''
    now = get_now()
    cr = get_closing_rule_for_now(company_slug)
    return cr.count()
    
    
def is_open(company_slug, now=None):
    '''
    Is the company currently open? Pass "now" to test with a specific timestamp.
    This method is used as stand alone and helper.
    '''
    if now is None:
        now = get_now()
    print "is_open", now, now.isoweekday()
    
    if has_closing_rule_for_now(company_slug):
        print "has_no_closing_rule"
        return False
        
    now_time = datetime.time(now.hour, now.minute, now.second)
    
    if company_slug:
        ohs = OpeningHours.objects.filter(company__slug=company_slug)
    else:
        ohs = Company.objects.first().openinghours_set.all()
    for oh in ohs:
        is_open = False
        # start and end is on the same day
        if oh.weekday == now.isoweekday() and oh.from_hour <= now_time and now_time <= oh.to_hour: 
           is_open = oh
        
        # start and end are not on the same day and we test on the start day
        if oh.weekday == now.isoweekday() and oh.from_hour <= now_time and ((oh.to_hour < oh.from_hour) and (now_time < datetime.time(23, 59, 59))):
            is_open = oh
            
        # start and end are not on the same day and we test on the end day
        if (oh.weekday == (now.isoweekday()-1)%7 and oh.from_hour >= now_time and oh.to_hour >= now_time and oh.to_hour < oh.from_hour):
            is_open = oh
            #print " 'Special' case after midnight", oh
        
        if is_open is not False:
            return oh
    return False
    
    
def next_time_open(company_slug):
    ''' 
    Returns the next possible opening hours object ( aka when is the company open for the next time?).
    '''
    if not is_open(company_slug):
        now = get_now()
        now_time = datetime.time(now.hour, now.minute, now.second)
        found_opening_hours = False
        for i in range(8):
            lWeekday = (now.isoweekday()+i)%8
            ohs = OpeningHours.objects.filter(company__slug=company_slug, weekday=lWeekday).order_by('weekday','from_hour')
            
            if ohs.count():
                for oh in ohs:
                    future_now = now + datetime.timedelta(days=i)
                    # same day issue
                    tmp_now = datetime.datetime(future_now.year, future_now.month, future_now.day, oh.from_hour.hour, oh.from_hour.minute, oh.from_hour.second)
                    if tmp_now < now:
                        tmp_now = now # be sure to set the bound correctly...
                    if is_open(company_slug, now=tmp_now):
                        found_opening_hours = oh
                        break
                if found_opening_hours is not False:
                    return found_opening_hours, tmp_now
    return False, None
