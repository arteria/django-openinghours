from django.conf import settings

COMPANY_MODEL = 'openinghours.Company'
PREMISES_MODEL = getattr(settings, 'OPENINGHOURS_PREMISES_MODEL', COMPANY_MODEL)
