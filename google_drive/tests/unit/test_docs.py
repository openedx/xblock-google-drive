import json

from webob import Request
from mock import Mock

from workbench.runtime import WorkbenchRuntime
from xblock.runtime import KvsFieldData, DictKeyValueStore

from google_drive import GoogleDocumentBlock, GoogleCalendarBlock

from nose.tools import (
    assert_equals
)

def make_request(body, method='POST'):
    request = Request.blank('/')
    request.method = 'POST'
    request.body = body.encode('utf-8')
    request.method = method
    return request

def make_document_block():
    runtime = WorkbenchRuntime()
    key_store = DictKeyValueStore()
    db_model = KvsFieldData(key_store)
    return GoogleDocumentBlock(runtime, db_model, Mock())

def make_calendar_block():
    runtime = WorkbenchRuntime()
    key_store = DictKeyValueStore()
    db_model = KvsFieldData(key_store)
    return GoogleCalendarBlock(runtime, db_model, Mock())

def test_studio_document_submit():
    block = make_document_block()

    body = json.dumps({
        'display_name': "Google Document",
        'embed_code': "<iframe>"
    })
    res = block.handle('studio_submit', make_request(body))

    assert_equals(json.loads(res.body), {'result': 'success'})

    assert_equals(block.display_name, "Google Document")
    assert_equals(block.embed_code, "<iframe>")

def test_calendar_document_submit():
    block = make_calendar_block()

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
