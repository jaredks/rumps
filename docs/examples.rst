Examples
==============

Sometimes the best way to learn something is by example. Form your own application based on some of these samples.

Simple subclass structure
-------------------------

Just a straightforward application,

.. code-block:: python

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

Decorating any functions
------------------------

The following code demonstrates how you can decorate functions with :func:`rumps.clicked` whether or not they are inside a subclass of :class:`rumps.App`. The parameter ``sender``, the :class:`rumps.MenuItem` object, is correctly passed to both functions even though ``button`` needs an instance of ``SomeApp`` as its ``self`` parameter.

Usually functions registered as callbacks should accept one and only one argument but an `App` subclass is viewed as a special case as its use can provide a simple and pythonic way to implement the logic behind an application.

.. code-block:: python

    from rumps import *

    @clicked('Testing')
    def tester(sender):
        sender.state = not sender.state

    class SomeApp(rumps.App):
        def __init__(self):
            super(SomeApp, self).__init__(type(self).__name__, menu=['On', 'Testing'])
            rumps.debug_mode(True)

        @clicked('On')
        def button(self, sender):
            sender.title = 'Off' if sender.title == 'On' else 'On'
            Window("I can't think of a good example app...").run()

    if __name__ == "__main__":
        SomeApp().run()

New features in 0.2.0
---------------------

Menu items can be disabled (greyed out) by passing ``None`` to :meth:`rumps.MenuItem.set_callback`. :func:`rumps.alert` no longer requires `title` (will use a default localized string) and allows for custom `cancel` button text. The new parameter `quit_button` for :class:`rumps.App` allows for custom quit button text or removal of the quit button entirely by passing ``None``.

.. warning::
   By setting :attr:`rumps.App.quit_button` to ``None`` you **must include another way to quit the application** by somehow calling :func:`rumps.quit_application` otherwise you will have to force quit.

.. code-block:: python

    import rumps
    
    rumps.debug_mode(True)
    
    @rumps.clicked('Print Something')
    def print_something(_):
        rumps.alert(message='something', ok='YES!', cancel='NO!')
    
    
    @rumps.clicked('On/Off Test')
    def on_off_test(_):
        print_button = app.menu['Print Something']
        if print_button.callback is None:
            print_button.set_callback(print_something)
        else:
            print_button.set_callback(None)
    
    
    @rumps.clicked('Clean Quit')
    def clean_up_before_quit(_):
        print 'execute clean up code'
        rumps.quit_application()
    
    
    app = rumps.App('Hallo Thar', menu=['Print Something', 'On/Off Test', 'Clean Quit'], quit_button=None)
    app.run()

