"""Setup for my_google_drive XBlock."""

from __future__ import absolute_import

import os

from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='xblock-google-drive',
    version='0.5.0',
    description='An XBlock which allows embedding of Google documents and calendar within an edX course',
    url='https://github.com/openedx/xblock-google-drive',
    packages=[
        'google_drive',
    ],
    install_requires=[
        'mako',
        'XBlock',
        'xblock-utils',
    ],
    dependency_links=[
        'http://github.com/openedx/xblock-utils/tarball/master#egg=xblock-utils',
    ],
    entry_points={
        'xblock.v1': [
            'google-document = google_drive:GoogleDocumentBlock',
            'google-calendar = google_drive:GoogleCalendarBlock'
        ]
    },
    package_data=package_data("google_drive", ["static", "templates", "public", "translations", "conf"]),
)
