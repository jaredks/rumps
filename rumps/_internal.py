# -*- coding: utf-8 -*-
"""
rumps._internal
~~~~~~~~~~~~~~~

xxx

"""

import inspect
import traceback

import AppKit
import Foundation

from . import compat
from . import ctx
from . import events
from . import exceptions
from . import utils


def _require_string(*objs):
    for obj in objs:
        if not isinstance(obj, compat.string_types):
            raise TypeError('a string is required but given {0}, a {1}'.format(obj, type(obj).__name__))


def _require_string_or_none(*objs):
    for obj in objs:
        if not(obj is None or isinstance(obj, compat.string_types)):
            raise TypeError('a string or None is required but given {0}, a {1}'.format(obj, type(obj).__name__))


def _require_int(*objs):
    for obj in objs:
        if not isinstance(obj, compat.integer_types):
            raise TypeError('an integer is required but given {0}, a {1}'.format(obj, type(obj).__name__))


def _call_as_function_or_method(func, event):
    # The idea here is that when using decorators in a class, the functions passed are not bound so we have to
    # determine later if the functions we have (those saved as callbacks) for particular events need to be passed
    # 'self'.
    #
    # This works for an App subclass method or a standalone decorated function. Will attempt to find function as
    # a bound method of the App instance. If it is found, use it, otherwise simply call function.
    try:
        app = ctx.current_app()
    except exceptions.NoCurrentApplication:
        pass
    else:
        for name, method in inspect.getmembers(app, predicate=inspect.ismethod):
            if method.__func__ is func:
                return method(event)
    return func(event)



class Observer(Foundation.NSObject):
    def setupObservers(self):
        print 'setupObservers'

        workspace = AppKit.NSWorkspace.sharedWorkspace()
        notification_center = workspace.notificationCenter()

        notification_center.addObserver_selector_name_object_(
            self,
            self.willSleep_,
            AppKit.NSWorkspaceWillSleepNotification,
            None
        )
        notification_center.addObserver_selector_name_object_(
            self,
            self.didWake_,
            AppKit.NSWorkspaceDidWakeNotification,
            None
        )
        notification_center.addObserver_selector_name_object_(
            self,
            self.textDidBeginEditing_,
            AppKit.NSControlTextDidBeginEditingNotification,
            None
        )
        notification_center.addObserver_selector_name_object_(
            self,
            self.textDidBeginEditing_,
            AppKit.NSControlTextDidChangeNotification,
            None
        )
        notification_center.addObserver_selector_name_object_(
            self,
            self.textDidBeginEditing_,
            AppKit.NSControlTextDidEndEditingNotification,
            None
        )

    def willSleep_(self, notification):
        print 'Observer.willSleep_'
        utils.log('Observer.willSleep_')
        events.on_sleep.emit()

    def didWake_(self, notification):
        print 'Observer.didWake_'
        utils.log('Observer.didWake_')
        events.on_wake.emit()

    def textDidBeginEditing_(self, notification):
        print 'Observer.textDidBeginEditing_'
        utils.log('Observer.textDidBeginEditing_')
        print notification
        print notification.userInfo()

observer = Observer.alloc().init()
observer.setupObservers()


class NSApp(Foundation.NSObject):
    """Objective-C delegate class for NSApplication. Don't instantiate - use App instead."""

    def userNotificationCenter_didActivateNotification_(self, notification_center, notification):
        notification_center.removeDeliveredNotification_(notification)
        ns_dict = notification.userInfo()
        if ns_dict is None:
            data = None
        else:
            dumped = ns_dict['value']
            app = ctx.current_app()
            data = app.serializer.loads(dumped)

        #data['activationType'] = notification.activationType()
        #data['actualDeliveryDate'] = notification.actualDeliveryDate()

        # notification center function not specified -> no error but warning in log
        if not events.on_notification.callbacks:
            utils.log(
                'WARNING: notification received but no function specified for '
                'answering it; use @notifications decorator to register a '
                'function.'
            )
        else:
            for callback in events.on_notification.callbacks:
                try:
                    _call_as_function_or_method(callback, data)
                except Exception:
                    utils.log(traceback.format_exc())

    def initializeStatusBar(self):
        self.nsstatusitem = AppKit.NSStatusBar.systemStatusBar().statusItemWithLength_(-1)  # variable dimensions
        self.nsstatusitem.setHighlightMode_(True)

        self.setStatusBarIcon()
        self.setStatusBarTitle()

        mainmenu = self._app['_menu']
        quit_button = self._app['_quit_button']
        if quit_button is not None:
            quit_button.set_callback(self._app['_quit_application'])
            mainmenu.add(quit_button)
        else:
            utils.log(
                'WARNING: the default quit button is disabled. To exit the '
                'application gracefully, another button should have a callback '
                'of quit_application or call it indirectly.'
            )
        self.nsstatusitem.setMenu_(mainmenu._menu)  # mainmenu of our status bar spot (_menu attribute is NSMenu)

    def setStatusBarTitle(self):
        self.nsstatusitem.setTitle_(self._app['_title'])
        self.fallbackOnName()

    def setStatusBarIcon(self):
        self.nsstatusitem.setImage_(self._app['_icon_nsimage'])
        self.fallbackOnName()

    def fallbackOnName(self):
        if not (self.nsstatusitem.title() or self.nsstatusitem.image()):
            self.nsstatusitem.setTitle_(self._app['_name'])

    def applicationDidFinishLaunching_(self, notification):
        print 'applicationDidFinishLaunching_'
        #self.setupObservers()

    def applicationWillTerminate_(self, ns_notification):
        print 'applicationWillTerminate_'
        events.before_quit.emit()
