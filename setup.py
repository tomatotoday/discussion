#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

readme = """
Tomato Discussion Application.
"""


requirements = [
    'flask==0.11.1',
    'flask-jsonrpc==0.3.1',
    'flask-sqlalchemy==2.1',
]

test_requirements = [
    'pytest==2.9.1',
]

setup(
    name='tomato-discussion',
    version='0.1.0',
    description="tomato discussion.",
    long_description=readme,
    author="Ju Lin",
    author_email='soasme@gmail.com',
    url='https://github.com/soasme/tomato',
    packages=find_packages(exclude=('tests', 'tests.*', '*.tests', '*.tests.*', )),
    package_dir={'tomato': 'tomato'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='tomato-discussion',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
