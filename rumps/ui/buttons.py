# -*- coding: utf-8 -*-

import AppKit

from . import _mixins
from .. import _objc
from .. import utils


class Button(_mixins.Component, _mixins.Actionable):
    """xxx"""

    DEFAULT_WIDTH = 120
    DEFAULT_HEIGHT = 28

    _button_types = ('NSButtonTypeMomentaryPushIn', 'NSMomentaryPushInButton')

    def __init__(self, title=None, **options):
        self._ns = _objc.RumpsNSButton.create_(self)
        self._ns.setButtonType_(utils.getattr_failover(AppKit, self._button_types))
        self._ns.setBezelStyle_(AppKit.NSRoundedBezelStyle)
        self.set_frame(**options)
        self.title = title

    @property
    def title(self):
        """This property contains the title displayed on the button when it’s in an off state or the empty string if the button doesn’t display a title. This title is always displayed if the button doesn’t use its alternate contents for highlighting or displaying the on state. By default, a button’s title is Button.
        """
        return self._ns.title()

    @title.setter
    def title(self, value):
        self._ns.setTitle_(value)

    # TODO
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
        return self._ns.state()

    @state.setter
    def state(self, new_state):
        self._ns.setState_(new_state)


class Checkbox(Button):
    """xxx"""

    _button_types = ('NSButtonTypeSwitch', 'NSSwitchButton')


class Radio(Button):
    """xxx"""

    _button_types = ('NSButtonTypeRadio', 'NSRadioButton')

    def _after_add_to_view(self, view):
        self._ns.setTarget_(view._cb_manager)
        self._ns.setAction_('callback:')
