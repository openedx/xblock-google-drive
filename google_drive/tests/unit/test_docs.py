""" Tests for google drive components """
import json
import unittest

from webob import Request
from mock import Mock

from workbench.runtime import WorkbenchRuntime
from xblock.runtime import KvsFieldData, DictKeyValueStore
from xblock.fields import ScopeIds

from google_drive import GoogleDocumentBlock, GoogleCalendarBlock

from nose.tools import assert_equals, assert_in


def generate_scope_ids(runtime, block_type):
    """ helper to generate scope IDs for an XBlock """
    def_id = runtime.id_generator.create_definition(block_type)
    usage_id = runtime.id_generator.create_usage(def_id)
    return ScopeIds('user', block_type, def_id, usage_id)


def make_request(body, method='POST'):
    """ helper to make a request """
    request = Request.blank('/')
    request.method = 'POST'
    request.body = body.encode('utf-8')
    request.method = method
    return request


class TestGoogleDocumentBlock(unittest.TestCase):
    """ Tests for GoogleDocumentBlock """

    @classmethod
    def make_document_block(cls):
        """ helper to construct a GoogleDocumentBlock """
        runtime = WorkbenchRuntime()
        key_store = DictKeyValueStore()
        db_model = KvsFieldData(key_store)
        ids = generate_scope_ids(runtime, 'google_document')
        return GoogleDocumentBlock(runtime, db_model, scope_ids=ids)

    def test_document_templates_contents(self):
        """ Test content of GoogleDocumentBlock's rendered views """
        block = TestGoogleDocumentBlock.make_document_block()
        block.usage_id = Mock()

        student_fragment = block.render('student_view', Mock())
        assert_in('<div class="google-docs-xblock-wrapper"', student_fragment.content)
        assert_in('Google Document', student_fragment.content)
        assert_in(
            (
                'https://docs.google.com/presentation/d/1x2ZuzqHsMoh1epK8VsGAlanSo7r9z55ualwQlj-ofBQ'
                '/embed?start=true&loop'
                '=true&delayms=10000"\n    frameborder="0"\n    width="960"\n    height="569"\n    '
                'allowfullscreen="true"'
            ),
            student_fragment.content
        )

        studio_fragment = block.render('studio_view', Mock())
        assert_in(
            '<div class="wrapper-comp-settings is-active editor-with-buttons google-edit-wrapper" id="settings-tab">',
            studio_fragment.content
        )
        assert_in('<div class="user-inputs-and-validation">', studio_fragment.content)
        assert_in('<div class="xblock-inputs editor_content_wrapper">', studio_fragment.content)
        assert_in('<div class="xblock-actions">', studio_fragment.content)

    def test_studio_document_submit(self):
        """ Test studio submission of GoogleDocumentBlock """
        block = TestGoogleDocumentBlock.make_document_block()

        body = json.dumps({
            'display_name': "Google Document",
            'embed_code': "<iframe>",
            'alt_text': "This is alt text",
        })
        res = block.handle('studio_submit', make_request(body))

        assert_equals(json.loads(res.body), {'result': 'success'})

        assert_equals(block.display_name, "Google Document")
        assert_equals(block.embed_code, "<iframe>")
        assert_equals(block.alt_text, "This is alt text")

    def test_check_document_url(self):
        """ Test verification of the provided Google Document URL"""
        block = TestGoogleDocumentBlock.make_document_block()

        data = json.dumps({
            'url': (
                "https://docs.google.com/presentation/d/1x2ZuzqHsMoh1epK8VsGAl"
                "anSo7r9z55ualwQlj-ofBQ/embed?start=true&loop=true&delayms=10000"
            )
        })
        res = block.handle('check_url', make_request(data))

        assert_equals(json.loads(res.body), {'status_code': 200})

        data = json.dumps({
            'url': 'undefined'
        })
        res = block.handle('check_url', make_request(data))

        assert_equals(json.loads(res.body), {'status_code': 400})

        data = json.dumps({
            'url': (
                "https://docs.google.com/presentation/d/1x2ZuzqHsMoh1epK8VsdsadfG"
                "AlanSo7r9z55ualwQlj-ofBQ/embed?start=true&loop=true&delayms=10000"
            )
        })
        res = block.handle('check_url', make_request(data))

        assert_equals(json.loads(res.body), {'status_code': 404})

    def test_document_publish_event(self):
        """ Test event publishing in GoogleDocumentBlock"""
        block = TestGoogleDocumentBlock.make_document_block()

        body = json.dumps({
            'url': (
                'https://docs.google.com/presentation/d/1x2ZuzqHsMoh1epK8VsdsadfGAlanSo7r9z55ualwQlj-ofBQ/embed'
                '?start=true&loop=true&delayms=10000'
            ),
            'displayed_in': 'iframe',
            'event_type': 'edx.googlecomponent.document.displayed',
        })
        res = block.handle('publish_event', make_request(body))

        assert_equals(json.loads(res.body), {'result': 'success'})

        body = json.dumps({
            'url': (
                'https://docs.google.com/drawings/d/1LHGzCTLRb--CDvFFjoYp62TiIN5KgsE7QOy9Sift_eg/'
                'pub?w=882&amp;h=657'),
            'displayed_in': 'img',
            'event_type': 'edx.googlecomponent.document.displayed',
        })
        res = block.handle('publish_event', make_request(body))

        assert_equals(json.loads(res.body), {'result': 'success'})

        body = json.dumps({
            'url': (
                'https://docs.google.com/presentation/d/1x2ZuzqHsMoh1epK8VsdsadfGAlanSo7r9z55ualwQlj-ofBQ/embed'
                '?start=true&loop=true&delayms=10000'
            ),
            'displayed_in': 'iframe',
        })
        res = block.handle('publish_event', make_request(body))

        assert_equals(json.loads(res.body), {'result': 'error', 'message': 'Missing event_type in JSON data'})


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

    def test_calendar_templates_contents(self):
        """ Test content of GoogleCalendarBlock's rendered views """
        block = TestGoogleCalendarBlock.make_calendar_block()
        block.usage_id = Mock()

        student_fragment = block.render('student_view', Mock())
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
            '<div class="wrapper-comp-settings is-active editor-with-buttons google-edit-wrapper" id="settings-tab">',
            studio_fragment.content
        )
        assert_in('<div class="user-inputs-and-validation">', studio_fragment.content)
        assert_in('<div class="xblock-inputs editor_content_wrapper">', studio_fragment.content)
        assert_in('<div class="xblock-actions">', studio_fragment.content)

    def test_calendar_document_submit(self):
        """ Test studio submission of GoogleCalendarBlock """
        block = TestGoogleCalendarBlock.make_calendar_block()

        body = json.dumps({
            'display_name': "Google Calendar",
            'calendar_id': "google1234",
            'default_view': 1
        })
        res = block.handle('studio_submit', make_request(body))

        assert_equals(json.loads(res.body), {'result': 'success'})

        assert_equals(block.display_name, "Google Calendar")
        assert_equals(block.calendar_id, "google1234")
        assert_equals(block.default_view, 1)

    def test_calendar_publish_event(self):
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
