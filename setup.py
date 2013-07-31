#!/usr/bin/env python
from distutils.core import setup
import rumps

setup(
    name='rumps',
    version=rumps.__version__,
    description='Ridiculously Uncomplicated Mac os x Python toolbar appS',
    author='Jared Suttles',
    url='https://github.com/jaredks/rumps',
    packages=['rumps'],
    package_data={'': ['LICENSE']},
    long_description=open('README.md').read() + '\n\n' + open('CHANGES').read(),
    license='BSD License',
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
