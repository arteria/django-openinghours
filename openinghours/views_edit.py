from openinghours.models import OpeningHours, WEEKDAYS
from openinghours.forms import Slot, time_to_str, str_to_time
from openinghours import utils
from django.shortcuts import render, get_object_or_404


def edit(request, pk):
    """Crowd facing editing UI supporting one or two time slots (sets) per day.

    Models still support more slots via shell or admin UI.
    """
    Location = utils.get_premises_model()
    location = get_object_or_404(Location, pk=pk)
    
    # build a lookup dictionary to populate the form slots
    # day numbers are keys, list of opening hours for that day are values
    hours = {}
    for o in OpeningHours.objects.filter(company=location):
        hours.setdefault(o.weekday, []).append(o)

    two_sets = False
    week = []
    for day in WEEKDAYS:
        day_n = day[0]
        # Here, we generate form initials for the 2 slots.
        if day_n not in hours.keys():
            closed = True
            ini1, ini2 = [None, None]
        else:
            closed = False
            ini = [{'opens': time_to_str(oh.from_hour),
                    'shuts': time_to_str(oh.to_hour)}
                   for oh in hours[day_n]]
            ini += [None] * (2 - len(ini[:2]))  # pad
            ini1, ini2 = ini[:2]  # trim
            if ini2:
                two_sets = True

        pre = "day%s_" % day_n
        week.append({
            'weekday': day,
            'slot1': Slot(prefix=pre+'1', initial=ini1),
            'slot2': Slot(prefix=pre+'2', initial=ini2),
            'closed': closed
        })

    if request.method == 'POST':
        pass

    return render(request, "openinghours/form.html", {
        'week': week,
        'two_sets': two_sets
    })
