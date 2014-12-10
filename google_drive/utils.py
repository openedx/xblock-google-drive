# -*- coding: utf-8 -*-
#

# Imports ###########################################################

import logging
import pkg_resources

from django.template import Context, Template

from xblockutils.resources import ResourceLoader
from xblockutils.publish_event import PublishEventMixin

# Globals ###########################################################

log = logging.getLogger(__name__)


# Functions #########################################################

loader = ResourceLoader(__name__)

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
