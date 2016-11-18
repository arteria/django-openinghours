from django.conf import settings

PREMISES_MODEL = getattr(settings, 'OPENINGHOURS_PREMISES_MODEL',
                                   'openinghours.Company')
