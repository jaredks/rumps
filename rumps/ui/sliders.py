# -*- coding: utf-8 -*-

from . import _mixins
from .. import _internal
from .. import _objc


class Slider(_mixins.Component, _mixins.Actionable):
    """xxx

    :param value: a number for the current position of the slider.
    :param min_value: a number for the minimum position to which a slider can
        be moved.
    :param max_value: a number for the maximum position to which a slider can
        be moved.
    :param dimensions: a sequence of numbers whose length is two, specifying
        the dimensions of the slider.
    """

    DEFAULT_WIDTH = 180
    DEFAULT_HEIGHT = 15

    def __init__(self, value=50, min_value=0, max_value=100, **options):
        self._ns = _objc.RumpsNSSlider.create_(self)

        self.min_value = min_value
        self.max_value = max_value
        self.value = value

        self.set_frame(**options)

        if 'callback' in options:
            self.set_callback(options['callback'])

    @property
    def number_of_tick_marks(self):
        """x"""
        return self._ns.numberOfTickMarks()

    @number_of_tick_marks.setter
    def number_of_tick_marks(self, value):
        _internal._require_int(value)
        self._ns.setNumberOfTickMarks_(value)

    @property
    def allows_tick_mark_values_only(self):
        """YES if the slider fixes its values to the values represented by its tick marks; otherwise, NO. For example, if a slider has a minimum value of 0, a maximum value of 100, and five markers, the allowable values are 0, 25, 50, 75, and 100. When users move the slider’s knob, it jumps to the tick mark nearest the cursor when the mouse button is released. This method has no effect if the slider has no tick marks.
        """
        return self._ns.getAllowsTickMarkValuesOnly()

    @allows_tick_mark_values_only.setter
    def allows_tick_mark_values_only(self, value):
        self._ns.setAllowsTickMarkValuesOnly_(value)

    @property
    def continuous(self):
        return self._ns.getContinuous()

    @continuous.setter
    def continuous(self, value):
        self._ns.setContinuous_(value)

    @property
    def min_value(self, value):
        """xxx"""
        return self._ns.minValue()

    @min_value.setter
    def min_value(self, value):
        self._ns.setMinValue_(value)

    @property
    def max_value(self, value):
        """xxx"""
        return self._ns.maxValue()

    @max_value.setter
    def max_value(self, value):
        self._ns.setMaxValue_(value)

    @property
    def value(self):
        """The current position of the slider. If the
        :attr:`number_of_tick_marks` is nonzero, return the closest tick mark
        to the value selected.
        """
        value = self._ns.doubleValue()
        if not self.number_of_tick_marks:
            return value
        else:
            return self._ns.closestTickMarkValueToValue_(value)

    @value.setter
    def value(self, x):
        _internal._require_int(x)
        self._ns.setDoubleValue_(x)

    @property
    def actual_value(self):
        """The current position of the slider. Unaffected by the value of
        :attr:`number_of_tick_marks`.
        """
        return self._ns.doubleValue()
