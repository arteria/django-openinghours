from django.utils.encoding import force_text
from freezegun import freeze_time

from openinghours.models import OpeningHours, ClosingRules
from openinghours.templatetags.openinghours_tags import iso_day_to_weekday, is_open, next_time_open, \
    has_closing_rule_for_now, get_closing_rule_for_now, opening_hours
from openinghours.tests.tests import OpeningHoursTestCase


class TemplatetagsTestCase(OpeningHoursTestCase):

    def setUp(self):
        super(TemplatetagsTestCase, self).setUp()

    def tearDown(self):
        super(TemplatetagsTestCase, self).tearDown()

    def test_iso_day_to_weekday(self):
        with freeze_time("2016-02-22"):  # Monday
            self.assertEqual(force_text(iso_day_to_weekday(1)), u'today')
            self.assertNotEqual(force_text(iso_day_to_weekday(2)), u'today')
        with freeze_time("2016-02-23"):  # Tuesday
            self.assertNotEqual(force_text(iso_day_to_weekday(1)), u'today')
            self.assertEqual(force_text(iso_day_to_weekday(2)), u'today')

    def test_to_weekday(self):
        pass  # TODO: Write test

    def test_is_open(self):
        with freeze_time("2016-02-22 09:00:00"):  # Monday
            self.assertEqual(
                    is_open(self.company),
                    OpeningHours.objects.filter(company=self.company).first()
            )
        with freeze_time("2016-02-22 12:15:00"):  # Monday
            self.assertFalse(is_open(self.company))
        with freeze_time("2016-02-22 23:00:30"):  # Monday
            self.assertFalse(is_open(self.company))
        with freeze_time("2016-02-23 17:59:59"):  # Tuesday
            self.assertTrue(is_open(self.company))
        with freeze_time("2016-02-23 18:00:00"):  # Tuesday
            self.assertTrue(is_open(self.company))
        with freeze_time("2016-02-23 18:00:01"):  # Tuesday
            self.assertFalse(is_open(self.company))
        with freeze_time("2016-02-23 18:29:59"):  # Tuesday
            self.assertFalse(is_open(self.company))
        with freeze_time("2016-02-23 18:30:00"):  # Tuesday
            self.assertTrue(is_open(self.company))

    def test_next_time_open(self):
        with freeze_time("2016-02-22 08:00:00"):  # Monday
            self.assertEqual(
                    next_time_open(self.company),
                    OpeningHours.objects.filter(company=self.company).first()
            )
        with freeze_time("2016-02-22 09:00:00"):  # Monday
            self.assertFalse(next_time_open(self.company))

    def test_next_time_open_on_sunday(self):
        with freeze_time("2018-02-25 08:00:00"):  # Sunday
            oh = OpeningHours.objects.create(
                company=self.company,
                weekday=1,
                from_hour='00:00:00',
                to_hour='23:00:00',
            )
            self.assertEqual(
                next_time_open(self.company),
                oh,
            )

    def test_has_closing_rule_for_now(self):
        with freeze_time("2015-12-26 10:00:00"):  # Holiday
            self.assertTrue(has_closing_rule_for_now(self.company))
        with freeze_time("2016-02-22 10:00:00"):
            self.assertFalse(has_closing_rule_for_now(self.company))

    def test_get_closing_rule_for_now(self):
        with freeze_time("2015-12-26 10:00:00"):  # Holiday
            self.assertEqual(
                    get_closing_rule_for_now(self.company).first(),
                    ClosingRules.objects.filter(company=self.company).first()
            )
        with freeze_time("2016-02-22 10:00:00"):
            self.assertFalse(get_closing_rule_for_now(self.company))

    def test_opening_hours(self):
        with freeze_time("2016-02-22 08:00:00"):  # Monday
            opening_hours_str = opening_hours(self.company)
            self.assertIn(u'Monday', opening_hours_str)
            self.assertIn(u'Tuesday', opening_hours_str)
            self.assertIn(u'Wednesday', opening_hours_str)
            self.assertIn(u'Thursday', opening_hours_str)
            self.assertIn(u'Friday', opening_hours_str)
            self.assertIn(u'Saturday', opening_hours_str)
            self.assertIn(u'Sunday', opening_hours_str)
            self.assertIn(u'8:30am to 12:00pm', opening_hours_str)
            self.assertIn(u'9:00am to 5:00pm', opening_hours_str)
            self.assertIn(u'10:00am to 1:00pm', opening_hours_str)
            self.assertIn(u'12:30pm to 10:00pm', opening_hours_str)
            self.assertIn(u'12:30pm to 6:00pm', opening_hours_str)
            self.assertIn(u'6:30pm to 10:00pm', opening_hours_str)
            self.assertNotIn(u'2:30am to 4:00am', opening_hours_str)
