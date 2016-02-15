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
    
    def prefix(day_n, slot_n): return "day%s_%s" % (day_n, slot_n)
    
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

        week.append({
            'weekday': day,
            'slot1': Slot(prefix=prefix(day_n, 1), initial=ini1),
            'slot2': Slot(prefix=prefix(day_n, 2), initial=ini2),
            'closed': closed
        })

    if request.method == 'POST':
        # low level processing of the raw POST data
        post = dict(request.POST)
        data = []
        for k,v in post.items():
            if not k.startswith('day'):
                continue
            day_id, time_id = k.split('_')
            day_n = int(day_id[-1])   # 1 for Monday, 2 for Tuesday, 3 for ...
            slot_n = int(time_id[0])  # 1 for morning slot, 2 for afternoon
            open_shut = time_id[2:]   # string 'opens' or 'shuts'
            time = str_to_time(v[0])  # time object: time(15, 30)
            data.append((day_n, slot_n, time, open_shut))
        data = sorted(data)
        from pprint import pprint
        pprint(data)

    return render(request, "openinghours/form.html", {
        'week': week,
        'two_sets': two_sets
    })
