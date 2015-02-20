""" Runs tests for publish event functionality """
# -*- coding: utf-8 -*-
#

# Imports ###########################################################
from .base_test import GoogleCalendarBaseTest, GoogleDocumentBaseTest


# Classes ###########################################################
class GoogleCalendarPublishTestCase(GoogleCalendarBaseTest):  # pylint: disable=too-few-public-methods, too-many-ancestors
    """
    Tests for Google Calendar event publishing functionality.
    """

    def test_calendar_publish_event(self):
        """ Tests whether the publish event for calendar was triggered """
        calendar = self.go_to_page('Calendar')
        load_event_complete = calendar.find_element_by_css_selector('.load_event_complete')
        self.assertEqual(
            load_event_complete.get_attribute('value'),
            "I've published the event that indicates that the load has completed"
        )


class GoogleDocumentPublishTestCase(GoogleDocumentBaseTest):  # pylint: disable=too-many-ancestors
    """
    Tests for Google Document event publishing functionality.
    """

    def test_document_publish_event(self):
        """ Tests whether the publish event for document was triggered """
        document = self.go_to_page('Document')
        load_event_complete = document.find_element_by_css_selector('.load_event_complete')
        self.assertEqual(
            load_event_complete.get_attribute('value'),
            "I've published the event that indicates that the load has completed"
        )

    def test_image_publish_event(self):
        """ Tests whether the publish event for image was triggered """
        image = self.go_to_page('Image')
        load_event_complete = image.find_element_by_css_selector('.load_event_complete')
        self.assertEqual(
            load_event_complete.get_attribute('value'),
            "I've published the event that indicates that the load has completed"
        )
