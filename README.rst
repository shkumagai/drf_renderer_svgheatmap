=======================
DRF Renderer SVGHeatmap
=======================

.. list-table:: Category badge
    :width: 50 100
    :header-row: 1

    * - Category
      - Badge
    * - CI
      - |ci_test|
    * - Package
      - |py_ver| |dj_ver|
    * - Meta
      -


.. |ci_test| image:: https://github.com/shkumagai/drf_renderer_svgheatmap/workflows/Test/badge.svg?branch=master
    :target: https://github.com/shkumagai/drf_renderer_svgheatmap/workflows/Test/badge.svg?branch=master
    :alt: master

.. |codecov| image:: https://codecov.io/gh/shkumagai/drf_renderer_svgheatmap/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/shkumagai/drf_renderer_svgheatmap
    :alt: Coverage

.. |py_ver| image:: https://img.shields.io/badge/support%20version-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue.svg?logo=python&logoColor=F9DC3E
    :alt: Support Python version

.. |dj_ver| image:: https://img.shields.io/badge/support%20version-3.2%20%7C%204.0%20%7C%204.1-green.svg?logo=django&logoColor=F9DC3E
    :alt: Support Django version

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
