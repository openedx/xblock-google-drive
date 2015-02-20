""" Unit tests for google document components """
# -*- coding: utf-8 -*-
#

# Imports ###########################################################
import json
import unittest
from mock import Mock

from nose.tools import assert_equals, assert_in
from workbench.runtime import WorkbenchRuntime
from xblock.runtime import KvsFieldData, DictKeyValueStore

from google_drive import GoogleDocumentBlock
from google_drive.google_docs import DEFAULT_EMBED_CODE, DEFAULT_DOCUMENT_URL
from google_drive.tests.unit.test_utils import generate_scope_ids, make_request
from google_drive.tests.test_const import STUDIO_EDIT_WRAPPER, VALIDATION_WRAPPER, USER_INPUTS_WRAPPER, BUTTONS_WRAPPER
from google_drive.tests.test_const import RESULT_SUCCESS, RESULT_ERROR, RESULT_MISSING_EVENT_TYPE
from google_drive.tests.test_const import STATUS_CODE_200, STATUS_CODE_400, STATUS_CODE_404
from google_drive.tests.test_const import TEST_IMAGE_URL

# Constants ###########################################################
TEST_SUBMIT_DATA = {
    'display_name': "Google Document",
    'embed_code': "<iframe>",
    'alt_text': "This is alt text",
}
TEST_VALIDATE_URL_DATA = {
    'url': DEFAULT_DOCUMENT_URL,
}
TEST_VALIDATE_UNDEFINED_DATA = {
    'url': 'undefined'
}
TEST_VALIDATE_NONEXISTENT_URL_DATA = {
    'url': (
        "https://docs.google.com/presentation/d/1x2ZuzqHsMoh1epK8VsdsadfG"
        "AlanSo7r9z55ualwQlj-ofBQ/embed?start=true&loop=true&delayms=10000"
    )
}
TEST_COMPLETE_PUBLISH_DOCUMENT_DATA = {
    'url': DEFAULT_DOCUMENT_URL,
    'displayed_in': 'iframe',
    'event_type': 'edx.googlecomponent.document.displayed',
}
TEST_COMPLETE_PUBLISH_IMAGE_DATA = {
    'url': TEST_IMAGE_URL,
    'displayed_in': 'img',
    'event_type': 'edx.googlecomponent.document.displayed',
}
TEST_INCOMPLETE_PUBLISH_DATA = {
    'url': DEFAULT_DOCUMENT_URL,
    'displayed_in': 'iframe',
}


# Classes ###########################################################
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
        assert_in(DEFAULT_EMBED_CODE, student_fragment.content)

        studio_fragment = block.render('studio_view', Mock())
        assert_in(STUDIO_EDIT_WRAPPER, studio_fragment.content)
        assert_in(VALIDATION_WRAPPER, studio_fragment.content)
        assert_in(USER_INPUTS_WRAPPER, studio_fragment.content)
        assert_in(BUTTONS_WRAPPER, studio_fragment.content)

    def test_studio_document_submit(self):  # pylint: disable=no-self-use
        """ Test studio submission of GoogleDocumentBlock """
        block = TestGoogleDocumentBlock.make_document_block()

        body = json.dumps(TEST_SUBMIT_DATA)
        res = block.handle('studio_submit', make_request(body))
        # pylint: disable=no-value-for-parameter
        assert_equals(json.loads(res.body), RESULT_SUCCESS)

        assert_equals(block.display_name, TEST_SUBMIT_DATA['display_name'])
        assert_equals(block.embed_code, TEST_SUBMIT_DATA['embed_code'])
        assert_equals(block.alt_text, TEST_SUBMIT_DATA['alt_text'])

        body = json.dumps('')
        res = block.handle('studio_submit', make_request(body))
        assert_equals(json.loads(res.body), RESULT_ERROR)

    def test_check_document_url(self):  # pylint: disable=no-self-use
        """ Test verification of the provided Google Document URL"""
        block = TestGoogleDocumentBlock.make_document_block()

        data = json.dumps(TEST_VALIDATE_URL_DATA)
        res = block.handle('check_url', make_request(data))
        # pylint: disable=no-value-for-parameter
        assert_equals(json.loads(res.body), STATUS_CODE_200)

        data = json.dumps(TEST_VALIDATE_UNDEFINED_DATA)
        res = block.handle('check_url', make_request(data))

        assert_equals(json.loads(res.body), STATUS_CODE_400)

        data = json.dumps(TEST_VALIDATE_NONEXISTENT_URL_DATA)
        res = block.handle('check_url', make_request(data))

        assert_equals(json.loads(res.body), STATUS_CODE_404)

        data = json.dumps({})
        res = block.handle('check_url', make_request(data))

        assert_equals(json.loads(res.body), STATUS_CODE_400)

    def test_document_publish_event(self):  # pylint: disable=no-self-use
        """ Test event publishing in GoogleDocumentBlock"""
        block = TestGoogleDocumentBlock.make_document_block()

        body = json.dumps(TEST_COMPLETE_PUBLISH_DOCUMENT_DATA)
        res = block.handle('publish_event', make_request(body))
        # pylint: disable=no-value-for-parameter
        assert_equals(json.loads(res.body), RESULT_SUCCESS)

        body = json.dumps(TEST_COMPLETE_PUBLISH_IMAGE_DATA)
        res = block.handle('publish_event', make_request(body))

        assert_equals(json.loads(res.body), RESULT_SUCCESS)

        body = json.dumps(TEST_INCOMPLETE_PUBLISH_DATA)
        res = block.handle('publish_event', make_request(body))

        assert_equals(json.loads(res.body), RESULT_MISSING_EVENT_TYPE)
