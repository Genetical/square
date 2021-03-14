"""
The MIT License (MIT)
Copyright (c) 2021-present Genetical
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from square.enums import Enum, try_enum


class ErrorCategory(Enum):
    API_ERROR = "API_ERROR"
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
    INVALID_REQUEST_ERROR = "INVALID_REQUEST_ERROR"
    RATE_LIMIT_ERROR = "RATE_LIMIT_ERROR"
    PAYMENT_METHOD_ERROR = "PAYMENT_METHOD_ERROR"
    REFUND_ERROR = "REFUND_ERROR"


class ErrorCode(Enum):
    INTERNAL_SERVER_ERROR = ("INTERNAL_SERVER_ERROR",)
    UNAUTHORIZED = ("UNAUTHORIZED",)
    ACCESS_TOKEN_EXPIRED = ("ACCESS_TOKEN_EXPIRED",)
    ACCESS_TOKEN_REVOKED = ("ACCESS_TOKEN_REVOKED",)
    FORBIDDEN = ("FORBIDDEN",)
    INSUFFICIENT_SCOPES = ("INSUFFICIENT_SCOPES",)
    APPLICATION_DISABLED = ("APPLICATION_DISABLED",)
    V1_APPLICATION = ("V1_APPLICATION",)
    V1_ACCESS_TOKEN = ("V1_ACCESS_TOKEN",)
    BAD_REQUEST = ("BAD_REQUEST",)
    MISSING_REQUIRED_PARAMETER = ("MISSING_REQUIRED_PARAMETER",)
    INCORRECT_TYPE = ("INCORRECT_TYPE",)
    INVALID_TIME = ("INVALID_TIME",)
    INVALID_TIME_RANGE = ("INVALID_TIME_RANGE",)
    INVALID_VALUE = ("INVALID_VALUE",)
    INVALID_CURSOR = ("INVALID_CURSOR",)
    UNKNOWN_QUERY_PARAMETER = ("UNKNOWN_QUERY_PARAMETER",)
    CONFLICTING_PARAMETERS = ("CONFLICTING_PARAMETERS",)
    EXPECTED_JSON_BODY = ("EXPECTED_JSON_BODY",)
    INVALID_SORT_ORDER = ("INVALID_SORT_ORDER",)
    VALUE_REGEX_MISMATCH = ("VALUE_REGEX_MISMATCH",)
    VALUE_TOO_SHORT = ("VALUE_TOO_SHORT",)
    VALUE_TOO_LONG = ("VALUE_TOO_LONG",)
    VALUE_TOO_LOW = ("VALUE_TOO_LOW",)
    VALUE_TOO_HIGH = ("VALUE_TOO_HIGH",)
    VALUE_EMPTY = ("VALUE_EMPTY",)
    ARRAY_LENGTH_TOO_LONG = ("ARRAY_LENGTH_TOO_LONG",)
    ARRAY_LENGTH_TOO_SHORT = ("ARRAY_LENGTH_TOO_SHORT",)
    ARRAY_EMPTY = ("ARRAY_EMPTY",)
    EXPECTED_BOOLEAN = ("EXPECTED_BOOLEAN",)
    EXPECTED_INTEGER = ("EXPECTED_INTEGER",)
    EXPECTED_FLOAT = ("EXPECTED_FLOAT",)
    EXPECTED_STRING = ("EXPECTED_STRING",)
    EXPECTED_OBJECT = ("EXPECTED_OBJECT",)
    EXPECTED_ARRAY = ("EXPECTED_ARRAY",)
    EXPECTED_MAP = ("EXPECTED_MAP",)
    EXPECTED_BASE64_ENCODED_BYTE_ARRAY = ("EXPECTED_BASE64_ENCODED_BYTE_ARRAY",)
    INVALID_ARRAY_VALUE = ("INVALID_ARRAY_VALUE",)
    INVALID_ENUM_VALUE = ("INVALID_ENUM_VALUE",)
    INVALID_CONTENT_TYPE = ("INVALID_CONTENT_TYPE",)
    INVALID_FORM_VALUE = ("INVALID_FORM_VALUE",)
    NO_FIELDS_SET = ("NO_FIELDS_SET",)
    TOO_MANY_MAP_ENTRIES = ("TOO_MANY_MAP_ENTRIES",)
    MAP_KEY_LENGTH_TOO_SHORT = ("MAP_KEY_LENGTH_TOO_SHORT",)
    MAP_KEY_LENGTH_TOO_LONG = ("MAP_KEY_LENGTH_TOO_LONG",)
    CURRENCY_MISMATCH = ("CURRENCY_MISMATCH",)
    LOCATION_MISMATCH = ("LOCATION_MISMATCH",)
    IDEMPOTENCY_KEY_REUSED = ("IDEMPOTENCY_KEY_REUSED",)
    UNEXPECTED_VALUE = ("UNEXPECTED_VALUE",)
    SANDBOX_NOT_SUPPORTED = ("SANDBOX_NOT_SUPPORTED",)
    BAD_CERTIFICATE = ("BAD_CERTIFICATE",)
    INVALID_SQUARE_VERSION_FORMAT = ("INVALID_SQUARE_VERSION_FORMAT",)
    API_VERSION_INCOMPATIBLE = ("API_VERSION_INCOMPATIBLE",)
    NOT_FOUND = ("NOT_FOUND",)
    METHOD_NOT_ALLOWED = ("METHOD_NOT_ALLOWED",)
    NOT_ACCEPTABLE = ("NOT_ACCEPTABLE",)
    REQUEST_TIMEOUT = ("REQUEST_TIMEOUT",)
    CONFLICT = ("CONFLICT",)
    GONE = ("GONE",)
    REQUEST_ENTITY_TOO_LARGE = ("REQUEST_ENTITY_TOO_LARGE",)
    UNSUPPORTED_MEDIA_TYPE = ("UNSUPPORTED_MEDIA_TYPE",)
    UNPROCESSABLE_ENTITY = ("UNPROCESSABLE_ENTITY",)
    RATE_LIMITED = ("RATE_LIMITED",)
    NOT_IMPLEMENTED = ("NOT_IMPLEMENTED",)
    BAD_GATEWAY = ("BAD_GATEWAY",)
    SERVICE_UNAVAILABLE = ("SERVICE_UNAVAILABLE",)
    GATEWAY_TIMEOUT = "GATEWAY_TIMEOUT"


class SquareError(Exception):
    pass


class ClientError(SquareError):
    pass


class NotFoundError(ClientError):
    pass


class HTTPError(SquareError):
    def __init__(self, *, error):
        self.category = try_enum(ErrorCategory, error.get("category"))
        self.code = try_enum(ErrorCode, error.get("code"))
        self.detail = error.get("detail")
        self.field = error.get("field")

        super().__init__(self.detail)


class APIError(HTTPError):
    pass


class AuthenticationError(HTTPError):
    pass


class InvalidRequestError(HTTPError):
    pass


class RateLimited(HTTPError):
    pass


class PaymentMethodError(HTTPError):
    pass


class RefundError(HTTPError):
    pass


class InvalidArgument(ClientError):
    pass


class MultipleErrors(SquareError):
    def __init__(self, *, errors):
        self.exceptions = errors
        self.message = (
            "Multiple exceptions returned, access them with `error.exceptions`"
        )
        super().__init__(self.message)

    def __iter__(self):
        return self.exceptions
