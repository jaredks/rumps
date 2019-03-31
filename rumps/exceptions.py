# -*- coding: utf-8 -*-


class RumpsError(Exception):
    """A generic rumps error occurred."""


class NoCurrentApplication(RumpsError):
    """No application is currently running."""
