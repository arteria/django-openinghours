from freezegun import freeze_time

from openinghours.tests.tests import OpeningHoursTestCase


class FormsTestCase(OpeningHoursTestCase):

    def setUp(self):
        super(FormsTestCase, self).setUp()

    def tearDown(self):
        super(FormsTestCase, self).tearDown()

    def test_hours_are_published(self):
        response = self.client.get('/')
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
        post = self.client.post('/edit/1', post_data)
        resp = self.client.get('/edit/1')
        self.assertContains(resp, '<option value="11:30" selected', count=6)
        self.assertContains(resp, '<option value="17:30" selected', count=5)
        self.assertContains(resp, '<option value="00:00">', count=7*2*2)
        resp2 = self.client.get('/')
        self.assertContains(resp2, '11:30am')
        self.assertContains(resp2, '5:30pm')
