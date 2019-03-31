# -*- coding: utf-8 -*-
"""
rumps.decorators
~~~~~~~~~~~~~~~~

xxx

"""

from . import ctx
from . import events
from . import menus


@ctx.DeferredCalls
def timer(interval):
    """Decorator for registering a function as a callback in a new thread. The
    function will be repeatedly called every `interval` seconds. This decorator
    accomplishes the same thing as creating a :class:`rumps.Timer` object by
    using the decorated function and `interval` as parameters and starting it
    on application launch.

    .. code-block:: python

        @rumps.timer(2)
        def repeating_function(sender):
            print 'hi'

    :param interval: a number representing the time in seconds before the
        decorated function should be called.
    """
    def decorator(f):
        slider.defer(_create_timer, f, interval=interval)
        return f
    return decorator


def _create_timer(f, interval):
    t = Timer(f, interval=interval)
    t.start()


@ctx.DeferredCalls
def clicked(*args, **options):
    """Decorator for registering a function as a callback for a click action on
    a :class:`rumps.MenuItem` within the application. The passed `args` must
    specify an existing path in the main menu. The :class:`rumps.MenuItem`
    instance at the end of that path will have its
    :meth:`rumps.MenuItem.set_callback` method called, passing in the decorated
    function.

    .. versionchanged:: 0.2.1
        Accepts `key` keyword argument.

    .. code-block:: python

        @rumps.clicked('Animal', 'Dog', 'Corgi')
        def corgi_button(sender):
            import subprocess
            subprocess.call(['say', '"corgis are the cutest"'])

    :param args: a series of strings representing the path to a
        :class:`rumps.MenuItem` in the main menu of the application.
    :param key: a string representing the key shortcut as an alternative means
        of clicking the menu item.
    """
    def decorator(f):
        slider.defer(_register_click, f, path=args, options=options)
        return f
    return decorator


def _register_click(callback, path, options):
    app = ctx.current_app()
    menuitem = app.menu

    if menuitem is None:
        raise ValueError('no menu created')

    for item in path:
        try:
            menuitem = menuitem[item]
        except KeyError:
            menuitem.add(item)
            menuitem = menuitem[item]

    menuitem.set_callback(callback, options.get('key'))


@ctx.DeferredCalls
def slider(*args, **options):
    """Decorator for registering a function as a callback for a slide action on
    a :class:`rumps.SliderMenuItem` within the application. All elements of the
    provided path will be created as :class:`rumps.MenuItem` objects. The
    :class:`rumps.SliderMenuItem` will be created as a child of the last menu
    item.

    Accepts the same keyword arguments as :class:`rumps.SliderMenuItem`.

    .. versionadded:: 0.3.0

    :param args: a series of strings representing the path to a
        :class:`rumps.SliderMenuItem` in the main menu of the
        application.
    """
    def decorator(f):
        slider.defer(_register_slider, f, path=args, options=options)
        return f
    return decorator


def _register_slider(callback, path, options):
    app = ctx.current_app()
    menuitem = app.menu

    if menuitem is None:
        raise ValueError('no menu created')

    # create here in case of error so we don't create the path
    slider_menu_item = menus.SliderMenuItem(**options)
    slider_menu_item.set_callback(callback)

    for item in path:
        try:
            menuitem = menuitem[item]
        except KeyError:
            menuitem.add(item)
            menuitem = menuitem[item]

    menuitem.add(slider_menu_item)


def on_notification(f):
    """Decorator for registering a function to serve as a "notification center"
    for the application. This function will receive the data associated with an
    incoming macOS notification sent using :func:`rumps.notification`. This
    occurs whenever the user clicks on a notification for this application in
    the macOS Notification Center.

    .. code-block:: python

        @rumps.notifications
        def notification_center(info):
            if 'unix' in info:
                print 'i know this'

    """
    events.on_notification.register(f)
    return f
