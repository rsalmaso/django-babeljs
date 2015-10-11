# -*- coding: utf-8 -*-

# Copyright (C) 2007-2015, Raffaele Salmaso <raffaele@salmaso.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import absolute_import, division, print_function, unicode_literals
from .version import get_version

VERSION = (0, 1, 0, "final", 0)

__version__  = get_version(VERSION)
__author__  = "Raffaele Salmaso"
__email__ = "raffaele@salmaso.org"


class TransformError(Exception):
    pass


def _transpile(jsx, **opts):
    import os
    from . import conf as settings
    from . import execjs

    babel = os.path.join(settings.JS_ROOT, settings.BABELJS)
    try:
        js = execjs.compile("""var babel = require("{}");""".format(babel))
    except:
        raise TransformError()

    try:
        result = js.call("babel.transform", jsx, opts)
    except execjs.ProgramError as ex:
        raise TransformError(str(ex)[7:])

    return result


def _get_path(digest):
    return "babeljs-{}".format(digest)


def transpile(jsx, **opts):
    import hashlib
    from django.core.cache import caches
    from . import conf as settings
    cache = caches[settings.CACHE_BACKEND]
    path = _get_path(hashlib.sha512(jsx.encode("utf-8")).hexdigest())
    result = cache.get(path)
    if not result:
        result = _transpile(jsx, **opts)
        cache.set(path, result, settings.CACHE_TIMEOUT)
    return result
