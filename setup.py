#!/usr/bin/env python
from distutils.core import setup
import rumps

with open('README.rst') as f:
    readme = f.read()
with open('CHANGES.rst') as f:
    changes = f.read()

setup(
    name='rumps',
    version=rumps.__version__,
    description='Ridiculously Uncomplicated Mac os x Python Statusbar apps.',
    author='Jared Suttles',
    url='https://github.com/jaredks/rumps',
    packages=['rumps', 'rumps.packages'],
    package_data={'': ['LICENSE']},
    long_description=readme + '\n\n' + changes,
    license='BSD License',
    install_requires=['pyobjc-core'],
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
    ],
)
