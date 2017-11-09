#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# rumps: Ridiculously Uncomplicated macOS Python Statusbar apps.
# Copyright: (c) 2017, Jared Suttles. All rights reserved.
# License: BSD, see LICENSE for details.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
try:  # Python 2.7+,
    from test.support import import_fresh_module
    pyCollections = import_fresh_module('collections', blocked=['_collections'])
    _OrderedDict, _Link = pyCollections.OrderedDict, pyCollections._Link
except ImportError:
    from .packages.ordereddict import OrderedDict as _OrderedDict


# ListDict: OrderedDict subclass with insertion methods for modifying the order of the linked list in O(1) time
# https://gist.github.com/jaredks/6276032
class ListDict(_OrderedDict):
    def __insertion(self, link_prev, key_value):
        key, value = key_value
        if link_prev.key != key:
            if key in self:
                del self[key]
            link_next = link_prev.next
            new_link = _Link()
            new_link.prev, new_link.next, new_link.key = link_prev, link_next, key
            self._OrderedDict__map[key] = link_prev.next = link_next.prev = new_link
        dict.__setitem__(self, key, value)

    def insert_after(self, existing_key, key_value):
        self.__insertion(self._OrderedDict__map[existing_key], key_value)

    def insert_before(self, existing_key, key_value):
        self.__insertion(self._OrderedDict__map[existing_key].prev, key_value)
