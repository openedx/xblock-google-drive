"""
Google drive XBlocks
"""
from importlib.metadata import version

from .google_docs import GoogleDocumentBlock
from .google_calendar import GoogleCalendarBlock

__version__ = version("xblock-google-drive")
