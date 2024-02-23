""" Unit tests for google calendar components """
# -*- coding: utf-8 -*-
#

from __future__ import absolute_import
# Imports ###########################################################
import json
import unittest

import ddt
from django.utils.html import escape
from django.utils.translation import override as override_language
from mock import Mock
from nose.tools import assert_equal, assert_in
from workbench.runtime import WorkbenchRuntime
from xblock.runtime import DictKeyValueStore, KvsFieldData

from google_drive import GoogleCalendarBlock
from google_drive.google_calendar import DEFAULT_CALENDAR_ID
from google_drive.tests.test_const import (
    BUTTONS_WRAPPER,
    RESULT_ERROR,
    RESULT_MISSING_EVENT_TYPE,
    RESULT_SUCCESS,
    STUDIO_EDIT_WRAPPER,
    USER_INPUTS_WRAPPER,
    VALIDATION_WRAPPER
)
from google_drive.tests.unit.test_utils import generate_scope_ids, make_request

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

CALENDAR_LANGUAGES = [
    {
        'override': False,
        'activate_lang': None,
        'expected_lang': 'en-us',
    }, {
        'override': True,
        'activate_lang': 'en',
        'expected_lang': 'en',
    }, {
        'override': True,
        'activate_lang': 'eo',
        'expected_lang': 'eo',
    }, {
        'override': True,
        'activate_lang': 'jp-ja',
        'expected_lang': 'jp-ja',
    }
]


# Classes ###########################################################
@ddt.ddt
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

    def _render_calendar_block(self):
        block = TestGoogleCalendarBlock.make_calendar_block()
        block.usage_id = Mock()
        student_fragment = block.render('student_view', Mock())
        studio_fragment = block.render('studio_view', Mock())
        return block, student_fragment, studio_fragment

    @ddt.data(*CALENDAR_LANGUAGES)
    @ddt.unpack
    def test_calendar_template_content(self, override, activate_lang, expected_lang):
        """ Test content of GoogleCalendarBlock's rendered views """
        # pylint: disable=no-value-for-parameter
        if override:
            with override_language(activate_lang):
                _block, student_fragment, studio_fragment = self._render_calendar_block()
        else:
            _block, student_fragment, studio_fragment = self._render_calendar_block()

        src_url = (f'https://www.google.com/calendar/embed?mode=Month&src'
                   f'={DEFAULT_CALENDAR_ID}&showCalendars=0&hl={expected_lang}')

        assert_in('<div class="google-calendar-xblock-wrapper">', student_fragment.content)
        assert_in(escape(src_url), student_fragment.content)
        assert_in('Google Calendar', student_fragment.content)

        assert_in(STUDIO_EDIT_WRAPPER, studio_fragment.content)
        assert_in(VALIDATION_WRAPPER, studio_fragment.content)
        assert_in(USER_INPUTS_WRAPPER, studio_fragment.content)
        assert_in(BUTTONS_WRAPPER, studio_fragment.content)

    def test_calendar_document_submit(self):
        """ Test studio submission of GoogleCalendarBlock """
        block = TestGoogleCalendarBlock.make_calendar_block()

        body = json.dumps(TEST_SUBMIT_DATA)
        res = block.handle('studio_submit', make_request(body))
        # pylint: disable=no-value-for-parameter
        assert_equal(json.loads(res.body.decode('utf8')), RESULT_SUCCESS)

        assert_equal(block.display_name, TEST_SUBMIT_DATA['display_name'])
        assert_equal(block.calendar_id, TEST_SUBMIT_DATA['calendar_id'])
        assert_equal(block.default_view, TEST_SUBMIT_DATA['default_view'])

        body = json.dumps('')
        res = block.handle('studio_submit', make_request(body))
        # pylint: disable=no-value-for-parameter
        assert_equal(json.loads(res.body.decode('utf8')), RESULT_ERROR)

    def test_calendar_publish_event(self):
        """ Test event publishing in GoogleCalendarBlock"""
        block = TestGoogleCalendarBlock.make_calendar_block()

        body = json.dumps(TEST_COMPLETE_PUBLISH_DATA)
        res = block.handle('publish_event', make_request(body))
        # pylint: disable=no-value-for-parameter
        assert_equal(json.loads(res.body.decode('utf8')), RESULT_SUCCESS)

        body = json.dumps(TEST_INCOMPLETE_PUBLISH_DATA)
        res = block.handle('publish_event', make_request(body))

        assert_equal(json.loads(res.body.decode('utf8')), RESULT_MISSING_EVENT_TYPE)
