=======================
DRF Renderer SVGHeatmap
=======================

.. image:: https://github.com/shkumagai/drf_renderer_svgheatmap/workflows/Test/badge.svg?branch=master
    :target: https://github.com/shkumagai/drf_renderer_svgheatmap/workflows/Test/badge.svg?branch=master
    :alt: master

.. image:: https://codecov.io/gh/shkumagai/drf_renderer_svgheatmap/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/shkumagai/drf_renderer_svgheatmap
    :alt: Coverage

.. image:: https://pyup.io/repos/github/shkumagai/drf_renderer_svgheatmap/shield.svg
    :target: https://pyup.io/repos/github/shkumagai/drf_renderer_svgheatmap/
    :alt: Updates

.. image:: https://pyup.io/repos/github/shkumagai/drf_renderer_svgheatmap/python-3-shield.svg
    :target: https://pyup.io/repos/github/shkumagai/drf_renderer_svgheatmap/
    :alt: Python 3

Purpose
=======

Simple SVG Heatmap rendering library for Django application.

- Free software: Apache License 2.0

Feature
=======

To install DRF Renderer SVGHeatmap, run as below in your terminal::

    $ pip install drf_renderer_svgheatmap

Usage
=====

.. code:: python

    from drf_renderer_svgheatmap.renderer import SimpleSVGHeatmapRenderer
    from rest_framework.views import APIView

    ...

    class SomethingHeatmapView(APIView):
        renderer_classes = (
            SimpleSVGHeatmapRenderer,
            JSONRenderer,
        )

        def get(self, request, **kwargs):
            data = get_data()  # return list of dict
            return Response(data)

Develop
=======

::

    $ git clone git@github.com:shkumagai/drf_renderer_svgheatmap.git
    $ cd drf_renderer_svgheatmap
    $ mkvirtualenv -a . -p $(which python) -r requirements/development.txt drf_svgheatmap
