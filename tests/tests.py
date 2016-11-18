from django.test import TestCase, Client
from openinghours.models import Company, OpeningHours, ClosingRules
from openinghours.forms import str_to_time
from datetime import datetime, timedelta


class OpeningHoursTestCase(TestCase):
    """Test some possible business scenarios."""
    def setUp(self):
        """Create test opening hours and holidays:

        - late opening for Monday and Tuesday
        - some planned breaks
        - closed on a Sunday
        """
        test_data = {
            1: ['08:30 12:00', '12:30 22:00'],
            2: ['08:30 12:00', '12:30 18:00', '18:30 22:00'],
            3: ['09:00 17:00'],
            4: ['09:00 17:00'],
            5: ['09:00 17:00'],
            6: ['10:00 13:00'],
            7: None,
        }
        self.company, created = Company.objects.get_or_create(name="Company Ltd.",
                                                         slug="company-ltd")
        for day, hours in test_data.items():
            if not hours:
                continue
            for slot in hours:
                from_hour, to_hour = slot.split()
                OpeningHours.objects.get_or_create(
                    company=self.company,
                    weekday=day,
                    from_hour=str_to_time(from_hour),
                    to_hour=str_to_time(to_hour)
                )

        holiday = ClosingRules.objects.create(
            company=self.company,
            start=datetime(2015, 12, 25) - timedelta(days=2),
            end=datetime(2015, 12, 25) + timedelta(days=4),
            reason="Public holiday"
        )

    def tearDown(self):
        """Reset state by hand while developing tests in the shell."""
        for o in OpeningHours.objects.all():
            o.delete()
