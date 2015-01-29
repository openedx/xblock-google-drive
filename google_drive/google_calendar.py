"""
Google Calendar XBlock implementation
"""
# -*- coding: utf-8 -*-
#

# Imports ###########################################################
import logging

from xblock.core import XBlock
from xblock.fields import Scope, String, Integer
from xblock.fragment import Fragment

from xblockutils.publish_event import PublishEventMixin
from xblockutils.resources import ResourceLoader

log = logging.getLogger(__name__)
RESOURCE_LOADER = ResourceLoader(__name__)

# Classes ###########################################################


class GoogleCalendarBlock(XBlock, PublishEventMixin):
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
        default="edx.org_lom804qe3ttspplj1bgeu1l3ak@group.calendar.google.com"
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

        view = self.views[self.default_view][1]

        iframe = (
            '<iframe src="https://www.google.com/calendar/embed'
            '?mode={}&amp;src={}&amp;showCalendars=0" title="{}"></iframe>'
        ).format(
            view, self.calendar_id, self.display_name
        )

        fragment.add_content(RESOURCE_LOADER.render_template('/templates/html/google_calendar.html', {
            "self": self,
            "iframe": iframe
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
        fragment.add_content(RESOURCE_LOADER.render_template('/templates/html/google_calendar_edit.html', {
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
        self.display_name = submissions['display_name']
        self.calendar_id = submissions['calendar_id']
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
