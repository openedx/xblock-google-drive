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
        help="Google provides an embed code for Drive documents with a variety of settings. From inside a Google Drive document, select Publish to the Web from within the File menuto get to your Embed Code with your desired settings.",
        scope=Scope.settings,
        default=textwrap.dedent("""
            <iframe
                src="https://docs.google.com/presentation/d/1B22AsMwG7jgE39vm1BuiJClir_JUz1q077cPEKJR2mI/embed?start=false&loop=false&delayms=3000"
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

        fragment.initialize_js('GoogleDocumentEditBlock')

        return fragment

    @XBlock.json_handler
    def studio_submit(self, submissions, suffix=''):

        self.display_name = submissions['display_name']
        self.embed_code = submissions['embed_code']

        return {
            'result': 'success',
        }
