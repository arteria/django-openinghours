from django.views.generic import TemplateView
from openinghours.models import Company

class CurrentlyOpenView(TemplateView):
    template_name = "openinghours/index.html"
    
    def get_context_data(self, **kwargs):
        context = super(CurrentlyOpenView, self).get_context_data(**kwargs)
        context['location'] = Company.objects.first()
        return context
