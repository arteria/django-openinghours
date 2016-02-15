from openinghours.models import OpeningHours, WEEKDAYS
from openinghours.forms import Slot
from django.shortcuts import render

def edit(request):
    oh = OpeningHours.objects.filter(company_id=1).order_by('weekday')
    
    week = []
    for day in WEEKDAYS:
        pre = "day%s_" % day[0]
        week.append({
            'weekday': day,
            'slot1': Slot(prefix=pre+'1'),
            'slot2': Slot(prefix=pre+'2'),
        })
    
    if request.method == 'POST':
        pass
        
    return render(request, "openinghours/form.html", {
        'week': week,
    })
