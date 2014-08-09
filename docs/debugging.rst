Debugging Your Application
==========================

When writing your application you will want to turn on debugging mode.

.. code-block:: python

    import rumps
    rumps.debug_mode(True)

If you are running your program from the interpreter, you should see the informational messages.

.. code-block:: bash

    python {your app name}.py

If testing the .app generated using py2app, to be able to see these messages you must not,

.. code-block:: bash

    open {your app name}.app

but instead run the executable. While within the directory containing the .app,

.. code-block:: bash

    ./{your app name}.app/Contents/MacOS/{your app name}

And, by default, your .app will be in ``dist`` folder after running ``python setup.py py2app``. So of course that would then be,

.. code-block:: bash

    ./dist/{your app name}.app/Contents/MacOS/{your app name}
