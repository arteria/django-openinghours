from django.views.generic import TemplateView
from openinghours.utils import get_premises_model


class CurrentlyOpenView(TemplateView):
    model = get_premises_model()
    template_name = "openinghours/index.html"

    def get_context_data(self, **kwargs):
        context = super(CurrentlyOpenView, self).get_context_data(**kwargs)
        context['location'] = self.model.objects.first()
        return context
