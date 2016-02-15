from django.conf.urls import url
from openinghours.views import CurrentlyOpenView
from openinghours.views_edit import edit

urlpatterns = [
     url(r'^$', CurrentlyOpenView.as_view(), name='openinghours_currently_open'),
     url(r'^edit$', edit, name='openinghours_edit'),
]
