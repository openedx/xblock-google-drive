# -*- coding: utf-8 -*-
#

# Imports ###########################################################

import pkg_resources
#import logging
import textwrap
#import json
#import webob
#from lxml import etree
#from xml.etree import ElementTree as ET
import requests

from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment

# from StringIO import StringIO

from .utils import render_template, AttrDict, load_resource


# Globals ###########################################################

#log = logging.getLogger(__name__)


# Classes ###########################################################

class GoogleDocumentBlock(XBlock):
    """
    XBlock providing a google document embed link
    """
    display_name = String(
        display_name="Display Name",
        help="This name appears in the horizontal navigation at the top of the page.",
        scope=Scope.settings,
        default="Google Document"
    )

    embed_code = String(
        display_name="Embed Code",
        help="Google provides an embed code for Drive documents. In the Google Drive document, from the File menu, select Publish to the Web. Modify settings as needed, click Publish, and copy the embed code into this field.",
        scope=Scope.settings,
        default=textwrap.dedent("""
            <iframe
                src="https://docs.google.com/presentation/d/1x2ZuzqHsMoh1epK8VsGAlanSo7r9z55ualwQlj-ofBQ/embed?start=true&loop=true&delayms=10000"
                frameborder="0"
                width="960"
                height="569"
                allowfullscreen="true"
                mozallowfullscreen="true"
                webkitallowfullscreen="true">
            </iframe>
        """))

    def student_view(self, context={}):
        """
        Player view, displayed to the student
        """

        fragment = Fragment()
        context.update({
            "self": self,
        })
        fragment.add_content(render_template('/templates/html/google_docs.html', context))
        fragment.add_css(load_resource('public/css/google_docs.css'))
        fragment.add_javascript(load_resource('public/js/google_docs.js'))

        fragment.initialize_js('GoogleDocumentBlock')

        return fragment

    def studio_view(self, context):
        """
        Editing view in Studio
        """
        fragment = Fragment()
        fragment.add_content(render_template('/templates/html/google_docs_edit.html', {
            'self': self,
        }))
        fragment.add_javascript(load_resource('public/js/google_docs_edit.js'))

        fragment.initialize_js('GoogleDocumentEditBlock', {'defaultName': self.fields['display_name']._default})

        return fragment

    @XBlock.json_handler
    def studio_submit(self, submissions, suffix=''):

        self.display_name = submissions['display_name']
        self.embed_code = submissions['embed_code']

        return {
            'result': 'success',
        }

    @XBlock.json_handler
    def iframe_loaded(self, iframe_data, suffix=''):

        self.runtime.publish(self, 'iframe.loaded', iframe_data)

        return {
            'result': 'success',
        }

    @XBlock.json_handler
    def image_loaded(self, image_data, suffix=''):

        self.runtime.publish(self, 'image.loaded', image_data)

        return {
            'result': 'success',
        }

    @XBlock.json_handler
    def check_url(self, data, suffix=''):

        try:
            r = requests.head(data['url'])
        except:
            return {
                'status_code': 404,
            }

        return {
            'status_code': r.status_code,
        }
