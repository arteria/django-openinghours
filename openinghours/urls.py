from django.conf.urls import patterns, url

urlpatterns = patterns(
     'openinghours.views',    url(r'^$', 'currentOpenings', name='openinghours_current_openings'),
)
