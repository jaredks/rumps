# -*- coding: utf-8 -*-

from .utils import EventEmitter

before_start = EventEmitter('before_start')
on_notification = EventEmitter('on_notification')
on_sleep = EventEmitter('on_sleep')
on_wake = EventEmitter('on_wake')
before_quit = EventEmitter('before_quit')
