from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/openinghours/')),
    path('openinghours/', include('openinghours.urls')),
]
