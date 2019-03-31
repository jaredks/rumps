# -*- coding: utf-8 -*-
"""
rumps
=====

Ridiculously Uncomplicated macOS Python Statusbar apps.

rumps exposes Objective-C classes as Python classes and functions which greatly
simplifies the process of creating a statusbar application.

Copyright: (c) 2019, Jared Suttles. All rights reserved.

License: BSD, see LICENSE for details.

"""

__title__ = 'rumps'
__version__ = '0.3.0.dev'
__author__ = 'Jared Suttles'
__license__ = 'Modified BSD'
__copyright__ = 'Copyright 2019 Jared Suttles'

from .app import App, quit_application
from .decorators import timer, clicked, slider, on_notification
from .menus import MenuItem, SliderMenuItem, separator, UIMenuItem
from .notifications import notification
from .timers import timers, Timer
from .utils import application_support, debug_mode

from .deprecated import Window
from . import events
from . import ui

alert = ui.alert
notifications = on_notification


# TODO
from . import text
