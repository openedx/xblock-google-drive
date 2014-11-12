import json

from webob import Request
from mock import Mock

from workbench.runtime import WorkbenchRuntime
from xblock.runtime import KvsFieldData, DictKeyValueStore

from google_drive import GoogleDocumentBlock

from nose.tools import (
    assert_equals, assert_true, assert_false,
    assert_in
)

def make_request(body, method='POST'):
    request = Request.blank('/')
    request.method = 'POST'
    request.body = body.encode('utf-8')
    request.method = method
    return request

def make_block():
    runtime = WorkbenchRuntime()
    key_store = DictKeyValueStore()
    db_model = KvsFieldData(key_store)
    return GoogleDocumentBlock(runtime, db_model, Mock())

def test_studio_submit():
    block = make_block()

    body = json.dumps({
        'display_name': "Google Document",
        'embed_code': "<iframe>"
    })
    res = block.handle('studio_submit', make_request(body))

    assert_equals(json.loads(res.body), {'result': 'success'})

    assert_equals(block.display_name, "Google Document")
    assert_equals(block.embed_code, "<iframe>")
