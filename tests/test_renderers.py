# -*- coding: utf-8 -*-
#  Copyright 2019 Shoji Kumagai
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import re
import secrets
from math import ceil

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_renderer_svgheatmap.renderers import (
    BaseSVGHeatmapRenderer,
    SimpleSVGHeatmapRenderer,
)

DUMMYSTATUS = status.HTTP_200_OK
EMPTYCONTENT = []


def generatePoints(grid=32, length=360, is_1d=False):
    points = [
        {
            "x": secrets.randbelow(grid - 1),
            "y": secrets.randbelow(grid * 2 - 1),
            "value": secrets.randbelow(999) + 1,
        }
        for i in range(length)
    ]
    max_value = max(p["value"] for p in points)
    key_fmt = "{y}" if is_1d else "{x}-{y}"
    _points = {}
    for point in points:
        point["relative_value"] = ceil(point["value"] * 10 / max_value)
        _points.setdefault(key_fmt.format(**point), point)
    return sorted(_points.values(), key=lambda p: p["y"])


class EmptyBaseMockView(APIView):
    renderer_classes = (
        BaseSVGHeatmapRenderer,
        JSONRenderer,
    )

    def get(self, request, **kwargs):
        return Response(EMPTYCONTENT, status=DUMMYSTATUS)


class SomethingBaseMockView(APIView):
    renderer_classes = (BaseSVGHeatmapRenderer,)
    width = 640
    height = 1280

    def get(self, request, **kwargs):
        points = generatePoints()
        return Response(points, status=DUMMYSTATUS)


re_svgroot = re.compile(
    r"""^<svg
    \ baseProfile="full"
    \ height="[.0-9%]+"
    \ version="1\.1"
    \ width="[.0-9%]+"
    \ xmlns="http://www.w3.org/2000/svg"
    \ xmlns:ev="http://www.w3.org/2001/xml-events"
    \ xmlns:xlink="http://www.w3.org/1999/xlink">.+</svg>$
    """.encode(
        "utf-8",
    ),
    re.X,
)


class TestBaseSVGHeatmapRenderer(object):
    def test_renderer_serializes_empty_content(self, client):
        response = client.get("/empty")

        assert 200 == response.status_code
        assert (
            BaseSVGHeatmapRenderer.media_type + "; charset=utf-8"
            == response["Content-Type"]
        )
        assert re_svgroot.search(response.content) is not None
        assert re.search(r"<g />".encode("utf-8"), response.content) is not None

    def test_renderer_serializes_content_on_format_json(self, client):
        response = client.get("/empty.json")

        assert 200 == response.status_code
        assert JSONRenderer.media_type == response["Content-Type"]
        assert str(EMPTYCONTENT).encode("utf-8") == response.content

    def test_renderer_serializes_content_on_format_svg(self, client):
        response = client.get("/empty.svg")

        assert 200 == response.status_code
        assert (
            BaseSVGHeatmapRenderer.media_type + "; charset=utf-8"
            == response["Content-Type"]
        )
        assert re_svgroot.search(response.content) is not None
        assert re.search(r"<g />".encode("utf-8"), response.content) is not None

    def test_renderer_not_implemented_translate_method(self, client):
        response = client.get("/")

        assert 200 == response.status_code
        assert (
            BaseSVGHeatmapRenderer.media_type + "; charset=utf-8"
            == response["Content-Type"]
        )
        assert re_svgroot.search(response.content) is not None
        assert re.search(r"<g />".encode("utf-8"), response.content) is not None
        assert b'width="640"' in response.content
        assert b'height="1280"' in response.content


class EmptySimpleMockView(APIView):
    renderer_classes = (SimpleSVGHeatmapRenderer,)

    def get(self, request, **kwargs):
        return Response(EMPTYCONTENT, status=DUMMYSTATUS)


class SomethingSimple2DMockView(APIView):
    renderer_classes = (SimpleSVGHeatmapRenderer,)
    grid = 64
    opacity = 0.4
    svg_render_map = "interactions"
    v_key = "relative_value"

    def get(self, request, **kwargs):
        points = generatePoints(grid=self.grid)
        return Response({"interactions": points}, status=DUMMYSTATUS)


class SomethingSimple1DMockView(SomethingSimple2DMockView):
    is_line = True


class AnotherSimpleMockView(APIView):
    renderer_classes = (SimpleSVGHeatmapRenderer,)
    v_key = "relative_value"
    width = 640
    height = 1280

    def get(self, request, **kwargs):
        points = generatePoints()
        return Response(points, status=DUMMYSTATUS)


class OtherSimpleMockView(APIView):
    renderer_classes = (SimpleSVGHeatmapRenderer,)
    v_key = "relative_value"
    width = "640"
    height = "1280"

    def get(self, request, **kwargs):
        points = generatePoints()
        return Response(points, status=DUMMYSTATUS)


re_rectnode = re.compile(
    r"""<rect
    \ fill="\#[0-9a-fA-F]{6}"   # filled color
    \ height="[.0-9%]+"         # rectangle height
    \ opacity="[01]\.\d"        # background opacity
    \ width="[.0-9%]+"          # rectangle width
    \ x="[.0-9%]+"              # inserted x position
    \ y="[.0-9%]+">             # inserted y position
    <title>\d+%</title>         # tip content
    </rect>""".encode(
        "utf-8",
    ),
    re.X,
)


class TestSimpleSVGHeatmapRenderer(object):
    def test_renderer_serializes_2dcontent(self, client):
        response = client.get("/simple2d")

        # with open('sample2d.svg', 'w') as fp:
        #     fp.write(response.content.decode('utf-8'))

        assert 200 == response.status_code
        assert re.search(r"<g>.+</g>".encode("utf-8"), response.content) is not None
        assert (
            re.search(r"^<svg .+>.+</svg>$".encode("utf-8"), response.content)
            is not None
        )
        assert b'width="100%"' in response.content
        assert b'height="100%"' in response.content
        assert b'opacity="0.4"' in response.content

    def test_renderer_serializes_1dcontent(self, client):
        response = client.get("/simple1d")

        # with open('sample1d.svg', 'w') as fp:
        #     fp.write(response.content.decode('utf-8'))

        assert 200 == response.status_code
        assert re.search(r"<g>.+</g>".encode("utf-8"), response.content) is not None
        assert (
            re.search(r"^<svg .+>.+</svg>$".encode("utf-8"), response.content)
            is not None
        )
        assert b'width="100%"' in response.content
        assert b'height="100%"' in response.content
        assert b'opacity="0.4"' in response.content

    def test_renderer_serializes_content_size_specified_with_int(self, client):
        response = client.get("/another")

        assert 200 == response.status_code
        assert re.search(r"<g>.+</g>".encode("utf-8"), response.content) is not None
        assert (
            re.search(r"^<svg .+>.+</svg>$".encode("utf-8"), response.content)
            is not None
        )
        assert b'width="640"' in response.content
        assert b'height="1280"' in response.content

    def test_renderer_serializes_content_size_specified_with_str(self, client):
        response = client.get("/other")

        assert 200 == response.status_code
        assert re.search(r"<g>.+</g>".encode("utf-8"), response.content) is not None
        assert (
            re.search(r"^<svg .+>.+</svg>$".encode("utf-8"), response.content)
            is not None
        )
        assert b'width="640"' in response.content
        assert b'height="1280"' in response.content

    def test_renderer_serializes_empty_content(self, client):
        response = client.get("/simple/empty")

        assert 200 == response.status_code
        assert (
            SimpleSVGHeatmapRenderer.media_type + "; charset=utf-8"
            == response["Content-Type"]
        )
        assert re_svgroot.search(response.content) is not None
        assert re.search(r"<g />".encode("utf-8"), response.content) is not None
