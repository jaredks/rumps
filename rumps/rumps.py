#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# rumps: Ridiculously Uncomplicated Mac os x Python Statusbar apps.
# Copyright: (c) 2013, Jared Suttles. All rights reserved.
# License: BSD, see LICENSE for details.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from Foundation import (NSUserNotification, NSUserNotificationCenter, NSDate, NSTimer, NSRunLoop, NSDefaultRunLoopMode,
                        NSSearchPathForDirectoriesInDomains, NSMakeRect, NSLog, NSObject)
from AppKit import NSApplication, NSStatusBar, NSMenu, NSMenuItem, NSAlert, NSTextField, NSImage
from PyObjCTools import AppHelper

import os
import sys
import weakref
from collections import Mapping, Iterable
from .utils import ListDict

_TIMERS = weakref.WeakSet()
separator = object()


def debug_mode(choice):
    """
    Enable/disable printing helpful information for debugging your program. If testing the .app generated using
    py2app, to be able to see these messages you must not `open {your app name}.app` but instead run the executable,

    While within the directory containing the .app,

        ./{your app name}.app/Contents/MacOS/{your app name}

    And, by default, your .app will be in `dist` folder after running `python setup.py py2app`. So of course that would
    then be,

        ./dist/{your app name}.app/Contents/MacOS/{your app name}

    """
    global _log
    if choice:
        def _log(*args):
            NSLog(' '.join(map(str, args)))
    else:
        def _log(*_):
            pass
debug_mode(False)


def alert(title, message='', ok=None, cancel=False):
    """
    Simple alert window.
    """
    message = str(message)
    title = str(title)
    alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
        title, ok, 'Cancel' if cancel else None, None, message)
    alert.setAlertStyle_(0)  # informational style
    _log('alert opened with message: {}, title: {}'.format(repr(message), repr(title)))
    return alert.runModal()


def notification(title, subtitle, message, data=None, sound=True):
    """
    Notification sender. Apple says, "The userInfo content must be of reasonable serialized size (less than 1k) or an
    exception will be thrown." So don't do that!
    """
    if data is not None and not isinstance(data, Mapping):
        raise TypeError('notification data must be a mapping')
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(message)
    notification.setUserInfo_({} if data is None else data)
    if sound:
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
    notification.setDeliveryDate_(NSDate.dateWithTimeInterval_sinceDate_(0, NSDate.date()))
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)


def application_support(name):
    """
    Return the application support folder path for the given application name.
    """
    app_support_path = os.path.join(NSSearchPathForDirectoriesInDomains(14, 1, 1).objectAtIndex_(0), name)
    if not os.path.isdir(app_support_path):
        os.mkdir(app_support_path)
    return app_support_path


def timers():
    """
    Returns a set of Timer objects.
    """
    return set(_TIMERS)


def _nsimage_from_file(filename, dimensions=None):
    """
    Takes a path to an image file and returns an NSImage object.
    """
    try:
        _log('attempting to open image at {}'.format(filename))
        with open(filename):
            pass
    except IOError:  # literal file path didn't work -- try to locate image based on main script path
        try:
            from __main__ import __file__ as main_script_path
            main_script_path = os.path.dirname(main_script_path)
            filename = os.path.join(main_script_path, filename)
        except ImportError:
            pass
        _log('attempting (again) to open image at {}'.format(filename))
        with open(filename):  # file doesn't exist
            pass              # otherwise silently errors in NSImage which isn't helpful for debugging
    image = NSImage.alloc().initByReferencingFile_(filename)
    image.setScalesWhenResized_(True)
    image.setSize_((20, 20) if dimensions is None else dimensions)
    return image


# Decorators and helper function serving to register functions for dealing with interaction and events
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def timer(interval):
    """
    Decorator for registering a function as a callback for a timer thread. Timer object deals with delegating event
    to callback function.
    """
    def decorator(f):
        timers = timer.__dict__.setdefault('*timers', [])
        timers.append(Timer(f, interval))
        return f
    return decorator


def clicked(*args):
    """
    Decorator for registering a function as a callback for a click action. MenuItem class deals with delegating the
    event to the callback function, passed here to set_callback method.
    """
    def decorator(f):

        def register_click(self):
            menuitem = self._menu  # self not defined yet but will be later in 'run' method
            if menuitem is None:
                raise ValueError('no menu created')
            try:
                for arg in args:
                    menuitem = menuitem[arg]
            except KeyError:
                raise ValueError('no path exists in menu for {}'.format(' -> '.join(map(repr, args))))
            menuitem.set_callback(f)

        # delay registering the button until we have a current instance to be able to traverse the menu
        buttons = clicked.__dict__.setdefault('*buttons', [])
        buttons.append(register_click)

        return f
    return decorator


def notifications(f):
    """
    Decorator for registering a function to serve as notification center. Should accept data dict of incoming
    notifications and can decide behavior based on that information.
    """
    notifications.__dict__['*notification_center'] = f
    return f


def _call_as_function_or_method(f, event):
    """
    The idea here is that when using decorators in a class, the functions passed are not bound so we have to determine
    later if the functions we have (those saved as callbacks) for particular events need to be passed 'self'.

    Usually functions registered as callbacks should accept one and only one argument but an App subclass is viewed as
    a special case as it can provide a simple and pythonic way to implement the logic behind an application.

    This works for an App subclass method or a standalone decorated function. Will attempt to call function with event
    alone then try with self and event. This might not be a great idea if the function is unbound and normally takes
    two arguments... but people shouldn't be decorating functions that consume more than a single parameter anyway!

    Decorating methods of a class subclassing something other than App should produce AttributeError eventually which
    is hopefully understandable.
    """
    try:
        r = f(event)
        _log('given function {} is outside an App subclass definition'.format(repr(f)))
        return r
    except TypeError as e:  # possibly try it with self if TypeError makes sense
        if e.message.endswith('takes exactly 2 arguments (1 given)'):
            r = f(getattr(App, '*app_instance'), event)
            _log('given function {} is probably inside a class (which should be an App subclass)'.format(repr(f)))
            return r
        raise e
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Menu(ListDict):
    """
    Wrapper for Objective C's NSMenu. Class implements core functionality of menus in rumps. MenuItem subclasses Menu.
    """
    _choose_key = object()

    def __init__(self):
        self._separators = 1
        if not hasattr(self, '_menu'):
            self._menu = NSMenu.alloc().init()
        super(Menu, self).__init__()

    def __setitem__(self, key, value):
        if key not in self:
            key, value = self._process_new_menuitem(key, value)
            self._menu.addItem_(value._menuitem)
            super(Menu, self).__setitem__(key, value)

    def __delitem__(self, key):
        value = self[key]
        self._menu.removeItem_(value._menuitem)
        super(Menu, self).__delitem__(key)

    def add(self, menuitem):
        self.__setitem__(self._choose_key, menuitem)

    def clear(self):
        self._menu.removeAllItems()
        super(Menu, self).clear()

    def copy(self):
        raise NotImplementedError

    @classmethod
    def fromkeys(cls, *args, **kwargs):
        raise NotImplementedError

    def update(self, iterable, **kwargs):
        """
        This update is a bit different from the usual dict update method. It works recursively and will parse a
        variety of Python containers, creating menus as necessary.

        Keys of corresponding MenuItems in the Menu dictionary are the title of those MenuItems at the time of parsing.
        """
        def parse_menu(iterable, menu, depth):
            if isinstance(iterable, MenuItem):
                menu.add(iterable)
                return

            for n, ele in enumerate(iterable.iteritems() if isinstance(iterable, Mapping) else iterable):

                # for mappings we recurse but don't drop down a level in the menu
                if not isinstance(ele, MenuItem) and isinstance(ele, Mapping):
                    parse_menu(ele, menu, depth)

                # any iterables other than strings and MenuItems
                elif not isinstance(ele, (basestring, MenuItem)) and isinstance(ele, Iterable):
                    try:
                        menuitem, submenu = ele
                    except TypeError:
                        raise ValueError('menu iterable element #{} at depth {} has length {}; must be a single '
                                         'menu item or a pair consisting of a menu item and its '
                                         'submenu'.format(n, depth, len(tuple(ele))))
                    menuitem = MenuItem(menuitem)
                    menu.add(menuitem)
                    parse_menu(submenu, menuitem, depth+1)

                # menu item / could be visual separator where ele is None or separator
                else:
                    menu.add(ele)
        parse_menu(iterable, self, 0)
        parse_menu(kwargs, self, 0)

    # ListDict insertion methods
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def insert_after(self, existing_key, menuitem):
        key, menuitem = self._process_new_menuitem(self._choose_key, menuitem)
        self._insert_helper(existing_key, key, menuitem, 1)
        super(Menu, self).insert_after(existing_key, (key, menuitem))

    def insert_before(self, existing_key, menuitem):
        key, menuitem = self._process_new_menuitem(self._choose_key, menuitem)
        self._insert_helper(existing_key, key, menuitem, 0)
        super(Menu, self).insert_before(existing_key, (key, menuitem))

    def _insert_helper(self, existing_key, key, menuitem, pos):
        if existing_key == key:  # this would mess stuff up...
            raise ValueError('same key provided for location and insertion')
        existing_menuitem = self[existing_key]
        index = self._menu.indexOfItem_(existing_menuitem._menuitem)
        self._menu.insertItem_atIndex_(menuitem._menuitem, index + pos)

    # Processing MenuItems
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _process_new_menuitem(self, key, value):
        if value is None:
            value = separator

        if value is not separator:
            value = MenuItem(value)  # safely convert if not already MenuItem
            if key is self._choose_key:
                key = value.title
            if key != value.title:
                _log('WARNING: key {} is not the same as the title of the corresponding MenuItem {}; while this would '
                     'occur if the title is dynamically altered, having different names at the time of menu creation '
                     'may not be desired '.format(repr(key), repr(value.title)))
        else:
            value = SeparatorMenuItem()
            if key is self._choose_key:
                key = 'separator_' + str(self._separators)
                self._separators += 1

        return key, value


class MenuItemCallbackHolder(NSObject):

    _instance = None
    _ns_to_py_and_callback = {}

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.alloc().init()
        return cls._instance

    def callback_(self, nsmenuitem):
        iteminstance, callback = self._ns_to_py_and_callback[nsmenuitem]
        _log(iteminstance)
        return _call_as_function_or_method(callback, iteminstance)


class MenuItem(Menu):
    """
    Python-Objective-C NSMenuItem -> MenuItem: Encapsulates and abstracts NSMenuItem (and possibly NSMenu as a submenu).

    OrderedDict subclassing enables remembering order of items added to menu and has constant time lookup.

    Because of the quirks of PyObjC, a class level dictionary is required in order to have callback_ be a @classmethod.
    And we need callback_ to be class level because we can't use instances of MenuItem in setTarget_ method of
    NSMenuItem. Otherwise this would be much more straightfoward like Timer class.

    So the target is always the MenuItem class and action is always the @classmethod callback_ -- for every function
    decorated with @clicked(...). All we do is lookup the MenuItem instance and the user-provided callback function
    based on the NSMenuItem (the only argument passed to callback_).
    """

    def __new__(cls, *args, **kwargs):
        if args and isinstance(args[0], MenuItem):  # can safely wrap MenuItem instances
            return args[0]
        return super(MenuItem, cls).__new__(cls, *args, **kwargs)

    def __init__(self, title, callback=None, key='', icon=None, dimensions=None):
        if isinstance(title, MenuItem):  # don't initialize already existing instances
            return
        self._holder = MenuItemCallbackHolder.instance()
        self._menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(str(title), None, '')
        if callable(callback):
            self.set_callback(callback, key)
        self._menu = self._icon = None
        self.set_icon(icon, dimensions)
        super(MenuItem, self).__init__()

    def __setitem__(self, key, value):
        if self._menu is None:
            self._menu = NSMenu.alloc().init()
            self._menuitem.setSubmenu_(self._menu)
        super(MenuItem, self).__setitem__(key, value)

    def __repr__(self):
        try:
            callback = MenuItemCallbackHolder._ns_to_py_and_callback[self._menuitem][1]
        except KeyError:
            callback = None
        return '<{}: [{} -> {}; callback: {}]>'.format(type(self).__name__, repr(self.title), map(str, self),
                                                       repr(callback))

    @property
    def title(self):
        return self._menuitem.title()

    @title.setter
    def title(self, new_title):
        new_title = str(new_title)
        self._menuitem.setTitle_(new_title)

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, icon_path):
        self.set_icon(icon_path)

    def set_icon(self, icon_path, dimensions=None):
        if icon_path is None:
            return
        if dimensions is not None and len(dimensions) != 2:
            dimensions = None
        image = _nsimage_from_file(icon_path, dimensions)
        self._icon = image
        self._menuitem.setImage_(image)

    @property
    def state(self):
        return self._menuitem.state()

    @state.setter
    def state(self, new_state):
        self._menuitem.setState_(new_state)

    def set_callback(self, callback, key=''):
        MenuItemCallbackHolder._ns_to_py_and_callback[self._menuitem] = self, callback
        self._menuitem.setAction_('callback:')
        self._menuitem.setTarget_(self._holder)
        self._menuitem.setKeyEquivalent_(key)


class SeparatorMenuItem(object):
    def __init__(self):
        self._menuitem = NSMenuItem.separatorItem()


class Timer(object):
    """
    Python abstraction of an event timer in a new thread for application. Serves as container for ObjC objects,
    callback function, and starting point for thread.
    """
    def __init__(self, callback, interval):
        self.set_callback(callback)
        self._interval = interval
        self._status = False

    def __call__(self):
        return self._nstimer

    def __repr__(self):
        return ('<{}: [callback: {}; interval: {}; '
                'status: {}]>').format(type(self).__name__, repr(getattr(self, '*callback').__name__),
                                       self._interval, 'ON' if self._status else 'OFF')

    @property
    def interval(self):
        return self._interval  # self._nstimer.timeInterval() when active but could be inactive

    @interval.setter
    def interval(self, new_interval):
        if self._status:
            if abs(self._nsdate.timeIntervalSinceNow()) >= self._nstimer.timeInterval():
                self.stop()
                self._interval = new_interval
                self.start()
        else:
            self._interval = new_interval

    @property
    def callback(self):
        return getattr(self, '*callback')

    def is_alive(self):
        return self._status

    def start(self):
        if not self._status:
            self._nsdate = NSDate.date()
            self._nstimer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(
                self._nsdate, self._interval, self, 'callback:', None, True)
            NSRunLoop.currentRunLoop().addTimer_forMode_(self._nstimer, NSDefaultRunLoopMode)
            _TIMERS.add(self)
            self._status = True

    def stop(self):
        if self._status:
            self._nstimer.invalidate()
            del self._nstimer
            del self._nsdate
            self._status = False

    def set_callback(self, callback):
        setattr(self, '*callback', callback)

    def callback_(self, _):
        _log(self)
        return _call_as_function_or_method(getattr(self, '*callback'), self)


class Window(object):
    """
    Window class for consuming user input.
    """
    def __init__(self, message, title='', default_text='', ok=None, cancel=False, dimensions=(320, 160)):
        message = str(message)
        title = str(title)
        self._default_text = default_text
        self._cancel = bool(cancel)
        self._icon = None

        self._alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
            title, ok, 'Cancel' if cancel else None, None, message)
        self._alert.setAlertStyle_(0)  # informational style

        self._textfield = NSTextField.alloc().initWithFrame_(NSMakeRect(0, 0, *dimensions))
        self._textfield.setSelectable_(True)
        if default_text:
            self._textfield.setStringValue_(default_text)
        self._alert.setAccessoryView_(self._textfield)

    @property
    def title(self):
        return self._alert.messageText()

    @title.setter
    def title(self, new_title):
        new_title = str(new_title)
        self._alert.setMessageText_(new_title)

    @property
    def message(self):
        return self._alert.informativeText()

    @message.setter
    def message(self, new_message):
        new_message = str(new_message)
        self._alert.setInformativeText_(new_message)

    @property
    def default_text(self):
        return self._default_text

    @default_text.setter
    def default_text(self, new_text):
        new_text = str(new_text)
        self._default_text = new_text
        self._textfield.setStringValue_(new_text)

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, icon_path):
        new_icon = _nsimage_from_file(icon_path)
        self._icon = icon_path
        self._alert.setIcon_(new_icon)

    def add_button(self, name):
        name = str(name)
        self._alert.addButtonWithTitle_(name)

    def add_buttons(self, iterable=None, *args):
        if iterable is None:
            return
        if isinstance(iterable, basestring):
            self.add_button(iterable)
        else:
            for ele in iterable:
                self.add_button(ele)
        for arg in args:
            self.add_button(arg)

    def run(self):
        _log(self)
        clicked = self._alert.runModal() % 999
        if clicked > 2 and self._cancel:
            clicked -= 1
        self._textfield.validateEditing()
        text = self._textfield.stringValue()
        self.default_text = self._default_text  # reset default text
        return Response(clicked, text)


class Response(object):
    def __init__(self, clicked, text):
        self._clicked = clicked
        self._text = text

    def __repr__(self):
        shortened_text = self._text if len(self._text) < 21 else self._text[:17] + '...'
        return '<{}: [clicked: {}, text: {}]>'.format(type(self).__name__, self._clicked, repr(shortened_text))

    @property
    def clicked(self):
        return self._clicked

    @property
    def text(self):
        return self._text


class NSApp(NSObject):
    """
    Objective C delegate class for NSApplication. Don't instantiate - use App instead.
    """
    def userNotificationCenter_didActivateNotification_(self, notification_center, notification):
        notification_center.removeDeliveredNotification_(notification)
        data = dict(notification.userInfo())
        try:
            _call_as_function_or_method(getattr(notifications, '*notification_center'), data)
        except AttributeError:  # notification center function not specified -> no error but warning in log
            _log('WARNING: notification received but no function specified for answering it; use @notifications '
                 'decorator to register a function.')

    def initializeStatusBar(self):
        self.nsstatusitem = NSStatusBar.systemStatusBar().statusItemWithLength_(-1)  # variable dimensions
        self.nsstatusitem.setHighlightMode_(True)

        if self._app['_icon'] is not None:
            self.setStatusBarIcon()
            _log('creating icon')
            if self._app['_title'] is not None:
                self.setStatusBarTitle()
        else:
            self.setStatusBarTitle()

        mainmenu = self._app['_menu']
        mainmenu.add('Quit')
        mainmenu['Quit']._menuitem.setAction_('terminate:')  # _menuitem attribute is NSMenuItem
        self.nsstatusitem.setMenu_(mainmenu._menu)  # mainmenu of our status bar spot (_menu attribute is NSMenu)

    def setStatusBarTitle(self):
        self.nsstatusitem.setTitle_(self._app['_title'] if self._app['_title'] is not None else self._app['_name'])

    def setStatusBarIcon(self):
        self.nsstatusitem.setImage_(_nsimage_from_file(self._app['_icon']))


class App(object):
    """
    App class provides a simple and pythonic iterface for all those long and ugly PyObjC calls. Serves as a setup
    class for NSApp since Objective C classes shouldn't be instantiated normally. This is the most user-friendly
    way.
    """
    def __init__(self, name, title=None, icon=None, menu=None):
        self._name = str(name)
        self._icon = self._title = None
        self.icon = icon
        self.title = title
        self._menu = Menu()
        if menu is not None:
            self.menu = menu
        self._application_support = application_support(self._name)

    # Properties
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @property
    def name(self):
        return self._name

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if title is None:
            return
        self._title = str(title)
        try:
            self._nsapp.setStatusBarTitle()
        except AttributeError:
            pass

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, icon_path):
        if icon_path is None:
            return
        self._icon = icon_path
        try:
            self._nsapp.setStatusBarIcon()
        except AttributeError:
            pass

    @property
    def menu(self):
        return self._menu

    @menu.setter
    def menu(self, iterable):
        self._menu.update(iterable)

    # Open files in application support folder
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def open(self, *args):
        return open(os.path.join(self._application_support, args[0]), *args[1:])

    # Run the application
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def run(self):
        """
        Perform various setup tasks then start application run loop.
        """
        nsapplication = NSApplication.sharedApplication()
        nsapplication.activateIgnoringOtherApps_(True)  # NSAlerts in front
        self._nsapp = NSApp.alloc().init()
        self._nsapp._app = self.__dict__  # allow for dynamic modification based on this App instance
        self._nsapp.initializeStatusBar()
        nsapplication.setDelegate_(self._nsapp)
        NSUserNotificationCenter.defaultUserNotificationCenter().setDelegate_(self._nsapp)

        setattr(App, '*app_instance', self)  # class level ref to running instance (for passing self to App subclasses)
        t = b = None
        for t in getattr(timer, '*timers', []):
            t.start()
        for b in getattr(clicked, '*buttons', []):
            b(self)  # we waited on registering clicks so we could pass self to access _menu attribute
        del t, b

        AppHelper.runEventLoop()
        sys.exit(0)
