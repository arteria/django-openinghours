# -*- coding: utf-8 -*-
import datetime

try:
    from threadlocals.threadlocals import get_current_request
except ImportError:
    get_current_request = None


from openinghours.models import OpeningHours, ClosingRules, Company


def get_now():
    ''''''
    # Allow access global request and read a timestamp from query...
    request = get_current_request()
    if request:
        openinghours_now = request.GET.get('openinghours-now')
        if openinghours_now:
            return datetime.datetime.strptime(openinghours_now, '%Y%m%d%H%M%S')
    return datetime.datetime.now()


def get_closing_rule_for_now(company_slug):
    '''
    Access the all closing rules for a company
    '''
    now = get_now()

    if company_slug:
        return ClosingRules.objects.filter(company__slug=company_slug, start__lte=now, end__gte=now)

    return Company.objects.first().closingrules_set.filter(start__lte=now, end__gte=now)


def has_closing_rule_for_now(company_slug):
    '''
    Has the company closing rules to evaluate?
    '''
    cr = get_closing_rule_for_now(company_slug)
    return cr.count()


def is_open(company_slug, now=None):
    '''
    Is the company currently open? Pass "now" to test with a specific timestamp.
    This method is used as stand alone and helper.
    '''
    if now is None:
        now = get_now()

    if has_closing_rule_for_now(company_slug):
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
        if (oh.weekday == (now.isoweekday() - 1) % 7 and oh.from_hour >= now_time and oh.to_hour >= now_time and oh.to_hour < oh.from_hour):
            is_open = oh
            # print " 'Special' case after midnight", oh

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
            l_weekday = (now.isoweekday() + i) % 8
            ohs = OpeningHours.objects.filter(company__slug=company_slug, weekday=l_weekday).order_by('weekday','from_hour')

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
