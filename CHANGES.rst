Changes
=======

0.2.1 (2014-12-13)
------------------

- No longer have to set menu explicitly
    + rumps will create the menu as it parses paths in ``clicked`` decorators
- Reverted change to `timers` that produced a list of weak references rather than objects
- New keyword arguments
    + `key` for ``clicked``
    + `debug` for ``App.run``


0.2.0 (2014-08-09)
------------------

**Improvements and compatibility fixes**

- Added a large number of docstrings
- Merged pull request allowing unicode text
- Compatibility fixes for Python 2.6
    + Included OrderedDict recipe
    + _TIMERS not using weakref.WeakSet
- Compatibility fixes for Mac OS X versions prior to 10.8 (Notification Center)
    + Attempting to send a notification on <10.8 will raise ``RuntimeError``
- Added ``quit_application`` function to allow for both custom quit buttons and running clean up code before quitting

**API changes**

- Most api changes dealt with accepting ``None`` as a parameter to use or restore a default setting
- Raise ``TypeError`` before less obvious exceptions occur in PyObjC
- alert and Window
    + No required parameters
    + Passing a string as `cancel` parameter will change the button text to that string
    + `Window.add_button` now requires a string
- App
    + `name` parameter must be a string and `title` must be either a string or ``None``
    + Added `quit_button` parameter allowing custom text or disabling completely by passing ``None``
- MenuItem
    + Passing ``None`` as `callback` parameter to `MenuItem.set_callback` method will disable the callback function and grey out the menu item
    + passing an invalid sequence for `dimensions` parameter to `MenuItem.set_icon` will no longer silently error


0.1.5 (2014-08-03)
------------------

- Fix implemented for NSInvalidArgumentException issue on 10.9.x


0.1.4 (2013-08-21)
------------------

- Menu class subclassing ListDict, a subclass of OrderedDict with additional insertion operations
- ``update`` method of Menu works like old App.menu parsing - consumes various nested Python containers and creates menus


0.1.3 (2013-08-19)
------------------

- ``separator`` global for marking menu separators (in addition to None in context of a menu)
- Can now have separators in sub menus using either ``separator`` or None
- Key and menu title not matching doesn't raise an exception since the situation would occur if the title is changed dynamically
    + Instead, a warning in the log
- Refactored MenuItem such that it subclasses new Menu class
- Menu class created
    + Wraps NSMenu using __setitem__, __delitem__, etc.
    + Allows for main menu to be easily changed during runtime as it now uses Menu class instead of vanilla OrderedDict
    + ``clear`` method for MenuItem + other irrelevant methods inherited from OrderedDict raise NotImplementedError
- As result of refactoring, could simplify menu parsing for App


0.1.2 (2013-08-11)
------------------

- Interval access and modification added to Timer objects
- timers function for iterating over timers
- Timer class now directly in module namespace
- More specfic case for trying callback with instance of App subclass as first argument
    + Point is to avoid catching a completely different TypeError, then sending 2 variables to a function consuming 1


0.1.1 (2013-08-07)
------------------

- Parsing data structures for creating menus is now more robust
- Fixed MenuItem __repr__ for printing instances where no callback function has been given
- Added ``example_menu.py`` to examples serving also as a test for new MenuItem changes
- Can now ``del`` MenuItems of submenus and it will be reflected in the actual menu
- ``add`` method for more convenient addition of MenuItems to a MenuItem's submenu
- Created module docstring


0.1.0 (2013-07-31)
------------------

- world, hello! meet rumps.
