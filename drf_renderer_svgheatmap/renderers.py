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

from typing import Any, Dict, List, Optional, Union

from rest_framework.renderers import BaseRenderer
from svgwrite import Drawing
from svgwrite.container import Group
from svgwrite.shapes import Rect

# Data types
Point = Dict[str, int]
DataContainer = List[Point]
ColorScale = List[str]

DEFAULT_COLOR_SCALE: ColorScale = [
    '#3300FF',
    '#00B3FF',
    '#00FFFF',
    '#00FF66',
    '#33FF00',
    '#CCFF00',
    '#FFE600',
    '#FF9900',
    '#FF4D00',
    '#FF0000',
]
GRID: int = 32
OPACITY: float = 0.5  # 0.0 (transparent) to 1.0 (opaque)


class BaseSVGHeatmapRenderer(BaseRenderer):
    """Base class for SVG Heatmap renderer.

    To use this renderer, need to implement `translate` method in subclass.
    """

    media_type: str = 'image/svg+xml'
    format: str = 'svg'

    filename: str = 'heatmap.svg'
    svg_profile: str = 'full'
    default_width: str = '100%'
    default_height: str = '100%'

    def translate(
        self,
        data: DataContainer,
        width: int,
        height: int,
        x_key: str = 'x',
        y_key: str = 'y',
        v_key: str = 'value',
        is_1d: bool = False,
        **kwargs: Any,
    ) -> Group:
        """Base translator for SVG Heatmap renderer.

        :param data: point datum array.
            point datum represent by dict consists with x, y positions and value.
        :param width: drawing area width.
        :param height: drawing area height.
        :param x_key: key name of x for points.
        :param y_key: key name of y for points.
        :param v_key: key name of value for points.
        :param is_1d: render rect as full width (One-dimensional heatmap).
        :return: Rect nodes enclosed with Group node.
        """
        return Group()

    def render(
        self,
        data: DataContainer,
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[Dict[str, Union[str, int, float]]] = None,
    ) -> bytes:
        """
        :param data: point datum array, or dict that include those array in certain key.
            point datum represent by dict consists with x, y positions and value.
            when dict specified, need to specify corresponding key via view's attribute
            as 'svg_render_map'.
        :param accepted_media_type:
        :param renderer_context:
        :return: SVG formatted heatmap in bytestring.
        """
        renderer_context = renderer_context or {}
        view = renderer_context['view']

        width = getattr(view, 'width', self.default_width)
        height = getattr(view, 'height', self.default_height)
        translatorArgs = {
            'colorScale': getattr(view, 'color_scale', DEFAULT_COLOR_SCALE),
            'grid': getattr(view, 'grid', GRID),
            'opacity': getattr(view, 'opacity', OPACITY),
            'x_key': getattr(view, 'x_key', 'x'),
            'y_key': getattr(view, 'y_key', 'y'),
            'v_key': getattr(view, 'v_key', 'value'),
            'is_1d': getattr(view, 'is_1d', False),
        }

        svg_render_map = getattr(view, 'svg_render_map', None)
        bare_data = data if svg_render_map is None else data[svg_render_map]
        datagroup = self.translate(bare_data, width, height, **translatorArgs)

        drawSize = (width, height)
        svgargs = getattr(view, 'svgargs', {})
        drawing = Drawing(self.filename, size=drawSize, profile=self.svg_profile, **svgargs)
        drawing.add(datagroup)

        return drawing.tostring().encode('ascii')


class SimpleSVGHeatmapRenderer(BaseSVGHeatmapRenderer):
    """Render heatmap with applied data points simply."""

    def translate(
        self,
        data: DataContainer,
        width: int,
        height: int,
        x_key: str = 'x',
        y_key: str = 'y',
        v_key: str = 'value',
        is_1d: bool = False,
        colorScale: ColorScale = DEFAULT_COLOR_SCALE,
        grid: int = GRID,
        opacity: float = OPACITY,
        **kwargs: Any,
    ):
        """Points to Rect element translator for Simple SVG Heatmap renderer.

        Return SVG Group node that includes Rect node which been set attributes
        such as coordinate, fill color, opacity.
        Those attributes are based on applied data.

        :param colorScale: ColorScale array to use.
        :param grid: grid count. 32 or 64.
        :param opacity: alpha value for heatmap.
        """
        isRelative = False
        if isinstance(width, str):
            if width.endswith("%"):
                gridSize = 3.125 if grid == 32 else 1.5625
                isRelative = True
            else:
                gridSize = int(width, 10) / grid
        elif isinstance(width, int):
            gridSize = width / grid

        group = Group()
        if data and isinstance(data, list):
            for datum in data:
                extra = {
                    'opacity': opacity,
                    'fill': colorScale[datum[v_key] - 1],
                }

                insert_x = 0 if is_1d else gridSize * datum[x_key]
                insert_y = gridSize * datum[y_key]
                size_w = gridSize if not is_1d else 100.0
                size_h = gridSize

                rect = Rect(
                    insert=(
                        insert_x if not isRelative else "%.4f%%" % insert_x,
                        insert_y if not isRelative else "%.4f%%" % insert_y,
                    ),
                    size=(
                        size_w if not isRelative else "%.4f%%" % size_w,
                        size_h if not isRelative else "%.4f%%" % size_h,
                    ),
                    **extra
                )
                rect.set_desc(title='{0}%'.format(datum[v_key] * 10))
                group.add(rect)

        return group
