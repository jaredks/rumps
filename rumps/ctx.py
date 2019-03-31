# -*- coding: utf-8 -*-
"""
rumps.ctx
~~~~~~~~~

xxx

"""

import functools

from . import exceptions

_CTX = {}


def current_app():
    """xxx
    """
    try:
        return _CTX['app_instance']
    except KeyError:
        raise exceptions.NoCurrentApplication


def _set_current_app(app):
    _CTX['app_instance'] = app


def is_app_running():
    """xxx
    """
    return 'app_instance' in _CTX


class DeferredCalls(object):
    def __init__(self, func, **options):
        self.func = func
        self.defer_with_running_app = options.get('defer_with_running_app', False)
        self.deferred = []

        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

        _CTX.setdefault('deferred', []).append(self)

    def __repr__(self):
        return '<%s "%s">' % (type(self).__name__, self.func.__name__)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def defer(self, func, *args, **options):
        if not self.defer_with_running_app and is_app_running():
            func(*args, **options)
            return
        partial = functools.partial(func, *args, **options)
        self.deferred.append(partial)

    def fire(self):
        current_app()
        for call in self.deferred:
            call()


def deferred_fire():
    for deferred in _CTX.get('deferred', []):
        # TODO: log(deferred)
        for x in deferred.deferred:
            x()
