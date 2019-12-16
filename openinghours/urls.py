from django.urls import path
from openinghours.views import CurrentlyOpenView
from openinghours.views_edit import OpeningHoursEditView

urlpatterns = [
     path('', CurrentlyOpenView.as_view(),
          name='openinghours_currently_open'),
     path('edit/<int:pk>', OpeningHoursEditView.as_view(),
          name='openinghours_edit'),
]
