from django.views.generic import TemplateView


class CurrentOpeningsView(TemplateView):
    template_name = "openinghours/index.html"