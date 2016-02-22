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
        company, created = Company.objects.get_or_create(name="Company Ltd.",
                                                         slug="company-ltd")
        for day, hours in test_data.items():
            if not hours:
                continue
            for slot in hours:
                from_hour, to_hour = slot.split()
                OpeningHours.objects.get_or_create(
                    company=company,
                    weekday=day,
                    from_hour=str_to_time(from_hour),
                    to_hour=str_to_time(to_hour)
                )

        def days_ahead(d): return datetime.today() + timedelta(days=d)

        # setup some holidays
        holiday = ClosingRules.objects.create(
            company=company,
            start=days_ahead(2),
            end=days_ahead(4),
            reason="Public holiday"
        )

    def tearDown(self):
        """Reset state by hand while developing tests in the shell."""
        for o in OpeningHours.objects.all():
            o.delete()

    def test_hours_are_published(self):
        response = Client().get('/')
        self.assertContains(response, '8:30am to 12:00pm')
        self.assertContains(response, '10:00am to 1:00pm')
    
    def test_edit_form(self):
        self.tearDown()
        post_data = {
            'day1_1-opens': '11:30', 'day1_1-shuts': '17:30',
            'day2_1-opens': '11:30', 'day2_1-shuts': '17:30',
            'day3_1-opens': '11:30', 'day3_1-shuts': '17:30',
            'day4_1-opens': '11:30', 'day4_1-shuts': '17:30',
            'day5_1-opens': '11:30', 'day5_1-shuts': '17:30',
            'day6_1-opens': '11:30', 'day6_1-shuts': '13:30',
            'day7_1-opens': '00:00', 'day7_1-shuts': '00:00',
            'day1_2-opens': '00:00', 'day1_2-shuts': '00:00',
            'day2_2-opens': '00:00', 'day2_2-shuts': '00:00',
            'day3_2-opens': '00:00', 'day3_2-shuts': '00:00',
            'day4_2-opens': '00:00', 'day4_2-shuts': '00:00',
            'day5_2-opens': '00:00', 'day5_2-shuts': '00:00',
            'day6_2-opens': '00:00', 'day6_2-shuts': '00:00',
            'day7_2-opens': '00:00', 'day7_2-shuts': '00:00',
        }
        post = Client().post('/edit/1', post_data)
        resp = Client().get('/edit/1')
        self.assertContains(resp, '<option value="11:30" selected', count=6)
        self.assertContains(resp, '<option value="17:30" selected', count=5)
        self.assertContains(resp, '<option value="00:00">', count=7*2*2)
        resp2 = Client().get('/')
        self.assertContains(resp2, '11:30am')
        self.assertContains(resp2, '5:30pm')
