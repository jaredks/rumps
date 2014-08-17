#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# rumps: Ridiculously Uncomplicated OS X Python Statusbar apps.
# Copyright: (c) 2014, Jared Suttles. All rights reserved.
# License: BSD, see LICENSE for details.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

"""
rumps
=====

Ridiculously Uncomplicated OS X Python Statusbar apps.

rumps exposes Objective-C classes as Python classes and functions which greatly simplifies the process of creating a
statusbar application.
"""

__title__ = 'rumps'
__version__ = '0.2.0'
__author__ = 'Jared Suttles'
__license__ = 'Modified BSD'
__copyright__ = 'Copyright 2014 Jared Suttles'

from .rumps import (separator, debug_mode, alert, notification, application_support, timers, quit_application, timer,
                    clicked, notifications, MenuItem, Timer, Window, App)
