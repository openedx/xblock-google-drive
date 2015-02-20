""" Runs tests for the studio views """
# -*- coding: utf-8 -*-
#

# Imports ###########################################################
from ddt import ddt, unpack, data
from .base_test import GoogleCalendarBaseTest, GoogleDocumentBaseTest
from .studio_scenarios import CALENDAR_SCENARIOS, DOCUMENT_SCENARIOS, IMAGE_SCENARIOS
from google_drive.google_calendar import DEFAULT_CALENDAR_URL
from google_drive.google_docs import DEFAULT_DOCUMENT_URL
from google_drive.tests.test_const import TEST_IMAGE_URL


# Classes ###########################################################
@ddt  # pylint: disable=too-many-ancestors
class GoogleCalendarStudioTest(GoogleCalendarBaseTest):
    """
    Tests for Google Calendar studio view.
    """
    default_css_selector = '#calendar-settings-tab'

    def studio_save(self):
        """ Save changes made in studio for Google Calendar """
        self.browser.find_element_by_css_selector('#calendar-submit-options').click()

    @data(*CALENDAR_SCENARIOS)  # pylint: disable=star-args
    @unpack
    def test_save_calendar(self, page_name):
        """
        Verify that option changes in Google Calendar studio view
        are appropriately saved and visible immediately after
        """
        self.go_to_page(page_name, view_name='studio_view')
        # Expecting every input value to be valid
        self.assertTrue(self.browser.find_element_by_css_selector('.validation_alert.covered'))
        display_name_input = self.browser.find_element_by_css_selector('#edit_display_name')
        # Change display name
        display_name_input.clear()
        display_name_input.send_keys('My Meetings')
        calendar_id_input = self.browser.find_element_by_css_selector('#edit_calendar_id')
        # Change calendar ID
        calendar_id_input.clear()
        calendar_id_input.send_keys('a')
        self.wait_until_exists('#edit_calendar_id.error')
        # Expects validation error due to calendar ID being invalid
        self.assertTrue(self.browser.find_element_by_css_selector('.validation_alert:not(covered)'))
        # Check to see that calendar ID input element is marked as invalid
        self.assertTrue(self.browser.find_element_by_css_selector('#edit_calendar_id.error'))
        # Save button should be disabled
        self.assertTrue(self.browser.find_element_by_css_selector('#calendar-submit-options.disabled'))
        clean_calendar_id_button = self.browser.find_element_by_css_selector('button.clear-calendar-id')
        # Reset calendar ID value to default one
        clean_calendar_id_button.click()
        # Expecting every input value to be valid again
        self.assertTrue(self.browser.find_element_by_css_selector('.validation_alert.covered'))

        self.studio_save()
        self.go_to_page(page_name, css_selector='div.google-calendar-xblock-wrapper')
        calendar_iframe = self.browser.find_element_by_css_selector('iframe')
        # Expecting that default calendar is the one loaded in the IFrame
        self.assertEqual(calendar_iframe.get_attribute("src"), DEFAULT_CALENDAR_URL)
        # Expecting that the new display name is the title of the IFrame
        self.assertEqual(calendar_iframe.get_attribute("title"), 'My Meetings')


@ddt  # pylint: disable=too-many-ancestors
class GoogleDocumentStudioTest(GoogleDocumentBaseTest):
    """
    Tests for Google Document studio view.
    """
    default_css_selector = '#document-settings-tab'

    def studio_save(self):
        """ Save changes made in studio for Google Document """
        self.browser.find_element_by_css_selector('#document-submit-options').click()

    @data(*DOCUMENT_SCENARIOS)  # pylint: disable=star-args
    @unpack
    def test_save_document(self, page_name):
        """
        Verify that option changes in Google Document studio view
        are appropriately saved and visible immediately after
        """
        self.go_to_page(page_name, view_name='studio_view')
        # Expecting every input value to be valid
        self.assertTrue(self.browser.find_element_by_css_selector('.validation_alert.covered'))
        display_name_input = self.browser.find_element_by_css_selector('#edit_display_name')
        # Change display name
        display_name_input.clear()
        display_name_input.send_keys('My Document')
        # Expecting list item that contains input element for alternative text to be hidden
        self.assertTrue(self.browser.find_element_by_css_selector('li#alt_text_item.covered'))

        self.studio_save()
        self.go_to_page(page_name, css_selector='div.google-docs-xblock-wrapper')
        document_iframe = self.browser.find_element_by_css_selector('iframe')
        # Expecting that default calendar is the one loaded in the IFrame
        self.assertEqual(document_iframe.get_attribute("src"), DEFAULT_DOCUMENT_URL)
        # Expecting that the new display name is the title of the IFrame
        self.assertEqual(document_iframe.get_attribute("title"), 'My Document')

    @data(*IMAGE_SCENARIOS)  # pylint: disable=star-args
    @unpack
    def test_save_image(self, page_name):
        """
        Verify that option changes in Google Image studio view
        are appropriately saved and visible immediately after
        """
        self.go_to_page(page_name, view_name='studio_view')
        # Expecting every input value to be valid
        self.assertTrue(self.browser.find_element_by_css_selector('.validation_alert.covered'))
        display_name_input = self.browser.find_element_by_css_selector('#edit_display_name')
        # Change display name
        display_name_input.clear()
        display_name_input.send_keys('My Image')
        # Expecting list item that contains input element for alternative text to be shown
        self.assertTrue(self.browser.find_element_by_css_selector('li#alt_text_item:not(covered)'))
        alt_text_input = self.browser.find_element_by_css_selector('#edit_alt_text')
        # Add alternative text for image
        alt_text_input.send_keys('Alternative text for my image')

        self.studio_save()
        self.go_to_page(page_name, css_selector='div.google-docs-xblock-wrapper')
        image_iframe = self.browser.find_element_by_css_selector('img')
        # Expecting that default calendar is the one loaded in the IFrame
        self.assertEqual(image_iframe.get_attribute("src"), TEST_IMAGE_URL)
        # Expecting that the new display name is the title of the IFrame
        self.assertEqual(image_iframe.get_attribute("alt"), 'Alternative text for my image')
