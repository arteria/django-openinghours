import datetime
from django.conf import settings
try:
    from threadlocals.threadlocals import get_current_request
except ImportError:
    get_current_request = None
from openinghours.models import OpeningHours, ClosingRules, PREMISES_MODEL
from django.core.exceptions import ImproperlyConfigured

from compat import get_model


def get_premises_model():
    """
    Support for custom company premises model
    with developer friendly validation.
    """
    try:
        app_label, model_name = PREMISES_MODEL.split('.')
    except ValueError:
        raise ImproperlyConfigured("OPENINGHOURS_PREMISES_MODEL must be of the"
                                   " form 'app_label.model_name'")
    premises_model = get_model(app_label=app_label, model_name=model_name)
    if premises_model is None:
        raise ImproperlyConfigured("OPENINGHOURS_PREMISES_MODEL refers to"
                                   " model '%s' that has not been installed"
                                   % PREMISES_MODEL)
    return premises_model

Company = get_premises_model()


def get_now():
    """
    Allows to access global request and read a timestamp from query.
    """
    if not get_current_request:
        return datetime.datetime.now()
    request = get_current_request()
    if request:
        openinghours_now = request.GET.get('openinghours-now')
        if openinghours_now:
            return datetime.datetime.strptime(openinghours_now, '%Y%m%d%H%M%S')
    return datetime.datetime.now()


def get_closing_rule_for_now(location):
    """
    Returns QuerySet of ClosingRules that are currently valid
    """
    now = get_now()

    if location:
        return ClosingRules.objects.filter(company=location,
                                           start__lte=now, end__gte=now)

    return Company.objects.first().closingrules_set.filter(start__lte=now,
                                                           end__gte=now)


def has_closing_rule_for_now(location):
    """
    Does the company have closing rules to evaluate?
    """
    cr = get_closing_rule_for_now(location)
    return cr.count()


def is_open(location, now=None):
    """
    Is the company currently open? Pass "now" to test with a specific
    timestamp. Can be used stand-alone or as a helper.
    """
    if now is None:
        now = get_now()

    if has_closing_rule_for_now(location):
        return False

    now_time = datetime.time(now.hour, now.minute, now.second)

    if location:
        ohs = OpeningHours.objects.filter(company=location)
    else:
        ohs = Company.objects.first().openinghours_set.all()
    for oh in ohs:
        is_open = False
        # start and end is on the same day
        if (oh.weekday == now.isoweekday() and
                oh.from_hour <= now_time and
                now_time <= oh.to_hour):
            is_open = oh

        # start and end are not on the same day and we test on the start day
        if (oh.weekday == now.isoweekday() and
                oh.from_hour <= now_time and
                ((oh.to_hour < oh.from_hour) and
                    (now_time < datetime.time(23, 59, 59)))):
            is_open = oh

        # start and end are not on the same day and we test on the end day
        if (oh.weekday == (now.isoweekday() - 1) % 7 and
                oh.from_hour >= now_time and
                oh.to_hour >= now_time and
                oh.to_hour < oh.from_hour):
            is_open = oh
            # print " 'Special' case after midnight", oh

        if is_open is not False:
            return oh
    return False


def next_time_open(location):
    """
    Returns the next possible opening hours object, or (False, None)
    if location is currently open or there is no such object
    I.e. when is the company open for the next time?
    """
    if not is_open(location):
        now = get_now()
        now_time = datetime.time(now.hour, now.minute, now.second)
        found_opening_hours = False
        for i in range(8):
            l_weekday = (now.isoweekday() + i) % 8
            ohs = OpeningHours.objects.filter(company=location,
                                              weekday=l_weekday
                                              ).order_by('weekday',
                                                         'from_hour')

            if ohs.count():
                for oh in ohs:
                    future_now = now + datetime.timedelta(days=i)
                    # same day issue
                    tmp_now = datetime.datetime(future_now.year,
                                                future_now.month,
                                                future_now.day,
                                                oh.from_hour.hour,
                                                oh.from_hour.minute,
                                                oh.from_hour.second)
                    if tmp_now < now:
                        tmp_now = now  # be sure to set the bound correctly...
                    if is_open(location, now=tmp_now):
                        found_opening_hours = oh
                        break
                if found_opening_hours is not False:
                    return found_opening_hours, tmp_now
    return False, None
