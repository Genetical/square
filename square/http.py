# -*- coding: utf-8 -*-
#  The MIT License (MIT)
#  Copyright (c) 2021-present Genetical
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

import logging
import warnings
from urllib.parse import quote, urljoin
import requests

log = logging.getLogger(__name__)


class Route:
    """Represents the Route for the request.
    This object represents the location and type of request. It will
    construct a fully formed url and store the HTTP method.

    Parameters
    ----------
    method : str
        The HTTP method to be used.
    path : str
        The subdirectory (path) of the domain. Any variable
        subdirectories should be in the form of a docstring.
    **parameters, optional
        Used to format the `path` so that variable
        subdirectories are replaced with their values.

    Attributes
    ----------
    method: str
    path: str
    url: str
        The constructed URL.

    Warns
    -----
    UserWarning
        Caused by using an unknown HTTP method.

    Warnings
    --------
    You should always submit untrusted data in the `parameters`
    param. The data will be correctly url escaped if needed.

    Examples
    --------
    >>> Route("GET", "customers/{customer_id}", customer_id="123456789")
    """
    BASE = "https://connect.squareupsandbox.com/v2/"

    def __init__(self, method, path, **parameters):
        if self.BASE is None:
            raise NotImplementedError("Route.BASE must be set.")

        if method.upper() not in ('GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'):
            warnings.warn(f"Unknown HTTP method '{method}'. Expect a 501 response.")
        self.method = method
        self.path = path

        if parameters:
            # Dict comprehension which url encodes all values in the `parameters` dict then formats it.
            path = path.format(
                **{k: quote(v) if isinstance(v, str) else v for k, v in parameters.items()}
            )

        self.url = urljoin(self.BASE, path)
