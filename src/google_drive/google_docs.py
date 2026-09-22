""" Google Document XBlock implementation """
# -*- coding: utf-8 -*-
#

# Imports ###########################################################
from __future__ import absolute_import
import logging
import textwrap

import requests
from xblock.core import XBlock
from xblock.fields import Scope, String
from web_fragments.fragment import Fragment
try:
    from xblock.utils.publish_event import PublishEventMixin  # pylint: disable=ungrouped-imports
    from xblock.utils.resources import ResourceLoader  # pylint: disable=ungrouped-imports
except ModuleNotFoundError:  # For backward compatibility with releases older than Quince.
    from xblockutils.publish_event import PublishEventMixin
    from xblockutils.resources import ResourceLoader
import six

LOG = logging.getLogger(__name__)
RESOURCE_LOADER = ResourceLoader(__name__)

# Constants ###########################################################
DEFAULT_DOCUMENT_URL = (
    'https://docs.google.com/presentation/d/1x2ZuzqHsMoh1epK8VsGAlanSo7r9z55ualwQlj-ofBQ/embed?'
    'start=true&loop=true&delayms=10000'
)
DEFAULT_EMBED_CODE = textwrap.dedent("""
    <iframe
        src="{}"
        frameborder="0"
        width="960"
        height="569"
        allowfullscreen="true"
        mozallowfullscreen="true"
        webkitallowfullscreen="true">
    </iframe>
""") .format(DEFAULT_DOCUMENT_URL)
DOCUMENT_TEMPLATE = "/templates/html/google_docs.html"
DOCUMENT_EDIT_TEMPLATE = "/templates/html/google_docs_edit.html"


def _(text):
    """
    Dummy ugettext.
    """
    return text


# Classes ###########################################################
@XBlock.needs("i18n")
class GoogleDocumentBlock(XBlock, PublishEventMixin):
    """
    XBlock providing a google document embed link
    """
    display_name = String(
        display_name=_("Display Name"),
        help=_("This name appears in the horizontal navigation at the top of the page."),
        scope=Scope.settings,
        default="Google Document"
    )
    embed_code = String(
        display_name=_("Embed Code"),
        help=_(
            "Google provides an embed code for Drive documents. In the Google Drive document, "
            "from the File menu, select Publish to the Web. Modify settings as needed, click "
            "Publish, and copy the embed code into this field."
        ),
        scope=Scope.settings,
        default=DEFAULT_EMBED_CODE
    )
    alt_text = String(
        display_name=_("Alternative Text"),
        help=_("Alternative text describes an image and appears if the image is unavailable."),
        scope=Scope.settings,
        default=""
    )

    # Context argument is specified for xblocks, but we are not using herein
    def student_view(self, context):  # pylint: disable=unused-argument
        """
        Player view, displayed to the student
        """
        fragment = Fragment()

        fragment.add_content(RESOURCE_LOADER.render_django_template(
            DOCUMENT_TEMPLATE,
            context={"self": self},
            i18n_service=self.runtime.service(self, 'i18n'),
        ))
        fragment.add_css(RESOURCE_LOADER.load_unicode('public/css/google_docs.css'))
        fragment.add_javascript(RESOURCE_LOADER.load_unicode('public/js/google_docs.js'))

        fragment.initialize_js('GoogleDocumentBlock')

        return fragment

    # Context argument is specified for xblocks, but we are not using herein
    def studio_view(self, context):  # pylint: disable=unused-argument
        """
        Editing view in Studio
        """
        fragment = Fragment()
        # Need to access protected members of fields to get their default value
        default_name = self.fields['display_name']._default  # pylint: disable=protected-access,unsubscriptable-object
        fragment.add_content(RESOURCE_LOADER.render_django_template(
            DOCUMENT_EDIT_TEMPLATE,
            context={'self': self, 'defaultName': default_name},
            i18n_service=self.runtime.service(self, 'i18n'),
        ))
        fragment.add_javascript(RESOURCE_LOADER.load_unicode('public/js/google_docs_edit.js'))
        fragment.add_css(RESOURCE_LOADER.load_unicode('public/css/google_edit.css'))

        fragment.initialize_js('GoogleDocumentEditBlock')

        return fragment

    # suffix argument is specified for xblocks, but we are not using herein
    @XBlock.json_handler
    def studio_submit(self, submissions, suffix=''):  # pylint: disable=unused-argument
        """
        Change the settings for this XBlock given by the Studio user
        """
        if not isinstance(submissions, dict):
            LOG.error("submissions object from Studio is not a dict - %r", submissions)
            return {
                'result': 'error'
            }

        if 'display_name' in submissions:
            self.display_name = submissions['display_name']
        if 'embed_code' in submissions:
            self.embed_code = submissions['embed_code']
        if 'alt_text' in submissions:
            self.alt_text = submissions['alt_text']

        return {
            'result': 'success',
        }

    # suffix argument is specified for xblocks, but we are not using herein
    @XBlock.json_handler
    def check_url(self, data, suffix=''):  # pylint: disable=unused-argument
        """
        Checks that the given document url is accessible, and therefore assumed to be valid
        """
        try:
            test_url = data['url']
        except KeyError as ex:
            LOG.debug("URL not provided - %s", six.text_type(ex))
            return {
                'status_code': 400,
            }

        try:
            url_response = requests.head(test_url)  # pylint: disable=missing-timeout
        # Catch wide range of request exceptions
        except requests.exceptions.RequestException as ex:
            LOG.debug("Unable to connect to %s - %s", test_url, six.text_type(ex))
            return {
                'status_code': 400,
            }

        return {
            'status_code': url_response.status_code,
        }

    @staticmethod
    def workbench_scenarios():
        """
        A canned scenario for display in the workbench.
        """
        return [("Google Docs scenario", "<vertical_demo><google-document/></vertical_demo>")]
