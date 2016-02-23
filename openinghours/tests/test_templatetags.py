from django.utils.encoding import force_text
from freezegun import freeze_time

from openinghours.templatetags.openinghours_tags import iso_day_to_weekday
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
        pass

    def test_is_open(self):
        pass

    def test_next_time_open(self):
        pass

    def test_has_closing_rule_for_now(self):
        pass

    def test_get_closing_rule_for_now(self):
        pass

    def opening_hours(self):
        pass

