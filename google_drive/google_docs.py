# -*- coding: utf-8 -*-
#

# Imports ###########################################################

import pkg_resources
import textwrap
import requests

from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment

from .utils import loader, AttrDict
from xblockutils.publish_event import PublishEventMixin

# Classes ###########################################################

class GoogleDocumentBlock(XBlock, PublishEventMixin):
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

    alt_text = String(
        display_name="Alternative Text",
        help="In situations where image is not available to the reader, the alternative text ensures that no information or functionality is lost.",
        scope=Scope.settings,
        default=""
    )

    def student_view(self, context={}):
        """
        Player view, displayed to the student
        """

        fragment = Fragment()
        context.update({
            "self": self
        })

        fragment.add_content(loader.render_template('/templates/html/google_docs.html', context))
        fragment.add_css(loader.load_unicode('public/css/google_docs.css'))
        fragment.add_javascript(loader.load_unicode('public/js/google_docs.js'))

        fragment.initialize_js('GoogleDocumentBlock')

        return fragment

    def studio_view(self, context):
        """
        Editing view in Studio
        """
        fragment = Fragment()
        fragment.add_content(loader.render_template('/templates/html/google_docs_edit.html', {
            'self': self,
            'defaultName': self.fields['display_name']._default
        }))
        fragment.add_javascript(loader.load_unicode('public/js/google_docs_edit.js'))
        fragment.add_css(loader.load_unicode('public/css/google_edit.css'))

        fragment.initialize_js('GoogleDocumentEditBlock')

        return fragment

    @XBlock.json_handler
    def studio_submit(self, submissions, suffix=''):

        self.display_name = submissions['display_name']
        self.embed_code = submissions['embed_code']
        self.alt_text = submissions['alt_text']

        return {
            'result': 'success',
        }

    @XBlock.json_handler
    def check_url(self, data, suffix=''):

        try:
            r = requests.head(data['url'])
        except:
            return {
                'status_code': 400,
            }

        return {
            'status_code': r.status_code,
        }

    @staticmethod
    def workbench_scenarios():
        """
        A canned scenario for display in the workbench.
        """
        return [("Google Docs scenario", "<vertical_demo><google-document/></vertical_demo>")]
