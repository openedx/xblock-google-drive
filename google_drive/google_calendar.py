""" Google Calendar XBlock implementation """
# -*- coding: utf-8 -*-
#

# Imports ###########################################################
import logging

from xblock.core import XBlock
from xblock.fields import Scope, String, Integer
from xblock.fragment import Fragment

from xblockutils.publish_event import PublishEventMixin
from xblockutils.resources import ResourceLoader

LOG = logging.getLogger(__name__)
RESOURCE_LOADER = ResourceLoader(__name__)

# Constants ###########################################################
DEFAULT_CALENDAR_ID = "edx.org_lom804qe3ttspplj1bgeu1l3ak@group.calendar.google.com"
DEFAULT_CALENDAR_URL = (
    'https://www.google.com/calendar/embed?mode=Month&src={}&showCalendars=0'.format(DEFAULT_CALENDAR_ID))
CALENDAR_TEMPLATE = "/templates/html/google_calendar.html"
CALENDAR_EDIT_TEMPLATE = "/templates/html/google_calendar_edit.html"


# Classes ###########################################################
class GoogleCalendarBlock(XBlock, PublishEventMixin):  # pylint: disable=too-many-ancestors
    """
    XBlock providing a google calendar view for a specific calendar
    """
    display_name = String(
        display_name="Display Name",
        help="This name appears in the horizontal navigation at the top of the page.",
        scope=Scope.settings,
        default="Google Calendar"
    )
    calendar_id = String(
        display_name="Public Calendar ID",
        help=(
            "Google provides an ID for publicly available calendars. In the Google Calendar, "
            "open Settings and copy the ID from the Calendar Address section into this field."
        ),
        scope=Scope.settings,
        default=DEFAULT_CALENDAR_ID
    )
    default_view = Integer(
        display_name="Default View",
        help="The calendar view that students see by default. A student can change this view.",
        scope=Scope.settings,
        default=1
    )
    views = [(0, 'Week'), (1, 'Month'), (2, 'Agenda')]

    # Context argument is specified for xblocks, but we are not using herein
    def student_view(self, context):  # pylint: disable=unused-argument
        """
        Player view, displayed to the student
        """
        fragment = Fragment()

        fragment.add_content(RESOURCE_LOADER.render_template(CALENDAR_TEMPLATE, {
            "mode": self.views[self.default_view][1],
            "src": self.calendar_id,
            "title": self.display_name,
        }))
        fragment.add_css(RESOURCE_LOADER.load_unicode('public/css/google_calendar.css'))
        fragment.add_javascript(RESOURCE_LOADER.load_unicode('public/js/google_calendar.js'))

        fragment.initialize_js('GoogleCalendarBlock')

        return fragment

    # Context argument is specified for xblocks, but we are not using herein
    def studio_view(self, context):  # pylint: disable=unused-argument
        """
        Editing view in Studio
        """
        fragment = Fragment()
        # Need to access protected members of fields to get their default value
        fragment.add_content(RESOURCE_LOADER.render_template(CALENDAR_EDIT_TEMPLATE, {
            'self': self,
            'defaultName': self.fields['display_name']._default,  # pylint: disable=protected-access
            'defaultID': self.fields['calendar_id']._default  # pylint: disable=protected-access
        }))
        fragment.add_javascript(RESOURCE_LOADER.load_unicode('public/js/google_calendar_edit.js'))
        fragment.add_css(RESOURCE_LOADER.load_unicode('public/css/google_edit.css'))

        fragment.initialize_js('GoogleCalendarEditBlock')

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
        if 'calendar_id' in submissions:
            self.calendar_id = submissions['calendar_id']
        if 'default_view' in submissions:
            self.default_view = submissions['default_view']

        return {
            'result': 'success',
        }

    @staticmethod
    def workbench_scenarios():
        """
        A canned scenario for display in the workbench.
        """
        return [("Google Calendar scenario", "<vertical_demo><google-calendar/></vertical_demo>")]
