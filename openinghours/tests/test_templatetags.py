from freezegun import freeze_time

from django.utils.translation import ugettext_lazy as _

from openinghours.templatetags.openinghours_tags import iso_day_to_weekday
from openinghours.tests.tests import OpeningHoursTestCase


class TemplatetagsTestCase(OpeningHoursTestCase):

    def setUp(self):
        super(TemplatetagsTestCase, self).setUp()

    def tearDown(self):
        super(TemplatetagsTestCase, self).tearDown()

    def test_iso_day_to_weekday(self):
        with freeze_time("2016-02-22"):  # Monday
            self.assertEqual(iso_day_to_weekday(1).encode('utf-8'), str('today'))
            self.assertNotEqual(iso_day_to_weekday(2).encode('utf-8'), str('today'))
        with freeze_time("2016-02-23"):  # Tuesday
            self.assertNotEqual(iso_day_to_weekday(1).encode('utf-8'), str('today'))
            self.assertEqual(iso_day_to_weekday(2).encode('utf-8'), str('today'))

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

