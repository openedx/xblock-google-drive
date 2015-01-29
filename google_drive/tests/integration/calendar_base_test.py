""" Google Calendar integration tests """
from xblockutils.base_test import SeleniumBaseTest


class GoogleCalendarBaseTest(SeleniumBaseTest):
    """ Test class for google calendar """
    module_name = __name__
    default_css_selector = 'div.google-calendar-xblock-wrapper'

    def test_calendar_publish_event(self):
        calendar = self.go_to_page('Calendar')
        load_event_complete = calendar.find_element_by_css_selector('.load_event_complete')
        self.assertEqual(
            load_event_complete.get_attribute('value'),
            "I've published the event that indicates that the load has completed"
        )
