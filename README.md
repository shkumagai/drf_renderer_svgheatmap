# DRF Renderer SVGHeatmap

| Category | Badge |
|:---------|:------|
| CI | [![lint](https://github.com/shkumagai/drf_renderer_svgheatmap/actions/workflows/check.yml/badge.svg)](https://github.com/shkumagai/drf_renderer_svgheatmap/actions/workflows/check.yml) [![Unit test](https://github.com/shkumagai/drf_renderer_svgheatmap/actions/workflows/unittest.yml/badge.svg)](https://github.com/shkumagai/drf_renderer_svgheatmap/actions/workflows/unittest.yml) |
| Package | ![Python Support Version](https://img.shields.io/badge/support%20version-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue.svg?logo=python&logoColor=F9DC3E) ![Django Support Version](https://img.shields.io/badge/support%20version-3.2%20%7C%204.0%20%7C%204.1-green.svg?logo=django&logoColor=F9DC3E) |
| Meta | [![code style - black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) [![imports - isort](https://img.shields.io/badge/imports-isort-ef8336.svg)](https://github.com/pycqa/isort) [![security - bandit](https://img.shields.io/badge/security-bandit-ef8336.svg)](https://github.com/pycqa/bandit) |


## Purpose

Simple SVG Heatmap rendering library for Django application.

- Free software: Apache License 2.0

## Feature

To install DRF Renderer SVGHeatmap, run as below in your terminal:
```sh
$ pip install drf_renderer_svgheatmap
```

## Usage
```py
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
```

## Develop

```sh
$ git clone git@github.com:shkumagai/drf_renderer_svgheatmap.git
$ cd drf_renderer_svgheatmap
$ mkvirtualenv -a . -p $(which python) -r requirements/development.txt drf_svgheatmap
```
