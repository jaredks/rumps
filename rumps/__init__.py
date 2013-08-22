#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# rumps: Ridiculously Uncomplicated Mac os x Python Statusbar apps.
# Copyright: (c) 2013, Jared Suttles. All rights reserved.
# License: BSD, see LICENSE for details.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

"""
rumps: Ridiculously Uncomplicated Mac os x Python Statusbar apps.

Classes:
App(name[, title[, icon[, menu]]]) --> App object representing your application
Window(message[, title[, default_text[, ok[, cancel[, dimensions]]]]]) --> Window object controlling a pop-up window
for consuming user input
Timer(callback, interval) --> Timer object that will call the function every interval seconds
MenuItem(title[, callback[, key[, icon[, dimensions]]]]) --> MenuItem object representing an item of a menu and any
associated submenu

Decorators:
@notifications --> Decorator for function dealing with incoming notifications
@clicked(*args) --> Decorator for function responding to click event on a MenuItem
@timer(interval) --> Decorator for function to be called every interval seconds

Functions:
timers() --> Returns a set of Timer objects
application_support(name) --> Returns the path to the application support folder for the given application name
notification(title[, subtitle[, message[, data[, sound]]]]) --> Sends a Mac OS X 10.8 notification
alert(title[, message[, ok[, cancel]]]) --> Opens an alert window
debug_mode(choice) --> Runs the application in debug mode with verbose output if True

"""

__title__ = 'rumps'
__version__ = '0.1.4'
__author__ = 'Jared Suttles'
__license__ = 'Modified BSD'
__copyright__ = 'Copyright 2013 Jared Suttles'

from .rumps import (separator, debug_mode, alert, notification, application_support, timers, timer, clicked,
                    notifications, MenuItem, Timer, Window, App)
