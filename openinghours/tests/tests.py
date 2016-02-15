from django.test import TestCase, Client
from openinghours.models import Company, OpeningHours, ClosingRules
import datetime

class OpeningHoursTestCase(TestCase):
    """Test some possible business scenarios."""
    def setUp(self):
        """Create test opening hours and holidays:
        
        - late opening for Monday and Tuesday
        - some planned breaks
        - closed on a Sunday
        """
        test_data = {
            1: [[( 8,30), (12,00)], [(12,30), (22,00)]],
            2: [[( 8,30), (12,00)], [(12,30), (18,00)], [(18,30), (22,00)]],
            3: [[( 9,00), (17,00)]],
            4: [[( 9,00), (17,00)]],
            5: [[( 9,00), (17,00)]],
            6: [[(10,00), (13,00)]],
            7: None,
        }
        company, created = Company.objects.get_or_create(name="Company Ltd.", slug="company-ltd")
        for day, hours in test_data.items():
            if not hours:
                continue
            for from_hour, to_hour in hours:
                OpeningHours.objects.get_or_create(
                    company   = company,
                    weekday   = day,
                    from_hour = datetime.time(*from_hour),
                    to_hour   = datetime.time(*to_hour)
                )
        # setup some holidays
        today = datetime.datetime.today()
        holiday = ClosingRules.objects.create(
            company = company,
            start  = today+datetime.timedelta(days=2),
            end    = today+datetime.timedelta(days=4),
            reason = "Public holiday"
        )
    
    def tearDown(self):
        """Reset state by hand while developing tests in the shell."""
        for o in OpeningHours.objects.all():
            o.delete()
    
    def test_hours_are_published(self):
        response = Client().get('/')
        self.assertContains(response, '8:30am to 12:00pm')
        self.assertContains(response, '10:00am to 1:00pm')
