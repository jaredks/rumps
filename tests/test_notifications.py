# -*- coding: utf-8 -*-

import pytest

import rumps

# do this hacky thing
notify = rumps._notifications.notify
_clicked = rumps._notifications._clicked
on_notification = rumps._notifications.on_notification
Notification = rumps._notifications.Notification


class NSUserNotificationCenterMock:
    def __init__(self):
        self.ns_user_notification = None

    def scheduleNotification_(self, ns_user_notification):
        self.ns_user_notification = ns_user_notification

    def removeDeliveredNotification_(self, ns_user_notification):
        assert ns_user_notification is self.ns_user_notification
        self.ns_user_notification = None


class TestNotify:
    path = 'rumps._notifications._default_user_notification_center'

    def test_simple(self, mocker):
        """Simple notification is created and scheduled. The internal callback
        handler does not raise any exceptions when processing the notification.
        """

        ns_user_notification_center_mock = NSUserNotificationCenterMock()
        mocker.patch(self.path, new=lambda: ns_user_notification_center_mock)

        assert ns_user_notification_center_mock.ns_user_notification is None
        notify(
            'a',
            'b',
            'c'
        )
        assert ns_user_notification_center_mock.ns_user_notification is not None
        _clicked(
            ns_user_notification_center_mock,
            ns_user_notification_center_mock.ns_user_notification
        )
        assert ns_user_notification_center_mock.ns_user_notification is None

    def test_with_data(self, mocker):
        """Notification that contains serializable data."""

        ns_user_notification_center_mock = NSUserNotificationCenterMock()
        mocker.patch(self.path, new=lambda: ns_user_notification_center_mock)

        @on_notification
        def user_defined_notification_callback(notification):
            assert notification.data == ['any', {'pickable': 'object'}, 'by', 'default']

        assert ns_user_notification_center_mock.ns_user_notification is None
        notify(
            'a',
            'b',
            'c',
            data=['any', {'pickable': 'object'}, 'by', 'default']
        )
        assert ns_user_notification_center_mock.ns_user_notification is not None
        _clicked(
            ns_user_notification_center_mock,
            ns_user_notification_center_mock.ns_user_notification
        )
        assert ns_user_notification_center_mock.ns_user_notification is None


class TestNotification:
    def test_can_access_data(self):
        n = Notification(None, 'some test data')
        assert n.data == 'some test data'

    def test_can_use_data_as_mapping(self):
        n = Notification(None, {2: 22, 3: 333})
        assert n[2] == 22
        assert 3 in n
        assert len(n) == 2

    def test_raises_typeerror_when_no_mapping(self):
        n = Notification(None, [4, 55, 666])
        with pytest.raises(TypeError) as excinfo:
            n[2]
        assert 'cannot be used as a mapping' in str(excinfo.value)
