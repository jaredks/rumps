Creating Standalone Applications
================================

If you want to create your own bundled .app you need to download py2app: https://pythonhosted.org/py2app/

For creating standalone apps, just make sure to include ``rumps`` in the ``packages`` list. Most simple statusbar-based
apps are just "background" apps (no icon in the dock; inability to tab to the application) so it is likely that you
would want to set ``'LSUIElement'`` to ``True``. A basic ``setup.py`` would look like,

.. code-block:: python

    from setuptools import setup

    APP = ['example_class.py']
    DATA_FILES = []
    OPTIONS = {
        'argv_emulation': True,
        'plist': {
            'LSUIElement': True,
        },
        'packages': ['rumps'],
    }

    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )

With this you can then create a standalone,

.. code-block:: bash

    python setup.py py2app
