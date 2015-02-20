""" Unit tests for google calendar components """
# -*- coding: utf-8 -*-
#

# Imports ###########################################################
import json
import unittest
import cgi
from mock import Mock

from nose.tools import assert_equals, assert_in
from workbench.runtime import WorkbenchRuntime
from xblock.runtime import KvsFieldData, DictKeyValueStore

from google_drive import GoogleCalendarBlock
from google_drive.google_calendar import DEFAULT_CALENDAR_URL
from google_drive.tests.unit.test_utils import generate_scope_ids, make_request
from google_drive.tests.test_const import STUDIO_EDIT_WRAPPER, VALIDATION_WRAPPER, USER_INPUTS_WRAPPER, BUTTONS_WRAPPER
from google_drive.tests.test_const import RESULT_SUCCESS, RESULT_ERROR, RESULT_MISSING_EVENT_TYPE

# Constants ###########################################################
TEST_SUBMIT_DATA = {
    'display_name': "Google Calendar",
    'calendar_id': "google1234",
    'default_view': 1
}
TEST_COMPLETE_PUBLISH_DATA = {
    'url': (
        'https://www.google.com/calendar/embed?mode=Month&src=edx.org_lom804qe3ttspplj1bgeu1l3ak'
        '@group.calendar.google.com&showCalendars=0'
    ),
    'displayed_in': 'iframe',
    'event_type': 'edx.googlecomponent.calendar.displayed'
}
TEST_INCOMPLETE_PUBLISH_DATA = {
    'url': (
        'https://www.google.com/calendar/embed?mode=Month&src=edx.org_lom804qe3ttspplj1bgeu1l3ak'
        '@group.calendar.google.com&showCalendars=0'
    ),
    'displayed_in': 'iframe'
}


# Classes ###########################################################
class TestGoogleCalendarBlock(unittest.TestCase):
    """ Tests for GoogleCalendarBlock """

    @classmethod
    def make_calendar_block(cls):
        """ helper to construct a GoogleCalendarBlock """
        runtime = WorkbenchRuntime()
        key_store = DictKeyValueStore()
        db_model = KvsFieldData(key_store)
        ids = generate_scope_ids(runtime, 'google_calendar')
        return GoogleCalendarBlock(runtime, db_model, scope_ids=ids)

    def test_calendar_template_content(self):  # pylint: disable=no-self-use
        """ Test content of GoogleCalendarBlock's rendered views """
        block = TestGoogleCalendarBlock.make_calendar_block()
        block.usage_id = Mock()

        student_fragment = block.render('student_view', Mock())
        # pylint: disable=no-value-for-parameter
        assert_in('<div class="google-calendar-xblock-wrapper">', student_fragment.content)
        assert_in(cgi.escape(DEFAULT_CALENDAR_URL), student_fragment.content)
        assert_in('Google Calendar', student_fragment.content)

        studio_fragment = block.render('studio_view', Mock())
        assert_in(STUDIO_EDIT_WRAPPER, studio_fragment.content)
        assert_in(VALIDATION_WRAPPER, studio_fragment.content)
        assert_in(USER_INPUTS_WRAPPER, studio_fragment.content)
        assert_in(BUTTONS_WRAPPER, studio_fragment.content)

    def test_calendar_document_submit(self):  # pylint: disable=no-self-use
        """ Test studio submission of GoogleCalendarBlock """
        block = TestGoogleCalendarBlock.make_calendar_block()

        body = json.dumps(TEST_SUBMIT_DATA)
        res = block.handle('studio_submit', make_request(body))
        # pylint: disable=no-value-for-parameter
        assert_equals(json.loads(res.body), RESULT_SUCCESS)

        assert_equals(block.display_name, TEST_SUBMIT_DATA['display_name'])
        assert_equals(block.calendar_id, TEST_SUBMIT_DATA['calendar_id'])
        assert_equals(block.default_view, TEST_SUBMIT_DATA['default_view'])

        body = json.dumps('')
        res = block.handle('studio_submit', make_request(body))
        # pylint: disable=no-value-for-parameter
        assert_equals(json.loads(res.body), RESULT_ERROR)

    def test_calendar_publish_event(self):  # pylint: disable=no-self-use
        """ Test event publishing in GoogleCalendarBlock"""
        block = TestGoogleCalendarBlock.make_calendar_block()

        body = json.dumps(TEST_COMPLETE_PUBLISH_DATA)
        res = block.handle('publish_event', make_request(body))
        # pylint: disable=no-value-for-parameter
        assert_equals(json.loads(res.body), RESULT_SUCCESS)

        body = json.dumps(TEST_INCOMPLETE_PUBLISH_DATA)
        res = block.handle('publish_event', make_request(body))

        assert_equals(json.loads(res.body), RESULT_MISSING_EVENT_TYPE)
