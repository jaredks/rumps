# -*- coding: utf-8 -*-

import pytest

from rumps._internal import guard_unexpected_errors


class TestGuardUnexpectedErrors(object):
    def test_raises(self, capfd):

        @guard_unexpected_errors
        def callback_func():
            raise ValueError('-.-')

        callback_func()

        captured = capfd.readouterr()
        assert not captured.out
        assert captured.err.strip().startswith('Traceback (most recent call last):')
        assert captured.err.strip().endswith('''ValueError: -.-

The above exception was the direct cause of the following exception:

rumps.exceptions.InternalRumpsError: an unexpected error occurred within an internal callback''')

    def test_no_raises(self, capfd):

        @guard_unexpected_errors
        def callback_func():
            return 88 * 2

        assert callback_func() == 176

        captured = capfd.readouterr()
        assert not captured.out
        assert not captured.err
