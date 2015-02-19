""" Base classes for integration tests """
from xblockutils.base_test import SeleniumBaseTest


class GoogleCalendarBaseTest(SeleniumBaseTest):  # pylint: disable=too-many-ancestors, too-few-public-methods
    """ Base class for Google Calendar integration tests """
    module_name = __name__
    default_css_selector = 'div.google-calendar-xblock-wrapper'


class GoogleDocumentBaseTest(SeleniumBaseTest):  # pylint: disable=too-many-ancestors, too-few-public-methods
    """ Base class for Google Document integration tests """
    module_name = __name__
    default_css_selector = 'div.google-docs-xblock-wrapper'
