""" Unit tests for google document components """
import json
import unittest
from mock import Mock

from nose.tools import assert_equals, assert_in
from workbench.runtime import WorkbenchRuntime
from xblock.runtime import KvsFieldData, DictKeyValueStore

from google_drive import GoogleCalendarBlock
from google_drive.tests.unit.test_utils import generate_scope_ids, make_request


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
        assert_in(
            (
                'https://www.google.com/calendar/embed?mode=Month&amp;src=edx.org_lom804qe3ttspplj1bgeu1l3ak'
                '@group.calendar.google.com&amp;showCalendars=0'
            ),
            student_fragment.content
        )
        assert_in('Google Calendar', student_fragment.content)

        studio_fragment = block.render('studio_view', Mock())
        assert_in(
            (
                '<div class="wrapper-comp-settings is-active editor-with-buttons google-edit-wrapper" '
                'id="calendar-settings-tab">'
            ),
            studio_fragment.content
        )
        assert_in('<div class="user-inputs-and-validation">', studio_fragment.content)
        assert_in('<div class="xblock-inputs editor_content_wrapper">', studio_fragment.content)
        assert_in('<div class="xblock-actions">', studio_fragment.content)

    def test_calendar_document_submit(self):  # pylint: disable=no-self-use
        """ Test studio submission of GoogleCalendarBlock """
        block = TestGoogleCalendarBlock.make_calendar_block()

        body = json.dumps({
            'display_name': "Google Calendar",
            'calendar_id': "google1234",
            'default_view': 1
        })
        res = block.handle('studio_submit', make_request(body))
        # pylint: disable=no-value-for-parameter
        assert_equals(json.loads(res.body), {'result': 'success'})

        assert_equals(block.display_name, "Google Calendar")
        assert_equals(block.calendar_id, "google1234")
        assert_equals(block.default_view, 1)

    def test_calendar_publish_event(self):  # pylint: disable=no-self-use
        """ Test event publishing in GoogleCalendarBlock"""
        block = TestGoogleCalendarBlock.make_calendar_block()

        body = json.dumps({
            'url': (
                'https://www.google.com/calendar/embed?mode=Month&src=edx.org_lom804qe3ttspplj1bgeu1l3ak'
                '@group.calendar.google.com&showCalendars=0'
            ),
            'displayed_in': 'iframe',
            'event_type': 'edx.googlecomponent.calendar.displayed'
        })
        res = block.handle('publish_event', make_request(body))
        # pylint: disable=no-value-for-parameter
        assert_equals(json.loads(res.body), {'result': 'success'})

        body = json.dumps({
            'url': (
                'https://www.google.com/calendar/embed?mode=Month&src=edx.org_lom804qe3ttspplj1bgeu1l3ak'
                '@group.calendar.google.com&showCalendars=0'
            ),
            'displayed_in': 'iframe',
        })
        res = block.handle('publish_event', make_request(body))

        assert_equals(json.loads(res.body), {'result': 'error', 'message': 'Missing event_type in JSON data'})
