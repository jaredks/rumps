# -*- coding: utf-8 -*-
"""
rumps.menus
~~~~~~~~~~~

xxx

"""

from collections import Mapping, Iterable

import AppKit

from . import _internal
from . import _objc
from . import compat
from . import ui

from .compat import text_type
from .utils import ListDict
from .images import Image

separator = object()


class Menu(ListDict):
    """Wrapper for Objective-C's NSMenu class.

    Implements core functionality of menus in rumps. :class:`rumps.MenuItem` subclasses `Menu`.
    """

    # NOTE:
    # Only ever used as the main menu since every other menu would exist as a submenu of a MenuItem

    _choose_key = object()

    def __init__(self):
        self._counts = {}
        if not hasattr(self, '_menu'):
            self._menu = AppKit.NSMenu.alloc().init()
        super(Menu, self).__init__()

    def __setitem__(self, key, value):
        if key not in self:
            key, value = self._process_new_menuitem(key, value)
            self._menu.addItem_(value._menuitem)
            super(Menu, self).__setitem__(key, value)

    def __delitem__(self, key):
        value = self[key]
        self._menu.removeItem_(value._menuitem)
        super(Menu, self).__delitem__(key)

    def add(self, menuitem):
        """Adds the object to the menu as a :class:`rumps.MenuItem` using the :attr:`rumps.MenuItem.title` as the
        key. `menuitem` will be converted to a `MenuItem` object if not one already.
        """
        self.__setitem__(self._choose_key, menuitem)

    def clear(self):
        """Remove all `MenuItem` objects from within the menu of this `MenuItem`."""
        self._menu.removeAllItems()
        super(Menu, self).clear()

    def copy(self):
        raise NotImplementedError

    @classmethod
    def fromkeys(cls, *args, **kwargs):
        raise NotImplementedError

    def update(self, iterable, **kwargs):
        """Update with objects from `iterable` after each is converted to a :class:`rumps.MenuItem`, ignoring
        existing keys. This update is a bit different from the usual ``dict.update`` method. It works recursively and
        will parse a variety of Python containers and objects, creating `MenuItem` object and submenus as necessary.

        If the `iterable` is an instance of :class:`rumps.MenuItem`, then add to the menu.

        Otherwise, for each element in the `iterable`,

            - if the element is a string or is not an iterable itself, it will be converted to a
              :class:`rumps.MenuItem` and the key will be its string representation.
            - if the element is a :class:`rumps.MenuItem` already, it will remain the same and the key will be its
              :attr:`rumps.MenuItem.title` attribute.
            - if the element is an iterable having a length of 2, the first value will be converted to a
              :class:`rumps.MenuItem` and the second will act as the submenu for that `MenuItem`
            - if the element is an iterable having a length of anything other than 2, a ``ValueError`` will be raised
            - if the element is a mapping, each key-value pair will act as an iterable having a length of 2

        """
        def parse_menu(iterable, menu, depth):
            if isinstance(iterable, MenuItem):
                menu.add(iterable)
                return

            for n, ele in enumerate(compat.iteritems(iterable) if isinstance(iterable, Mapping) else iterable):

                # for mappings we recurse but don't drop down a level in the menu
                if not isinstance(ele, MenuItem) and isinstance(ele, Mapping):
                    parse_menu(ele, menu, depth)

                # any iterables other than strings and MenuItems
                elif not isinstance(ele, (compat.string_types, MenuItem)) and isinstance(ele, Iterable):
                    try:
                        menuitem, submenu = ele
                    except TypeError:
                        raise ValueError('menu iterable element #{0} at depth {1} has length {2}; must be a single '
                                         'menu item or a pair consisting of a menu item and its '
                                         'submenu'.format(n, depth, len(tuple(ele))))
                    menuitem = MenuItem(menuitem)
                    menu.add(menuitem)
                    parse_menu(submenu, menuitem, depth+1)

                # menu item / could be visual separator where ele is None or separator
                else:
                    menu.add(ele)
        parse_menu(iterable, self, 0)
        parse_menu(kwargs, self, 0)

    # ListDict insertion methods
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def insert_after(self, existing_key, menuitem):
        """Insert a :class:`rumps.MenuItem` in the menu after the `existing_key`.

        :param existing_key: a string key for an existing `MenuItem` value.
        :param menuitem: an object to be added. It will be converted to a `MenuItem` if not one already.
        """
        key, menuitem = self._process_new_menuitem(self._choose_key, menuitem)
        self._insert_helper(existing_key, key, menuitem, 1)
        super(Menu, self).insert_after(existing_key, (key, menuitem))

    def insert_before(self, existing_key, menuitem):
        """Insert a :class:`rumps.MenuItem` in the menu before the `existing_key`.

        :param existing_key: a string key for an existing `MenuItem` value.
        :param menuitem: an object to be added. It will be converted to a `MenuItem` if not one already.
        """
        key, menuitem = self._process_new_menuitem(self._choose_key, menuitem)
        self._insert_helper(existing_key, key, menuitem, 0)
        super(Menu, self).insert_before(existing_key, (key, menuitem))

    def _insert_helper(self, existing_key, key, menuitem, pos):
        if existing_key == key:  # this would mess stuff up...
            raise ValueError('same key provided for location and insertion')
        existing_menuitem = self[existing_key]
        index = self._menu.indexOfItem_(existing_menuitem._menuitem)
        self._menu.insertItem_atIndex_(menuitem._menuitem, index + pos)

    # Processing MenuItems
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _process_new_menuitem(self, key, value):
        if value is None or value is separator:
            value = SeparatorMenuItem()

        if not hasattr(value, '_menuitem'):
            value = MenuItem(value)

        if key is self._choose_key:
            if hasattr(value, 'title'):
                key = value.title
            else:
                cls = type(value)
                count = self._counts[cls] = self._counts.get(cls, 0) + 1
                key = '%s_%d' % (cls.__name__, count)

        if hasattr(value, 'title') and key != value.title:
            _log('WARNING: key {0} is not the same as the title of the corresponding MenuItem {1}; while this '
                 'would occur if the title is dynamically altered, having different names at the time of menu '
                 'creation may not be desired '.format(repr(key), repr(value.title)))

        return key, value


class MenuItem(Menu):
    """Represents an item within the application's menu.

    A :class:`rumps.MenuItem` is a button inside a menu but it can also serve as a menu itself whose elements are
    other `MenuItem` instances.

    Encapsulates and abstracts Objective-C NSMenuItem (and possibly a corresponding NSMenu as a submenu).

    A couple of important notes:

        - A new `MenuItem` instance can be created from any object with a string representation.
        - Attempting to create a `MenuItem` by passing an existing `MenuItem` instance as the first parameter will not
          result in a new instance but will instead return the existing instance.

    Remembers the order of items added to menu and has constant time lookup. Can insert new `MenuItem` object before or
    after other specified ones.

    .. note::
       When adding a `MenuItem` instance to a menu, the value of :attr:`title` at that time will serve as its key for
       lookup performed on menus even if the `title` changes during program execution.

    :param title: the name of this menu item. If not a string, will use the string representation of the object.
    :param callback: the function serving as callback for when a click event occurs on this menu item.
    :param key: the key shortcut to click this menu item. Must be a string or ``None``.
    :param icon: a path to an image. If set to ``None``, the current image (if any) is removed.
    :param dimensions: a sequence of numbers whose length is two, specifying the dimensions of the icon.
    :param template: a boolean, specifying template mode for a given icon (proper b/w display in dark menu bar)
    """

    # NOTE:
    # Because of the quirks of PyObjC, a class level dictionary **inside an NSObject subclass for 10.9.x** is required
    # in order to have callback_ be a @classmethod. And we need callback_ to be class level because we can't use
    # instances in setTarget_ method of NSMenuItem. Otherwise this would be much more straightfoward like Timer class.
    #
    # So the target is always the NSApp class and action is always the @classmethod callback_ -- for every function
    # decorated with @clicked(...). All we do is lookup the MenuItem instance and the user-provided callback function
    # based on the NSMenuItem (the only argument passed to callback_).

    def __new__(cls, *args, **kwargs):
        if args and isinstance(args[0], MenuItem):  # can safely wrap MenuItem instances
            return args[0]
        return super(MenuItem, cls).__new__(cls, *args, **kwargs)

    def __init__(self, title, callback=None, key=None, icon=None, dimensions=None, template=None):
        if isinstance(title, MenuItem):  # don't initialize already existing instances
            return

        self._menuitem = _objc.RumpsNSMenuItem.alloc().initWithTitle_action_keyEquivalent_(text_type(title), None, '')
        _objc.associate(self._menuitem, self)
        self._menu = self._icon = None
        self._template = template
        self.set_callback(callback, key)
        self.set_icon(icon, dimensions, template)
        super(MenuItem, self).__init__()

    def __setitem__(self, key, value):
        if self._menu is None:
            self._menu = AppKit.NSMenu.alloc().init()
            self._menuitem.setSubmenu_(self._menu)
        super(MenuItem, self).__setitem__(key, value)

    def __repr__(self):
        return '<{0}: [{1} -> {2}; callback: {3}]>'.format(
            type(self).__name__,
            repr(self.title),
            list(map(str, self)),
            repr(self.callback)
        )

    @property
    def title(self):
        """The text displayed in a menu for this menu item. If not a string, will use the string representation of the
        object.
        """
        return self._menuitem.title()

    @title.setter
    def title(self, new_title):
        new_title = text_type(new_title)
        self._menuitem.setTitle_(new_title)

    @property
    def icon(self):
        """The path to an image displayed next to the text for this menu item. If set to ``None``, the current image
        (if any) is removed.

        .. versionchanged:: 0.2.0
           Setting icon to ``None`` after setting it to an image will correctly remove the icon. Returns the path to an
           image rather than exposing a `PyObjC` class.

        """
        return self._icon

    @icon.setter
    def icon(self, icon_path):
        self.set_icon(icon_path, template=self._template)

    def set_icon(self, icon_path, dimensions=None, template=None):
        """Sets the icon displayed next to the text for this menu item. If set to ``None``, the current image (if any)
        is removed. Can optionally supply `dimensions`.

        .. versionchanged:: 0.2.0
           Setting `icon` to ``None`` after setting it to an image will correctly remove the icon. Passing `dimensions`
           a sequence whose length is not two will no longer silently error.

        :param icon_path: a file path to an image.
        :param dimensions: a sequence of numbers whose length is two.
        :param template: a boolean who defines the template mode for the icon.
        """
        if icon_path is None:
            self._icon = None

        elif hasattr(icon_path, '_ns_image'):
            self._icon = icon_path

        else:
            self._icon = Image.from_file(icon_path, dimensions=dimensions, template=template)

        self._menuitem.setImage_(self._icon._ns_image if self._icon is not None else None)

    @property
    def template(self):
        """Template mode for an icon. If set to ``None``, the current icon (if any) is displayed as a color icon.
        If set to ``True``, template mode is enabled and the icon will be displayed correctly in dark menu bar mode.
        """
        return self._template

    @template.setter
    def template(self, template_mode):
        self._template = template_mode
        self.set_icon(self.icon, template=template_mode)

    @property
    def state(self):
        """The state of the menu item. The "on" state is symbolized by a check mark. The "mixed" state is symbolized
        by a dash.

        .. table:: Setting states

           =====  ======
           State  Number
           =====  ======
            ON      1
            OFF     0
           MIXED   -1
           =====  ======

        """
        return self._menuitem.state()

    @state.setter
    def state(self, new_state):
        self._menuitem.setState_(new_state)

    def set_callback(self, callback, key=None):
        """Set the function serving as callback for when a click event occurs on this menu item. When `callback` is
        ``None``, it will disable the callback function and grey out the menu item. If `key` is a string, set as the
        key shortcut. If it is ``None``, no adjustment will be made to the current key shortcut.

        .. versionchanged:: 0.2.0
           Allowed passing ``None`` as both `callback` and `key`. Additionally, passing a `key` that is neither a
           string nor ``None`` will result in a standard ``TypeError`` rather than various, uninformative `PyObjC`
           internal errors depending on the object.

        :param callback: the function to be called when the user clicks on this menu item.
        :param key: the key shortcut to click this menu item.
        """
        _internal._require_string_or_none(key)
        if key is not None:
            self._menuitem.setKeyEquivalent_(key)
        self._callback = callback
        self._menuitem.setAction_('callback:' if callback is not None else None)

    @property
    def callback(self):
        """Return the current callback function.

        .. versionadded:: 0.2.0

        """
        return self._callback

    @property
    def key(self):
        """The key shortcut to click this menu item.

        .. versionadded:: 0.2.0

        """
        return self._menuitem.keyEquivalent()


class UIMenuItem(object):
    """xxx
    """

    def __init__(self, view):
        self._menuitem = AppKit.NSMenuItem.alloc().init()
        self.view = view

    @property
    def view(self):
        """xxxx
        """
        return self._view

    @view.setter
    def view(self, value):
        ns = value._ns
        value._parent = self
        self._menuitem.setView_(ns)
        self._view = value


class SliderMenuItem(UIMenuItem):
    """Represents a slider menu item within the application's menu.

    .. versionadded:: 0.3.0

    :param value: a number for the current position of the slider.
    :param min_value: a number for the minimum position to which a slider can be moved.
    :param max_value: a number for the maximum position to which a slider can be moved.
    :param callback: the function serving as callback for when a slide event occurs on this menu item.
    :param dimensions: a sequence of numbers whose length is two, specifying the dimensions of the slider.
    """

    def __init__(self, value=50, min_value=0, max_value=100, callback=None, dimensions=(180, 15)):
        self._slider = ui.Slider(value=value, min_value=min_value, max_value=max_value)
        self._slider.set_callback(callback)
        self._slider.set_size(dimensions)

        UIMenuItem.__init__(self, self._slider)

    def __repr__(self):
        return '<{0}: [value: {1}; callback: {2}]>'.format(
            type(self).__name__,
            self.value,
            repr(self.callback)
        )

    def set_callback(self, callback):
        """Set the function serving as callback for when a slide event occurs
        on this menu item.

        :param callback: the function to be called when the user drags the
            marker on the slider.
        """
        self._slider.set_callback(callback)

    @property
    def callback(self):
        return self._slider.callback

    @property
    def value(self):
        """The current position of the slider."""
        return self._slider.value

    @value.setter
    def value(self, x):
        self._slider.value = x


class SeparatorMenuItem(object):
    """Visual separator between :class:`rumps.MenuItem` objects in the
    application menu.
    """
    def __init__(self):
        self._menuitem = AppKit.NSMenuItem.separatorItem()
