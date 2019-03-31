# -*- coding: utf-8 -*-
"""
rumps._objc
~~~~~~~~~~~

Extend PyObjC classes to add hooks and allow referencing the wrapper object via
an instance attribute. This module is "low-level" - each class is meant to be
used through the corresponding wrapper class.

"""

import traceback
import weakref

import AppKit

from . import _internal
from . import utils


def associate(ns, py):
    ns._py = weakref.ref(py)
    ns.setTarget_(ns)


@classmethod
def create_(cls, py):
    ns = cls.alloc().init()
    associate(ns, py)
    return ns


def callback_(self, ns):
    py_ref = ns._py
    py = py_ref()
    if py is None:
        # TODO: log.error
        utils.log('PYTHON OBJECT GCed BUT NS OBJECT STILL EXISTS AND HAD CALLBACK RUN')
    else:
        callback = py.callback
        utils.log('callback', callback, 'for', py)
        if callback:
            try:
                return _internal._call_as_function_or_method(callback, py)
            except Exception:
                utils.log(traceback.format_exc())


class CallbackManager(object):
    callback_ = callback_


def rightMouseDown_(self, event):
    print 'rightMouseDown_'
    py = self._py()
    try:
        callback = py.right_click
    except AttributeError:
        pass
    else:
        try:
            return _internal._call_as_function_or_method(callback, py)
        except Exception:
            utils.log(traceback.format_exc())


class RumpsNSTextField(AppKit.NSTextField):

    create_ = create_
    callback_ = callback_

    '''
    def mouseDown_(self, event):
        print 'MOUSE DOWN', self, event
    '''


class RumpsNSPopUpButton(AppKit.NSPopUpButton):
    create_ = create_
    callback_ = callback_
    rightMouseDown_ = rightMouseDown_


class RumpsNSSlider(AppKit.NSSlider):
    create_ = create_
    callback_ = callback_
    rightMouseDown_ = rightMouseDown_


class RumpsNSButton(AppKit.NSButton):
    create_ = create_
    callback_ = callback_
    rightMouseDown_ = rightMouseDown_

    #def mouseDown_(self, event):
    #    print 'mouseDown_', self, event

    def mouseEntered_(self, event):
        print 'mouseEntered_', self, event


class RumpsNSMenuItem(AppKit.NSMenuItem):
    create_ = create_
    callback_ = callback_
