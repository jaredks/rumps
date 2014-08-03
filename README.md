rumps
=====

<b>R</b>idiculously <b>U</b>ncomplicated <b>M</b>ac os x <b>P</b>ython <b>S</b>tatusbar apps.

![pic](https://raw.github.com/jaredks/rumps/master/examples/rumps_example.png)

```python
import rumps

class AwesomeStatusBarApp(rumps.App):
    def __init__(self):
        super(AwesomeStatusBarApp, self).__init__("Awesome App")
        self.menu = ["Preferences", "Silly button", "Say hi"]

    @rumps.clicked("Preferences")
    def prefs(self, _):
        rumps.alert("jk! no preferences available!")

    @rumps.clicked("Silly button")
    def onoff(self, sender):
        sender.state = not sender.state

    @rumps.clicked("Say hi")
    def sayhi(self, _):
        rumps.notification("Awesome title", "amazing subtitle", "hi!!1")

if __name__ == "__main__":
    AwesomeStatusBarApp().run()
```

How fun!?

`rumps` can greatly shorten the code required to generate a working app. No `PyObjC` underscore syntax required!


Use case
--------

`rumps` is for any console-based program that would benefit from a simple configuration toolbar or launch menu.

Good for:

* Notification-center-based app
* Controlling daemons / launching separate programs
* Updating simple info from web APIs on a timer

Not good for:

* Any app that is first and foremost a GUI application


Required
--------

* PyObjC


Recommended
-----------

* py2app

For creating standalone apps, just make sure to include `rumps` in the `packages` list. Most simple statusbar-based
apps are just "background" apps (no icon in the dock; inability to tab to the application) so it is likely that you
would want to set `'LSUIElement'` to `True`. A basic `setup.py` would look like,

```python
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
```

With this you can then create a standalone,

    python setup.py py2app


Installation
------------

    python setup.py install


License
-------

"Modified BSD License". See LICENSE for details. Copyright Jared Suttles, 2014.
