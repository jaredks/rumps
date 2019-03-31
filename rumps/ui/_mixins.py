# -*- coding: utf-8 -*-

import AppKit


class Interactable(object):

    #: The function to be called in response to a right click event on this UI
    #: component.
    right_click = None

    def on_right_click(self, callback):
        """Set the function serving as callback for when a right click event
        occurs on this UI component.

        :param callback: the function to be called.
        """
        self.right_click = callback


class Component(Interactable):
    """xxx

    :param x: xxx
    :param y: xxx
    :param height: xxx
    :param width: xxx
    :param callback: the function serving as callback for when an interaction
        event occurs on this component.
    """

    def set_frame(self, **options):
        """xxx"""
        self.x = options.get('x', 0)
        self.y = options.get('y', 0)
        self.width = options.get('width', self.DEFAULT_WIDTH)
        self.height = options.get('height', self.DEFAULT_HEIGHT)

    def set_size(self, dimensions):
        """xxx"""
        self._ns.setFrameSize_(AppKit.NSSize(*dimensions))

    def set_position(self, point):
        """xxx"""
        self._ns.setFrameOrigin_(AppKit.NSPoint(*point))

    @property
    def x(self):
        return self._ns.frame().origin.x

    @x.setter
    def x(self, value):
        # TODO: prohibit when parent is auto?
        self._ns.setFrameOrigin_(AppKit.NSPoint(value, self.y))

    @property
    def y(self):
        return self._ns.frame().origin.y

    @y.setter
    def y(self, value):
        # TODO: prohibit when parent is auto?
        self._ns.setFrameOrigin_(AppKit.NSPoint(self.x, value))

    @property
    def width(self):
        return self._ns.frame().size.width

    @width.setter
    def width(self, value):
        #if getattr(self, 'auto_width', False):
        #    raise exceptions.UIError(
        #        'cannot explicitly set width when auto_width is true'
        #    )
        self._ns.setFrameSize_(AppKit.NSSize(value, self.height))
        if self.parent:
            self.parent.layout()

    @property
    def height(self):
        return self._ns.frame().size.height

    @height.setter
    def height(self, value):
        #if getattr(self, 'auto_height', False):
        #    raise exceptions.UIError(
        #        'cannot explicitly set height when auto_height is true'
        #    )
        self._ns.setFrameSize_(AppKit.NSSize(self.width, value))
        if self.parent:
            print 'layout--'
            self.parent.layout()

    @property
    def parent(self):
        # TODO: use weakref of python object linked to superview() call?
        try:
            return self._parent
        except AttributeError:
            return None


class Actionable(object):

    #: The function to be called in response to a user interaction event.
    callback = None

    def set_callback(self, callback):
        """Set the function serving as callback for when a user interaction
        occurs on this UI component.

        :param callback: the function to be called.
        """
        self.callback = callback
        self._ns.setAction_('callback:' if callback is not None else None)
        return callback

    on_click = set_callback
