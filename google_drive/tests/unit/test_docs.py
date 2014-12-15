import json

from webob import Request
from mock import Mock

from workbench.runtime import WorkbenchRuntime
from xblock.runtime import KvsFieldData, DictKeyValueStore

from google_drive import GoogleDocumentBlock, GoogleCalendarBlock

from nose.tools import (
    assert_equals, assert_in
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

def test_document_templates_contents():
    block = make_document_block()

    student_fragment = block.render('student_view', Mock())
    assert_in('<div class="google-docs-xblock-wrapper"', student_fragment.content)
    assert_in('&#39;self.display_name&#39;', student_fragment.content)
    assert_in('&#39;self.embed_code&#39;', student_fragment.content)

    studio_fragment = block.render('studio_view', Mock())
    assert_in('<div class="wrapper-comp-settings is-active editor-with-buttons google-edit-wrapper" id="settings-tab">', studio_fragment.content)
    assert_in('<div class="user-inputs-and-validation">', studio_fragment.content)
    assert_in('<div class="xblock-inputs editor_content_wrapper">', studio_fragment.content)
    assert_in('<div class="xblock-actions">', studio_fragment.content)

def test_calendar_templates_contents():
    block = make_calendar_block()

    student_fragment = block.render('student_view', Mock())
    assert_in('<div class="google-calendar-xblock-wrapper">', student_fragment.content)
    assert_in('&#39;iframe&#39;', student_fragment.content)

    studio_fragment = block.render('studio_view', Mock())
    assert_in('<div class="wrapper-comp-settings is-active editor-with-buttons google-edit-wrapper" id="settings-tab">', studio_fragment.content)
    assert_in('<div class="user-inputs-and-validation">', studio_fragment.content)
    assert_in('<div class="xblock-inputs editor_content_wrapper">', studio_fragment.content)
    assert_in('<div class="xblock-actions">', studio_fragment.content)

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

def test_check_document_url():
    block = make_document_block()

    data = json.dumps({
        'url': "https://docs.google.com/presentation/d/1x2ZuzqHsMoh1epK8VsGAlanSo7r9z55ualwQlj-ofBQ/embed?start=true&loop=true&delayms=10000"
    })
    res = block.handle('check_url', make_request(data))

    assert_equals(json.loads(res.body), {'status_code': 200})

    data = json.dumps({
        'url': 'undefined'
    })
    res = block.handle('check_url', make_request(data))

    assert_equals(json.loads(res.body), {'status_code': 400})

    data = json.dumps({
        'url': "https://docs.google.com/presentation/d/1x2ZuzqHsMoh1epK8VsdsadfGAlanSo7r9z55ualwQlj-ofBQ/embed?start=true&loop=true&delayms=10000"
    })
    res = block.handle('check_url', make_request(data))

    assert_equals(json.loads(res.body), {'status_code': 404})


