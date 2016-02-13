from django.views.generic import TemplateView


class CurrentlyOpenView(TemplateView):
    template_name = "openinghours/index.html"
