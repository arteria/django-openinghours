"""Editing form for opening hours

Front-end untrusted end user grade UX aimed at business directory sites.

UX supports up to 2 sets of opening hours per day optimised for common stories:
9 till 5, closed for lunch, open till late, Saturday morning-closed on Sunday
"""

from django import forms
from datetime import time


def str_to_time(s):
    """ Turns strings like '08:30' to time objects """
    return time(*[int(x) for x in s.split(':')])


def time_to_str(t):
    """ Turns time objects to strings like '08:30' """
    return t.strftime('%H:%M')


def time_choices():
    """Return digital time choices every half hour from 00:00 to 23:30."""
    hours = list(range(0, 24))
    times = []
    for h in hours:
        hour = str(h).zfill(2)
        times.append(hour+':00')
        times.append(hour+':30')
    return list(zip(times, times))

TIME_CHOICES = time_choices()


class Slot(forms.Form):
    opens = forms.ChoiceField(choices=TIME_CHOICES)
    shuts = forms.ChoiceField(choices=TIME_CHOICES)
