from django.conf.urls import url
from openinghours.views import CurrentlyOpenView
from openinghours.views_edit import OpeningHoursEditView

urlpatterns = [
     url(r'^$', CurrentlyOpenView.as_view(),
         name='openinghours_currently_open'),
     url(r'^edit/(?P<pk>[0-9]+)$', OpeningHoursEditView.as_view(),
         name='openinghours_edit'),
]
