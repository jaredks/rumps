# -*- coding: utf-8 -*-
"""
rumps.utils
~~~~~~~~~~~

xxx

"""

import os
import sys

import Foundation

from . import compat
from .packages.ordereddict import OrderedDict as _OrderedDict


# ListDict: OrderedDict subclass with insertion methods for modifying the order of the linked list in O(1) time
# https://gist.github.com/jaredks/6276032
class ListDict(_OrderedDict):
    def __insertion(self, link_prev, key_value):
        key, value = key_value
        if link_prev[2] != key:
            if key in self:
                del self[key]
            link_next = link_prev[1]
            self._OrderedDict__map[key] = link_prev[1] = link_next[0] = [link_prev, link_next, key]
        dict.__setitem__(self, key, value)

    def insert_after(self, existing_key, key_value):
        self.__insertion(self._OrderedDict__map[existing_key], key_value)

    def insert_before(self, existing_key, key_value):
        self.__insertion(self._OrderedDict__map[existing_key][0], key_value)


class EventEmitter(object):
    def __init__(self, name):
        self.name = name
        self.callbacks = set()

    def register(self, func):
        self.callbacks.add(func)

    def unregister(self, func):
        try:
            self.callbacks.remove(func)
            return True
        except KeyError:
            return False

    def emit(self, *args, **kwargs):
        print 'EventEmitter("%s").emit called' % self.name
        for callback in self.callbacks:
            try:
                callback(*args, **kwargs)
            except Exception:
                import traceback
                traceback.print_exc()
                # TODO: log?

    __call__ = register


def application_support(name):
    """Return the application support folder path for the given `name`,
    creating it if it doesn't exist.
    """
    app_support_path = os.path.join(Foundation.NSSearchPathForDirectoriesInDomains(14, 1, 1).objectAtIndex_(0), name)
    if not os.path.isdir(app_support_path):
        os.mkdir(app_support_path)
    return app_support_path


def debug_mode(choice):
    """Enable or disable printing helpful information for debugging the
    program. Default is off.
    """
    app = current_app()
    app.debug_mode = choice


def log(*args, **kwargs):
    """xxx
    """
    separator = kwargs.get('separator', ' ')
    Foundation.NSLog(separator.join(map(compat.text_type, args)))


def getattr_failover(obj, attrs):
    for attr in attrs:
        try:
            return getattr(obj, attr)
        except AttributeError:
            pass
    raise


# TODO
def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2 ,4))
