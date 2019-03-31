# -*- coding: utf-8 -*-

from . import _mixins
from .. import _internal
from .. import _objc


class Dropdown(_mixins.Component, _mixins.Actionable):
    """xxx
    """

    DEFAULT_WIDTH = 240
    DEFAULT_HEIGHT = 22

    def __init__(self, values=None, **options):
        #ns_rect = Foundation.NSMakeRect(x, y, width, height)
        #self._ns = AppKit.NSPopUpButton.alloc().initWithFrame_(ns_rect)

        self._ns = _objc.RumpsNSPopUpButton.create_(self)
        self.set_frame(**options)
        #self._ns.setFrameSize_(AppKit.NSSize(width, height))
        #self._ns.setFrameOrigin(AppKit.NSPoint(x, y))

        if values is not None:
            self.extend(values)

        self._pulls_down = False

    def __repr__(self, ):
        return (
            '%s(%s)' % (
                type(self).__name__,
                list(self)
            )
        )

    def __iter__(self):
        values = self._ns.itemTitles()
        for value in values:
            yield value

    def __getitem__(self, index):
        # TODO negative number
        _require_int(index)
        if index > len(self):
            raise IndexError('index out of range')
        return self._ns.itemTitleAtIndex_(index)

    def __setitem__(self, index, value):
        _internal._require_string(value)
        if index > len(self):
            raise IndexError('assignment index out of range')
        self._ns.insertItemWithTitle_at_(value, index)

    def __delitem__(self, index):
        _require_int(index)
        self._ns.removeItemAt_(index)

    def __len__(self):
        return self._ns.numberOfItems()

    def append(self, value):
        _internal._require_string(value)
        self._ns.addItemWithTitle_(value)

    def extend(self, values):
        _internal._require_string(*values)
        self._ns.addItemsWithTitles_(values)

    def clear(self):
        self._ns.removeAllItems()

    @property
    def pulls_down(self):
        return self._pulls_down

    @pulls_down.setter
    def pulls_down(self, value):
        value = bool(value)
        self._ns.setPullsDown_(value)
        self._pulls_down = value

    @property
    def autoenables_items(self):
        return self._autoenables_items

    @autoenables_items.setter
    def autoenables_items(self, value):
        value = bool(value)
        self._ns.setAutoenablesItems_(value)
        self._autoenables_items = value

    @property
    def selected(self):
        return self._ns.titleOfSelectedItem()

    @selected.setter
    def selected(self, value):
        _internal._require_string(value)
        self._ns.selectItemWithTitle_(value)

    @property
    def selected_index(self):
        return self._ns.indexOfSelectedItem()

    @selected_index.setter
    def selected_index(self, value):
        _require_int(value)
        self._ns.selectItemAt_(value)
