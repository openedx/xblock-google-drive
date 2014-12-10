# -*- coding: utf-8 -*-
#

# Imports ###########################################################

import pkg_resources
import textwrap

from xblock.core import XBlock
from xblock.fields import Scope, String, Integer
from xblock.fragment import Fragment

from .utils import loader, AttrDict
from xblockutils.publish_event import PublishEventMixin

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
        help="Google provides an ID for publicly available calendars. In the Google Calendar, open Settings and copy the ID from the Calendar Address section into this field.",
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

    def student_view(self, context={}):
        """
        Player view, displayed to the student
        """

        fragment = Fragment()

        view = self.views[self.default_view][1]

        iframe = '<iframe src="https://www.google.com/calendar/embed?mode={}&amp;src={}&amp;showCalendars=0" title="{}"></iframe>'.format(view, self.calendar_id, self.display_name)

        context.update({
            "self": self,
            "iframe": iframe
        })
        fragment.add_content(loader.render_template('/templates/html/google_calendar.html', context))
        fragment.add_css(loader.load_unicode('public/css/google_calendar.css'))
        fragment.add_javascript(loader.load_unicode('public/js/google_calendar.js'))

        fragment.initialize_js('GoogleCalendarBlock')

        return fragment

    def studio_view(self, context):
        """
        Editing view in Studio
        """
        fragment = Fragment()
        fragment.add_content(loader.render_template('/templates/html/google_calendar_edit.html', {
            'self': self,
            'defaultName': self.fields['display_name']._default,
            'defaultID': self.fields['calendar_id']._default
        }))
        fragment.add_javascript(loader.load_unicode('public/js/google_calendar_edit.js'))
        fragment.add_css(loader.load_unicode('public/css/google_edit.css'))

        fragment.initialize_js('GoogleCalendarEditBlock')

        return fragment

    @XBlock.json_handler
    def studio_submit(self, submissions, suffix=''):

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
