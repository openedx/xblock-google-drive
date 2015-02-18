""" Unit tests for google document components """
import json
import unittest
from mock import Mock

from nose.tools import assert_equals, assert_in
from workbench.runtime import WorkbenchRuntime
from xblock.runtime import KvsFieldData, DictKeyValueStore

from google_drive import GoogleDocumentBlock
from google_drive.tests.unit.test_utils import generate_scope_ids, make_request


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

    def test_document_template_content(self):  # pylint: disable=no-self-use
        """ Test content of GoogleDocumentBlock's rendered views """
        block = TestGoogleDocumentBlock.make_document_block()
        block.usage_id = Mock()

        student_fragment = block.render('student_view', Mock())
        # pylint: disable=no-value-for-parameter
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
            (
                '<div class="wrapper-comp-settings is-active editor-with-buttons google-edit-wrapper" '
                'id="document-settings-tab">'
            ),
            studio_fragment.content
        )
        assert_in('<div class="user-inputs-and-validation">', studio_fragment.content)
        assert_in('<div class="xblock-inputs editor_content_wrapper">', studio_fragment.content)
        assert_in('<div class="xblock-actions">', studio_fragment.content)

    def test_studio_document_submit(self):  # pylint: disable=no-self-use
        """ Test studio submission of GoogleDocumentBlock """
        block = TestGoogleDocumentBlock.make_document_block()

        body = json.dumps({
            'display_name': "Google Document",
            'embed_code': "<iframe>",
            'alt_text': "This is alt text",
        })
        res = block.handle('studio_submit', make_request(body))
        # pylint: disable=no-value-for-parameter
        assert_equals(json.loads(res.body), {'result': 'success'})

        assert_equals(block.display_name, "Google Document")
        assert_equals(block.embed_code, "<iframe>")
        assert_equals(block.alt_text, "This is alt text")

    def test_check_document_url(self):  # pylint: disable=no-self-use
        """ Test verification of the provided Google Document URL"""
        block = TestGoogleDocumentBlock.make_document_block()

        data = json.dumps({
            'url': (
                "https://docs.google.com/presentation/d/1x2ZuzqHsMoh1epK8VsGAl"
                "anSo7r9z55ualwQlj-ofBQ/embed?start=true&loop=true&delayms=10000"
            )
        })
        res = block.handle('check_url', make_request(data))
        # pylint: disable=no-value-for-parameter
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

        data = json.dumps({})
        res = block.handle('check_url', make_request(data))

        assert_equals(json.loads(res.body), {'status_code': 400})

    def test_document_publish_event(self):  # pylint: disable=no-self-use
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
        # pylint: disable=no-value-for-parameter
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
