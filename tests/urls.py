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

from django.conf.urls import url

from .test_renderers import (
    AnotherSimpleMockView,
    EmptyBaseMockView,
    EmptySimpleMockView,
    OtherSimpleMockView,
    SomethingBaseMockView,
    SomethingSimple1DMockView,
    SomethingSimple2DMockView,
)

urlpatterns = [
    url(
        r'^$',
        SomethingBaseMockView.as_view(),
    ),
    url(
        r'^empty(\.(?P<format>.+))?$',
        EmptyBaseMockView.as_view(),
    ),
    url(
        r'^simple2d$',
        SomethingSimple2DMockView.as_view(),
    ),
    url(
        r'^simple1d$',
        SomethingSimple1DMockView.as_view(),
    ),
    url(
        r'^another$',
        AnotherSimpleMockView.as_view(),
    ),
    url(
        r'^other$',
        OtherSimpleMockView.as_view(),
    ),
    url(
        r'^simple/empty$',
        EmptySimpleMockView.as_view(),
    ),
]
