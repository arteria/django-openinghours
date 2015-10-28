from django.conf.urls import patterns, url


urlpatterns = patterns(
     'openinghours.views',    url(r'^$', 'current_openings', name='openinghours_current_openings'),
)
