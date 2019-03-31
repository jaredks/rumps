# -*- coding: utf-8 -*-

import AppKit

from .. import _internal
from .. import compat
from .. import utils


class Window(object):
    """Generate a window to interact with the user. Can display information and
    consume user input. Rendering can be customized by assembling UI components
    within the window's :attr:`view`.

    .. versionadded:: 0.4.0

    :param message: the text positioned below the `title` in smaller font. If
        not a string, will use the string representation of the object.
    :param title: the text positioned at the top of the window in larger font.
        If not a string, will use the string representation of the object.
    :param ok: the text for the "ok" button. Must be either a string or
        ``None``. If ``None``, a default localized button title will be used.
    :param cancel: the text for the "cancel" button. If a string, the button
        will have that text. If `cancel` evaluates to ``True``, will create a
        button with text "Cancel". Otherwise, this button will not be created.
    """

    def __init__(self, **options):
        message = options.get('message', '')
        title = options.get('title', '')
        ok = options.get('ok')
        cancel = options.get('cancel')

        self._cancel = bool(cancel)
        self._icon = None

        _internal._require_string_or_none(ok)
        if not isinstance(cancel, compat.string_types):
            cancel = 'Cancel' if cancel else None

        self._ns = AppKit.NSAlert.alloc().init()

        '''
        .alert
        defaultButton_
        alternateButton_
        otherButton_
        (
            ok,
            cancel,
            None,
        )
        '''

        self.style = 'INFO'
        self.title = title
        self.message = message
        self._view = None

    # TODO: keep?
    @property
    def style(self):
        """xxx
        """
        style_enum = self._ns.alertStyle()
        if style_enum == 0:
            return 'WARNING'
        elif style_enum == 1:
            return 'INFORMATIONAL'
        elif style_enum == 2:
            return 'CRITICAL'

    @style.setter
    def style(self, value):
        if value in ('INFO', 'INFORMATION', 'INFORMATIONAL'):
            self._ns.setAlertStyle_(1)
        elif value in ('WARN', 'WARNING'):
            self._ns.setAlertStyle_(0)
        elif value in ('CRIT', 'CRITICAL'):
            self._ns.setAlertStyle_(2)
        else:
            raise ValueError('invalid style "%s"' % value)

    @property
    def title(self):
        """The text positioned at the top of the window in larger font. If not
        a string, will use the string representation of the object.
        """
        return self._ns.messageText()

    @title.setter
    def title(self, value):
        value = compat.text_type(value)
        self._ns.setMessageText_(value)

    @property
    def message(self):
        """The text positioned below the :attr:`title` in smaller font. If not
        a string, will use the string representation of the object.
        """
        return self._ns.informativeText()

    @message.setter
    def message(self, value):
        value = compat.text_type(value)
        self._ns.setInformativeText_(value)

    @property
    def icon(self):
        """The path to an image displayed for this window. If set to ``None``,
        will default to the icon for the application using
        :attr:`rumps.App.icon`.

        .. versionchanged:: 0.2.0
           If the icon is set to an image then changed to ``None``, it will
           correctly be changed to the application icon.

        """
        return self._icon

    # TODO
    def set_icon(self, icon_path):
        new_icon = Image.from_file(icon_path) if icon_path is not None else None
        self._icon = icon_path
        self._ns.setIcon_(new_icon._ns)

    # TODO
    def buttons(self):
        return self._ns.buttons()

    def add_button(self, name):
        """Create a new button.

        The button displayed rightmost in the alert (for a left-to-right language) corresponds to the button at index 0 in this property’s array, and is considered the default button. A user can invoke this button by pressing the Return key.

        Any button with a title of “Cancel” has a key equivalent of Escape, and any button with the title “Don’t Save” has a key equivalent of Command-D (but only if it is not the first button). You can also assign different key equivalents for the buttons using the keyEquivalent method of the NSButton class.

        .. versionchanged:: 0.2.0
           The `name` parameter is required to be a string.

        :param name: the text for a new button. Must be a string.
        """
        _require_string(name)
        self._ns.addButtonWithTitle_(name)

    def add_buttons(self, iterable=None, *args):
        """Create multiple new buttons.

        .. versionchanged:: 0.2.0
           Since each element is passed to :meth:`rumps.Window.add_button`,
           they must be strings.

        """
        if iterable is None:
            return
        if isinstance(iterable, compat.string_types):
            self.add_button(iterable)
        else:
            for ele in iterable:
                self.add_button(ele)
        for arg in args:
            self.add_button(arg)

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, value):
        ns = value._ns
        value._parent = self
        self._ns.setAccessoryView_(ns)
        self._view = value

    def layout(self):
        """xxx"""
        self._ns.layout()

    @property
    def x(self):
        return self._ns.window().frame().origin.x

    @x.setter
    def x(self, value):
        ns_window = self._ns.window()
        ns_rect = Foundation.NSMakeRect(value, self.y, self.width, self.height)
        ns_window.setFrame_display_(ns_rect, True)

    @property
    def y(self):
        return self._ns.window().frame().origin.y

    @y.setter
    def y(self, value):
        self._ns.setFrameOrigin_(AppKit.NSPoint(self.x, value))

    @property
    def width(self):
        return self._ns.window().frame().size.width

    @width.setter
    def width(self, value):
        self._ns.setFrameSize_(AppKit.NSSize(value, self.height))

    @property
    def height(self):
        return self._ns.window().frame().size.height

    @height.setter
    def height(self, value):
        ns_window = self._ns.window()
        ns_rect = Foundation.NSMakeRect(self.x, self.y, self.width, value)
        ns_window.setFrame_display_(ns_rect, True)

    def run(self):
        """Launch the window. :class:`rumps.ui.Window` instances can be reused
        to retrieve user input as many times as needed.

        :return: a :class:`rumps.ui.Response` object that contains the text
        and the button clicked as an integer.
        """
        utils.log('running window', self)
        result = self._ns.runModal()
        print '>>>', result
        clicked = result % 999
        if clicked > 2 and self._cancel:
            clicked -= 1
        return Response(clicked)


class Response(object):
    """Holds information from user interaction with a :class:`rumps.Window`
    after it has been closed.
    """

    def __init__(self, clicked):
        self._clicked = clicked

    def __repr__(self):
        return '<{0}: [clicked: {1}]>'.format(type(self).__name__, self._clicked)

    @property
    def clicked(self):
        """Return a number representing the button pressed by the user.

        The "ok" button will return ``1`` and the "cancel" button will return
        ``0``. This makes it convenient to write a conditional like,

        .. code-block:: python

            if response.clicked:
                do_thing_for_ok_pressed()
            else:
                do_thing_for_cancel_pressed()

        Where `response` is an instance of :class:`rumps.ui.Response`.

        Additional buttons added using methods
        :meth:`rumps.ui.Window.add_button` and
        :meth:`rumps.ui.Window.add_buttons` will return ``2``, ``3``, ... in
        the order they were added.
        """
        return self._clicked


def alert(title=None, message='', ok=None, cancel=None, other=None, icon_path=None):
    """Generate a simple alert window.

    .. versionchanged:: 0.2.0
        Providing a `cancel` string will set the button text rather than only using text "Cancel". `title` is no longer
        a required parameter.

    .. versionchanged:: 0.3.0
        Add `other` button functionality as well as `icon_path` to change the alert icon.

    :param title: the text positioned at the top of the window in larger font. If ``None``, a default localized title
                  is used. If not ``None`` or a string, will use the string representation of the object.
    :param message: the text positioned below the `title` in smaller font. If not a string, will use the string
                    representation of the object.
    :param ok: the text for the "ok" button. Must be either a string or ``None``. If ``None``, a default
               localized button title will be used.
    :param cancel: the text for the "cancel" button. If a string, the button will have that text. If `cancel`
                   evaluates to ``True``, will create a button with text "Cancel". Otherwise, this button will not be
                   created.
    :param other: the text for the "other" button. If a string, the button will have that text. Otherwise, this button will not be
                   created.
    :param icon_path: a path to an image. If ``None``, the applications icon is used.
    :return: a number representing the button pressed. The "ok" button is ``1`` and "cancel" is ``0``.
    """
    message = compat.text_type(message)
    #message = message.replace('%', '%%')
    if title is not None:
        title = compat.text_type(title)
    _internal._require_string_or_none(ok)
    if not isinstance(cancel, compat.string_types):
        cancel = 'Cancel' if cancel else None
    alert = AppKit.NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
        title, ok, cancel, other, message)
    alert.setAlertStyle_(0)  # informational style
    if icon_path is not None:
        icon = Image.from_file(icon_path)
        alert.setIcon_(icon)
    #utils.log('alert opened with message: {0}, title: {1}'.format(repr(message), repr(title)))
    return alert.runModal()
