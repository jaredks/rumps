#!/usr/bin/env python

import errno
import os
import re
import sys
import traceback

from setuptools import setup

INFO_PLIST_TEMPLATE = '''\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleIdentifier</key>
    <string>%(name)s</string>
</dict>
</plist>
'''


def fix_virtualenv():
    executable_dir = os.path.dirname(sys.executable)

    try:
        os.mkdir(os.path.join(executable_dir, 'Contents'))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    with open(os.path.join(executable_dir, 'Contents', 'Info.plist'), 'w') as f:
        f.write(INFO_PLIST_TEMPLATE % {'name': 'rumps'})


with open('README.rst') as f:
    readme = f.read()
with open('CHANGES.rst') as f:
    changes = f.read()
with open('rumps/__init__.py') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='rumps',
    version=version,
    description='Ridiculously Uncomplicated MacOS Python Statusbar apps.',
    author='Jared Suttles',
    url='https://github.com/jaredks/rumps',
    packages=['rumps', 'rumps.packages'],
    package_data={'': ['LICENSE']},
    long_description=readme + '\n\n' + changes,
    license='BSD License',
    install_requires=[
        'pyobjc-framework-Cocoa'
    ],
    extras_require={
        'dev': [
            'pytest>=4.3',
            'pytest-mock>=2.0.0',
            'tox>=3.8'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: MacOS X',
        'Environment :: MacOS X :: Cocoa',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Objective C',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

# if this looks like a virtualenv
if hasattr(sys, 'real_prefix'):
    print('=' * 64)
    print(
        '\n'
        'It looks like we are inside a virtualenv. Attempting to apply fix.\n'
    )
    try:
        fix_virtualenv()
    except Exception:
        traceback.print_exc()
        print(
            'WARNING: Could not fix virtualenv. UI interaction likely will '
            'not function properly.\n'
        )
    else:
        print(
            'Applied best-effort fix for virtualenv to support proper UI '
            'interaction.\n'
        )
    print(
        'Use of venv is suggested for creating virtual environments:'
        '\n\n'
        '    python3 -m venv env'
        '\n'
    )
    print('=' * 64)
