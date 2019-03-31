# -*- coding: utf-8 -*-

from Foundation import NSDate, NSTimer, NSRunLoop, NSDefaultRunLoopMode
import weakref

_TIMERS = weakref.WeakKeyDictionary()


def timers():
    """Return a list of all :class:`rumps.Timer` objects. These can be active or inactive."""
    return list(_TIMERS)


class Timer(object):
    """
    Python abstraction of an Objective-C event timer in a new thread for application. Controls the callback function,
    interval, and starting/stopping the run loop.

    .. versionchanged:: 0.2.0
       Method `__call__` removed.

    :param callback: Function that should be called every `interval` seconds. It will be passed this
                     :class:`rumps.Timer` object as its only parameter.
    :param interval: The time in seconds to wait before calling the `callback` function.
    """
    def __init__(self, callback, interval):
        self.set_callback(callback)
        self._interval = interval
        self._status = False

    def __repr__(self):
        return ('<{0}: [callback: {1}; interval: {2}; '
                'status: {3}]>').format(type(self).__name__, repr(getattr(self, '*callback').__name__),
                                        self._interval, 'ON' if self._status else 'OFF')

    @property
    def interval(self):
        """The time in seconds to wait before calling the :attr:`callback` function."""
        return self._interval  # self._nstimer.timeInterval() when active but could be inactive

    @interval.setter
    def interval(self, new_interval):
        if self._status:
            if abs(self._nsdate.timeIntervalSinceNow()) >= self._nstimer.timeInterval():
                self.stop()
                self._interval = new_interval
                self.start()
        else:
            self._interval = new_interval

    @property
    def callback(self):
        """The current function specified as the callback."""
        return getattr(self, '*callback')

    def is_alive(self):
        """Whether the timer thread loop is currently running."""
        return self._status

    def start(self):
        """Start the timer thread loop."""
        if not self._status:
            self._nsdate = NSDate.date()
            self._nstimer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(
                self._nsdate, self._interval, self, 'callback:', None, True)
            NSRunLoop.currentRunLoop().addTimer_forMode_(self._nstimer, NSDefaultRunLoopMode)
            _TIMERS[self] = None
            self._status = True

    def stop(self):
        """Stop the timer thread loop."""
        if self._status:
            self._nstimer.invalidate()
            del self._nstimer
            del self._nsdate
            self._status = False

    def set_callback(self, callback):
        """Set the function that should be called every :attr:`interval` seconds. It will be passed this
        :class:`rumps.Timer` object as its only parameter.
        """
        setattr(self, '*callback', callback)

    def callback_(self, _):
        _log(self)
        try:
            return _call_as_function_or_method(getattr(self, '*callback'), self)
        except Exception:
            _log(traceback.format_exc())
