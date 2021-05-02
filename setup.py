#!/usr/bin/env python
from setuptools import find_packages, setup

import drf_renderer_svgheatmap

with open('README.rst') as readme_rst:
    readme = readme_rst.read()

with open('HISTORY.rst') as history_rst:
    history = history_rst.read()

install_requires = [
    'Django',
    'djangorestframework',
    'svgwrite',
]

classifiers = [
    'Development State :: 3 - Alpha',
    'Environment :: Web Environment',
    'Framework :: Django :: 2.2',
    'Framework :: Django :: 3.1',
    'Framework :: Django :: 3.2',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
]

setup(
    name='drf_renderer_svgheatmap',
    version=drf_renderer_svgheatmap.__version__,
    url='https://github.com/shkumagai/drf_renderer_svgheatmap',
    license='Apache License 2.0',
    description='SVG Heatmap renderer for Django REST Framework',
    long_description='\n\n'.join([readme, history]),
    long_description_content_type='text/x-rst',
    author=drf_renderer_svgheatmap.__author__,
    author_email=drf_renderer_svgheatmap.__email__,
    classifiers=classifiers,
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=install_requires,
    python_requires=">=3.6",
    zip_safe=False,
)
