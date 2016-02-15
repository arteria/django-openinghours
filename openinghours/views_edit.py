from openinghours.models import OpeningHours, WEEKDAYS
from openinghours.forms import Slot, time_to_str, str_to_time
from openinghours import utils
from django.shortcuts import render, redirect, get_object_or_404


def edit(request, pk):
    """Crowd facing editing UI supporting one or two time slots (sets) per day.

    Models still support more slots via shell or admin UI.
    """
    Location = utils.get_premises_model()
    location = get_object_or_404(Location, pk=pk)

    def prefix(day_n, slot_n): return "day%s_%s" % (day_n, slot_n)

    if request.method == 'POST':
        # TODO: write tests
        day_forms = []
        for day, day_name in WEEKDAYS:
            for s in (1, 2):
                day_forms += [[day, Slot(request.POST, prefix=prefix(day, s))]]
        if all([form.is_valid() for day, form in day_forms]):
            OpeningHours.objects.filter(company=location).delete()
            for day, slot in day_forms:
                opens, shuts = [str_to_time(slot.cleaned_data[x])
                                for x in ('opens', 'shuts')]
                if opens != shuts:
                    OpeningHours(from_hour=opens, to_hour=shuts,
                                 company=location, weekday=day).save()
            return redirect(request.path_info)

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
    return render(request, "openinghours/form.html", {
        'week': week,
        'two_sets': two_sets
    })
