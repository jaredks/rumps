# -*- coding: utf-8 -*-

import pickle

import AppKit
import PyObjCTools.AppHelper

from . import _internal
from . import ctx
from . import events
from . import menus
from . import notifications
from . import utils

# TODO
from .images import Image


class App(object):
    """Represents the statusbar application.

    Provides a simple and pythonic interface for all those long and cumbersome
    `PyObjC` calls. :class:`rumps.App` may be subclassed so that the
    application logic can be encapsulated within a class. Alternatively, an
    `App` can be instantiated and the various callback functions can exist at
    module level.

    .. versionchanged:: 0.2.0
       `name` parameter must be a string and `title` must be either a string or
       ``None``. `quit_button` parameter added.

    :param name: the name of the application.
    :param title: text that will be displayed for the application in the
        statusbar.
    :param icon: file path to the icon that will be displayed for the
        application in the statusbar.
    :param menu: an iterable of Python objects or pairs of objects that will be
        converted into the main menu for the application. Parsing is
        implemented by calling :meth:`rumps.MenuItem.update`.
    :param quit_button: the quit application menu item within the main menu. If
        ``None``, the default quit button will not be added.
    """

    #: A serializer for notification data.  The default is pickle.
    serializer = pickle

    def __init__(self, name, title=None, icon=None, template=None, menu=None, quit_button='Quit', debug=False):
        _internal._require_string(name)
        self._name = name
        self._icon = self._icon_nsimage = self._title = None
        self._template = template
        self.icon = icon
        self.title = title
        self.quit_button = quit_button
        self._menu = menus.Menu()
        if menu is not None:
            self.menu = menu
        self._application_support = utils.application_support(self._name)
        self.debug = debug

        # TODO
        self._quit_application = quit_application

    # Properties
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @property
    def name(self):
        """The name of the application. Determines the application support
        folder name. Will also serve as the title text of the application if
        :attr:`title` is not set.
        """
        return self._name

    @property
    def title(self):
        """The text that will be displayed for the application in the
        statusbar. Can be ``None`` in which case the icon will be used or, if
        there is no icon set the application text will fallback on the
        application :attr:`name`.

        .. versionchanged:: 0.2.0
           If the title is set then changed to ``None``, it will correctly be
           removed. Must be either a string or ``None``.

        """
        return self._title

    @title.setter
    def title(self, title):
        _internal._require_string_or_none(title)
        self._title = title
        try:
            self._nsapp.setStatusBarTitle()
        except AttributeError:
            pass

    @property
    def icon(self):
        """A path to an image representing the icon that will be displayed for
        the application in the statusbar. Can be ``None`` in which case the
        text from :attr:`title` will be used.

        .. versionchanged:: 0.2.0
           If the icon is set to an image then changed to ``None``, it will
           correctly be removed.

        """
        return self._icon

    @icon.setter
    def icon(self, icon_path):
        new_icon = Image.from_file(icon_path, template=self._template) if icon_path is not None else None
        self._icon = icon_path
        self._icon_nsimage = new_icon
        try:
            self._nsapp.setStatusBarIcon()
        except AttributeError:
            pass

    @property
    def template(self):
        """Template mode for an icon. If set to ``None``, the current icon (if
        any) is displayed as a color icon. If set to ``True``, template mode is
        enabled and the icon will be displayed correctly in dark menu bar mode.
        """
        return self._template

    @template.setter
    def template(self, template_mode):
        self._template = template_mode
        # resetting the icon to apply template setting
        self.icon = self._icon

    @property
    def menu(self):
        """Represents the main menu of the statusbar application. Setting
        `menu` works by calling :meth:`rumps.MenuItem.update`.
        """
        return self._menu

    @menu.setter
    def menu(self, iterable):
        self._menu.update(iterable)

    @property
    def quit_button(self):
        """The quit application menu item within the main menu. This is a
        special :class:`rumps.MenuItem` object that will both replace any
        function callback with :func:`rumps.quit_application` and add itself to
        the end of the main menu when :meth:`rumps.App.run` is called. If set
        to ``None``, the default quit button will not be added.

        .. warning::
           If set to ``None``, some other menu item should call
           :func:`rumps.quit_application` so that the application can exit
           gracefully.

        .. versionadded:: 0.2.0

        """
        return self._quit_button

    @quit_button.setter
    def quit_button(self, quit_text):
        if quit_text is None:
            self._quit_button = None
        else:
            self._quit_button = menus.MenuItem(quit_text)

    def log(self, *args, **kwargs):
        """xxx
        """
        if self.debug:
            utils.log(*args, **kwargs)

    # Open files in application support folder
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def open(self, *args):
        """Open a file within the application support folder for this
        application.

        .. code-block:: python

            app = App('Cool App')
            with app.open('data.json') as f:
                pass

        Is a shortcut for,

        .. code-block:: python

            app = App('Cool App')
            filename = os.path.join(application_support(app.name), 'data.json')
            with open(filename) as f:
                pass

        """
        return open(os.path.join(self._application_support, args[0]), *args[1:])

    # TODO: Events
    def set_on_right_click(self, callback):
        """Set the function serving as callback for when a right click event
        occurs on this UI component.

        :param callback: the function to be called.
        """
        self._callback = callback
        self._ns.setAction_('callback:' if callback is not None else None)

    @property
    def callback(self):
        """The function to be called in response to a user interaction event.
        """
        try:
            return self._callback
        except AttributeError:
            return None

    # Run the application
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def run(self, **options):
        """Performs various setup tasks including creating the underlying
        Objective-C application, starting the timers, and registering callback
        functions for click events. Then starts the application run loop.

        .. versionchanged:: 0.2.1
            Accepts `debug` keyword argument.

        :param debug: determines if application should log information useful
                      for debugging. Same effect as setting a value for
                      :attr:`debug.`.

        """
        dont_change = object()
        debug = options.get('debug', dont_change)
        if debug is not dont_change:
            self.debug = True

        ns_application = AppKit.NSApplication.sharedApplication()
        ns_application.activateIgnoringOtherApps_(True)  # NSAlerts in front
        self._nsapp = _internal.NSApp.alloc().init()
        self._nsapp._app = self.__dict__  # allow for dynamic modification based on this App instance
        ns_application.setDelegate_(self._nsapp)
        notifications._setup_notifications(self._nsapp)


        ctx._set_current_app(self)

        # TODO
        ctx.deferred_fire()

        self._nsapp.initializeStatusBar()
        PyObjCTools.AppHelper.installMachInterrupt()

        events.before_start.emit()
        PyObjCTools.AppHelper.runEventLoop()

    def quit(self):
        """xxx
        """
        quit_application()


def quit_application(sender=None):
    """Quit the application. Some menu item should call this function so that
    the application can exit gracefully.
    """
    ns_application = AppKit.NSApplication.sharedApplication()
    utils.log('quitting application')
    ns_application.terminate_(sender)
