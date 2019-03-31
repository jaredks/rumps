# -*- coding: utf-8 -*-

_ENABLED = True
try:
    from Foundation import NSUserNotification, NSUserNotificationCenter
except ImportError:
    _ENABLED = False

import os
import sys

import Foundation

from . import _internal
from . import ctx

# TODO
from .images import Image


def _gather_info_issue_9():
    missing_plist = False
    missing_bundle_ident = False
    info_plist_path = os.path.join(os.path.dirname(sys.executable), 'Info.plist')
    try:
        with open(info_plist_path) as f:
            import plistlib
            try:
                load_plist = plistlib.load
            except AttributeError:
                load_plist = plistlib.readPlist
            try:
                load_plist(f)['CFBundleIdentifier']
            except Exception:
                missing_bundle_ident = True

    except IOError as e:
        import errno
        if e.errno == errno.ENOENT:  # No such file or directory
            missing_plist = True

    info = '\n\n'
    if missing_plist:
        info += 'In this case there is no file at "%(info_plist_path)s"'
        info += '\n\n'
        confidence = 'should'
    elif missing_bundle_ident:
        info += 'In this case the file at "%(info_plist_path)s" does not contain a value for "CFBundleIdentifier"'
        info += '\n\n'
        confidence = 'should'
    else:
        confidence = 'may'
    info += 'Running the following command %(confidence)s fix the issue:\n'
    info += '/usr/libexec/PlistBuddy -c \'Add :CFBundleIdentifier string "rumps"\' %(info_plist_path)s\n'
    return info % {'info_plist_path': info_plist_path, 'confidence': confidence}


def _default_user_notification_center():
    notification_center = NSUserNotificationCenter.defaultUserNotificationCenter()
    if notification_center is None:
        info = (
            'Failed to setup the notification center. This issue occurs when the "Info.plist" file '
            'cannot be found or is missing "CFBundleIdentifier".'
        )
        try:
            info += _gather_info_issue_9()
        except Exception:
            import traceback
            traceback.print_exc()
        raise RuntimeError(info)
    else:
        return notification_center


def _setup_notifications(nsapp):
    if _ENABLED:
        try:
            notification_center = _default_user_notification_center()
        except RuntimeError:
            pass
        else:
            notification_center.setDelegate_(nsapp)


def notification(title, subtitle, message, data=None, sound=True, action_button=None, other_button=None,
                 has_reply_button=False, icon=None):
    """Send a notification to Notification Center (OS X 10.8+). If running on a
    version of macOS that does not support notifications, a ``RuntimeError``
    will be raised. Apple says,

        "The userInfo content must be of reasonable serialized size (less than 1k) or an exception will be thrown."

    So don't do that!

    :param title: text in a larger font.
    :param subtitle: text in a smaller font below the `title`.
    :param message: text representing the body of the notification below the
                    `subtitle`.
    :param data: will be passed to the application's "notification center"
                 (see :func:`rumps.notifications`) when this
                 notification is clicked.
    :param sound: whether the notification should make a noise when it arrives.
    :param action_button: title for the action button.
    :param other_button: title for the other button.
    :param has_reply_button: whether or not the notification has a reply button.
    :param icon: the filename of an image for the notification's icon, will
                 replace the default.

    """
    if not _ENABLED:
        raise RuntimeError('OS X 10.8+ is required to send notifications')

    if data is not None and not isinstance(data, Mapping):
        raise TypeError('notification data must be a mapping')

    _internal._require_string_or_none(title, subtitle, message)

    notification = NSUserNotification.alloc().init()

    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(message)

    if data is not None:
        app = ctx.current_app()
        dumped = app.serializer.dumps(data)
        ns_dict = Foundation.NSMutableDictionary.alloc().init()
        ns_string = Foundation.NSString.alloc().initWithString_(dumped)
        ns_dict.setDictionary_({'value': ns_string})
        notification.setUserInfo_(ns_dict)

    if icon is not None:
        notification.set_identityImage_(Image.from_file(icon))
    if sound:
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
    if action_button:
        notification.setActionButtonTitle_(action_button)
        notification.set_showsButtons_(True)
    if other_button:
        notification.setOtherButtonTitle_(other_button)
        notification.set_showsButtons_(True)
    if has_reply_button:
        notification.setHasReplyButton_(True)

    notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(0, Foundation.NSDate.date()))
    notification_center = _default_user_notification_center()
    notification_center.scheduleNotification_(notification)


# TODO
class Notification(object):
    pass
