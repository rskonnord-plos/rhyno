#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'rhyno',
]

requires = [
    'requests',
]

setup(
    name='rhyno',
    version='0.1.0',
    description='Pythonic Ambra admin API',
    long_description=open('README.md').read(),
    author='John LaBarba',
    author_email='jlabarba@plos.org',
    url='https://bitbucket.org/dweebit/rhyno',
    packages=packages,
    package_dir={'rhyno': 'rhyno'},
    include_package_data=True,
    install_requires=requires,
    license=open('LICENSE.txt').read(),
    zip_safe=True,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
)
