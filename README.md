Google Drive & Calendar XBlock
------------------------------

This XBlock allows embedding of Google documents and calendar,
within an edX course.

Installation
------------

Install the requirements into the python virtual environment of your
`edx-platform` installation by running the following command from the
root folder:

```bash
$ pip install -r requirements.txt
```

Enabling in Studio
------------------

You can enable the Google Drive & Calendar XBlock in studio through the advanced
settings.

1. From the main page of a specific course, navigate to `Settings ->
   Advanced Settings` from the top menu.
2. Check for the `advanced_modules` policy key, and add `"google-document"` and
   `"google-calendar"` to the policy value list.
3. Click the "Save changes" button.

Workbench installation and settings
-----------------------------------

Install to the workbench's virtualenv by running the following command form the mentoring repo root:

```bash
pip install -r requirements.txt
```

In the main XBlock repository, create the following configuration file
in `workbench/settings_googledrive.py` in the XBlock repository:

```python
from settings import *

INSTALLED_APPS += ('google_drive',)
DATABASES['default']['NAME'] = 'workbench.sqlite'
```

Running the workbench
---------------------

```bash
$ ./manage.py runserver 8000 --settings=workbench.settings_googledrive
```

Access it at [http://localhost:8000/](http://localhost:8000).

Running tests
-------------

From the xblock-google-drive repository root, run the tests with the
following command:

```bash
$ DJANGO_SETTINGS_MODULE="workbench.settings_googledrive" nosetests --with-django
```

If you want to run only the integration or the unit tests, append the directory to the command. You can also run separate modules in this manner.

```bash
$ DJANGO_SETTINGS_MODULE="workbench.settings_googledrive" nosetests --with-django tests/unit
```

If you have not installed the xblock-sdk in the active virtualenv,
you might also have to prepend `PYTHONPATH=".:/path/to/xblock"` to the command above.
(`/path/to/xblock` is the path to the xblock-sdk, where the workbench resides).

License
-------

The Google Drive & Calendar XBlocks are available under the GNU Affero General
Public License (AGPLv3).

