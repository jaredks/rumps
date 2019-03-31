# -*- coding: utf-8 -*-

import AppKit

from . import _mixins
from .. import _objc


class TextField(_mixins.Component, _mixins.Actionable):
    """xxx

    :param default_text: the text within the editable textbox. If not a string,
        will use the string representation of the object.
    """

    DEFAULT_WIDTH = 240
    DEFAULT_HEIGHT = 22

    def __init__(self, value=None, placeholder=None, **options):
        auto   = options.get('auto')

        self._ns = _objc.RumpsNSTextField.create_(self)
        #self._ns.setSelectable_(True)
        self._ns.setEditable_(True)

        self.set_frame(**options)

        if value:
            self.value = value
        if placeholder:
            self.placeholder = placeholder

    # TODO: rewrite docstring
    @property
    def value(self):
        """The text within the editable textbox. An example would be

            "Type your message here."

        If not a string, will use the string representation of the object.
        """
        return self._ns.stringValue()

    @value.setter
    def value(self, x):
        x = compat.text_type(x)
        self._ns.setStringValue_(x)

    @property
    def placeholder(self):
        """x
        """
        return self._ns.placeholderString()

    @placeholder.setter
    def placeholder(self, x):
        self._ns.setPlaceholderString_(x)


class Password(_mixins.Component, _mixins.Actionable):
    """xxx
    """

    DEFAULT_WIDTH = 240
    DEFAULT_HEIGHT = 22

    def __init__(self, **options):
        auto   = options.get('auto')

        # TODO
        self._ns = _objc.RumpsNSSecureTextField.create_(self)
        self._ns.setSelectable_(True)
        self._ns.setEditable_(True)

        self.set_frame(**options)
