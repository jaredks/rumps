# -*- coding: utf-8 -*-

import AppKit

from . import _mixins
from .. import _objc


class View(_mixins.Component):
    """xxx
    """

    ROWS = object()
    COLS = object()

    DEFAULT_WIDTH = 320
    DEFAULT_HEIGHT = 160

    def __init__(self, *components, **options):
        auto   = options.get('auto', 'rows')

        auto_height = options.get('auto_height', True)
        auto_width = options.get('auto_width', True)
        if auto_height:
            height = 0
        if auto_width:
            width = 0

        self._ns = AppKit.NSView.alloc().init()
        self.set_frame(**options)

        self.auto = auto
        self.auto_height = auto_height
        self.auto_width = auto_width

        #ns_rect = Foundation.NSMakeRect(x, y, width, height)
        #self._ns = AppKit.NSView.alloc().initWithFrame_(ns_rect)

        self._components = []
        self._max_height = 0
        self._max_width = 0
        self._cb_manager = _objc.CallbackManager()

        if components:
            self.extend(components)

    def auto_rows(self):
        """x
        """
        try:
            value = self.auto.lower()
        except AttributeError:
            value = self.auto
        return value in ['row', 'rows', self.ROWS]

    def auto_cols(self):
        """x
        """
        try:
            value = self.auto.lower()
        except AttributeError:
            value = self.auto
        return value in ['col', 'cols', self.COLS]

    @property
    def max_height(self):
        return self._max_height

    @property
    def max_width(self):
        return self._max_width

    def pack_vertically(self):
        """xxx"""
        y = self.height
        for component in self:
            padding = getattr(component, 'padding', 0)
            print 'padding', padding
            component.y = y - component.height - padding
            if not self.auto_cols():
                y = component.y - padding

    def pack_horizontally(self):
        """xxx"""
        if self.auto_rows():
            return

        x = 0
        for component in self:
            component.x = x
            x += component.width

    def layout(self):
        """xxx"""
        print 'LAYOUT'
        if self.auto_rows():
            if self.auto_height:
                self.height = sum(x.height for x in self._components)
            if self.auto_width:
                self.width = self.max_width
                #self.pack_horizontally()
            self.pack_vertically()

        elif self.auto_cols():
            if self.auto_width:
                self.width = sum(x.width for x in self._components)
            if self.auto_height:
                self.height = self.max_height
                self.pack_vertically()
            self.pack_horizontally()

        self._ns.display()
        if self.parent:
            self.parent.layout()

    def _arrange(self, component, op):
        if self.auto_rows():
            if self.auto_height:
                self.height = op(self.height, component.height)
            if self.auto_width:
                self.width = self.max_width
                self.pack_horizontally()
            self.pack_vertically()

        elif self.auto_cols():
            if self.auto_width:
                self.width = op(self.width, component.width)
            if self.auto_height:
                self.height = self.max_height
                self.pack_vertically()
            self.pack_horizontally()

    def add(self, component):
        if component in self:
            return

        ns = component._ns
        component._parent = self
        self._ns.addSubview_(ns)
        self._components.append(component)
        if hasattr(component, '_after_add_to_view'):
            component._after_add_to_view(self)

        # keep track of maximum dimensions of components in this tree
        self._max_height = max(self._max_height, component.height)
        self._max_width = max(self._max_width, component.width)

        self.layout()
        #self._arrange(component, operator.add)

    def extend(self, components):
        for component in components:
            self.add(component)

    def components(self):
        for child in self._components:
            yield child

    # TODO: keep this?
    __iter__ = components

    def __contains__(self, component):
        return component in self._components

    def __getitem__(self, i):
        return self._components[i]

    def delete(self, component):
        print self._components
        print self._ns.subviews()
        try:
            i = self._components.index(component)
            del self._components[i]
        except ValueError:
            raise exceptions.UIError('does not exist in view', component, self)
        subview = self._ns.subviews()[i]
        subview.removeFromSuperview()
        self.layout()
        print self._components
        print self._ns.subviews()
