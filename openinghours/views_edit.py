from openinghours.models import OpeningHours, WEEKDAYS
from openinghours.forms import Slot, time_to_str, str_to_time
from openinghours.utils import get_premises_model
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from collections import OrderedDict


class OpeningHoursEditView(DetailView):
    """Powers editing UI supporting up to 2 time slots (sets) per day.

    Models still support more slots via shell or admin UI.
    This UI will delete and not recreate anything above 2 daily slots.

    Inspired by Google local opening hours UI and earlier works.
    """
    model = get_premises_model()
    template_name = "openinghours/edit_base.html"

    def form_prefix(self, day_n, slot_n):
        """Form prefix made up of day number and slot number.

        - day number 1-7 for Monday to Sunday
        - slot 1-2 typically morning and afternoon
        """
        return "day%s_%s" % (day_n, slot_n)

    def post(self, request, pk):
        """ Clean the data and save opening hours in the database.
        Old opening hours are purged before new ones are saved.
        """
        location = self.get_object()
        # open days, disabled widget data won't make it into request.POST
        present_prefixes = [x.split('-')[0] for x in request.POST.keys()]
        day_forms = OrderedDict()
        for day_no, day_name in WEEKDAYS:
            for slot_no in (1, 2):
                prefix = self.form_prefix(day_no, slot_no)
                # skip closed day as it would be invalid form due to no data
                if prefix not in present_prefixes:
                    continue
                day_forms[prefix] = (day_no, Slot(request.POST, prefix=prefix))

        if all([day_form[1].is_valid() for pre, day_form in day_forms.items()]):
            OpeningHours.objects.filter(company=location).delete()
            for prefix, day_form in day_forms.items():
                day, form = day_form
                opens, shuts = [str_to_time(form.cleaned_data[x])
                                for x in ('opens', 'shuts')]
                if opens != shuts:
                    OpeningHours(from_hour=opens, to_hour=shuts,
                                 company=location, weekday=day).save()
        return redirect(request.path_info)

    def get(self, request, pk):
        """ Initialize the editing form

        1. Build opening_hours, a lookup dictionary to populate the form
           slots: keys are day numbers, values are lists of opening
           hours for that day.
        2. Build days, a list of days with 2 slot forms each.
        3. Build form initials for the 2 slots padding/trimming
           opening_hours to end up with exactly 2 slots even if it's
           just None values.
        """
        location = self.get_object()
        two_sets = False
        closed = None
        opening_hours = {}
        for o in OpeningHours.objects.filter(company=location):
            opening_hours.setdefault(o.weekday, []).append(o)
        days = []
        for day_no, day_name in WEEKDAYS:
            if day_no not in opening_hours.keys():
                if opening_hours:
                    closed = True
                ini1, ini2 = [None, None]
            else:
                closed = False
                ini = [{'opens': time_to_str(oh.from_hour),
                        'shuts': time_to_str(oh.to_hour)}
                       for oh in opening_hours[day_no]]
                ini += [None] * (2 - len(ini[:2]))  # pad
                ini1, ini2 = ini[:2]  # trim
                if ini2:
                    two_sets = True
            days.append({
                'name': day_name,
                'number': day_no,
                'slot1': Slot(prefix=self.form_prefix(day_no, 1), initial=ini1),
                'slot2': Slot(prefix=self.form_prefix(day_no, 2), initial=ini2),
                'closed': closed
            })
        return render(request, self.template_name, {
            'days': days,
            'two_sets': two_sets,
            'location': location,
        })
