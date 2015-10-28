from django.conf.urls import url
from openinghours.views import CurrentOpeningsView


urlpatterns = [
     url(r'^$', CurrentOpeningsView.as_view(), name='openinghours_current_openings'),
]