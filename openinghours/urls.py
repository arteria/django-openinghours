from django.conf.urls import url
from openinghours.views import CurrentlyOpenView


urlpatterns = [
     url(r'^$', CurrentlyOpenView.as_view(), name='openinghours_currently_open'),
]