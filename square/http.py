import logging

import requests
from square.errors import *
from urllib.parse import urljoin, quote
import uuid

log = logging.getLogger(__name__)


def generate_route(base):
    """Construct a route, given a base endpoint

    Parameters
    ----------
    base: str
        The endpoint that all requests should be based on.

    Returns
    -------
    Route

    """

    class Route:
        """Represents the Route for the request.
        This object represents the location and type of request. It will
        construct a fully formed url and store the HTTP method.

        Parameters
        ----------
        method : str
            The HTTP method to be used.
        domain : str
            The domain the request should be sent to.
        path : str
            The subdirectory (path) of the domain. Any variable
            subdirectories should be in the form of a docstring.
        **parameters, optional
            Used to format the `path` so that variable
            subdirectories are replaced with their values.

        Attributes
        ----------
        method: str
        domain: str
        path: str
        url: str
            The constructed URL.

        Warnings
        --------
        You should always submit  data in the `parameters` param.
        The data will be correctly url escaped if needed.

        Examples
        --------
        >>> Route("GET", "customers/{customer_id}", customer_id="123456789")
        or
        >>> Route("GET", "customers/{customer_id}", customer_id="123456789", domain="https://example.com")
        or
        >>> Route("GET", "customers/{customer_id}", customer_id="123456789", api_version="2020-08-01")
        """

        domain = base

        def __init__(self, method, path, *, domain=None, **parameters):
            if self.domain is not None and domain is None:
                domain = self.domain
            elif self.domain is None and domain is None:
                raise LookupError(
                    "Could not find a valid domain to use, either "
                    "specify it when calling the Route or "
                    "set it as a class variable."
                )

            self.method = method
            self.path = path

            if parameters:
                # Dict comprehension which url encodes all values in the `parameters` dict then formats it.
                path = path.format(
                    **{
                        k: quote(v) if isinstance(v, str) else v
                        for k, v in parameters.items()
                    }
                )

            self.url = urljoin(domain, path)

    return Route


def idempotent(func):
    def wrapper(*args, **kwargs):
        kwargs["idempotence"] = kwargs.get("idempotency", str(uuid.uuid4()))

        return func(*args, **kwargs)

    return wrapper


class HTTPClient:
    def __init__(self, token, environment, api_version):
        self.token = token
        self.__session = requests.session()
        self.api_version = api_version

        if environment == "production":
            self.Route = generate_route("https://connect.squareup.com/")
        elif environment == "sandbox":
            self.Route = generate_route("https://connect.squareupsandbox.com/")
        else:
            raise ValueError(f"Invalid environment '{environment}'")

    def request(self, route, **kwargs):
        method = route.method
        url = route.url
        log.debug(f"{method} {url} sending {kwargs.get('json', {})}")

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "Cache-Control": "no-cache",
            "Content-Type": "application/json",
        }

        if self.api_version is not None:
            headers.update({"Square-Version": self.api_version})

        kwargs["headers"] = headers

        r = self.__session.request(method, url, **kwargs)
        data = r.json()
        if 300 > r.status_code >= 200:
            log.debug(f"{method} {url} has received {data}")
            return data
        elif r.status_code == 404:
            raise ClientException(f"Unknown API path {route.url}")
        else:
            errors = []
            for error in data.get("errors", {}):
                if error["category"] == "API_ERROR":
                    errors.append(APIError(error=error))
                elif error["category"] == "AUTHENTICATION_ERROR":
                    errors.append(AuthenticationError(error=error))
                elif error["category"] == "INVALID_REQUEST_ERROR":
                    errors.append(InvalidRequest(error=error))
                elif error["category"] == "RATE_LIMIT_ERROR":
                    errors.append(RateLimited(error=error))
                elif error["category"] == "PAYMENT_METHOD_ERROR":
                    errors.append(PaymentMethodError(error=error))
                elif error["category"] == "REFUND_ERROR":
                    errors.append(RefundError(error=error))
            if len(errors) == 1:
                raise errors[0]
            else:
                raise MultipleExceptions(errors=errors)

    @idempotent
    def create_customer(self, **options):
        valid_keys = (
            "idempotency_key",
            "given_name",
            "family_name",
            "company_name",
            "nickname",
            "email_address",
            "address",
            "phone_number",
            "reference_id",
            "note",
            "birthday",
        )

        payload = {k: v for k, v in options.items() if k in valid_keys}

        return self.request(self.Route("POST", "v2/customers"), json=payload)

    def list_customers(self, **filters):
        valid_keys = ("cursor", "sort_field", "sort_order")

        payload = {k: v for k, v in filters.items() if k in valid_keys}

        return self.request(self.Route("GET", "v2/customers"), params=payload)

    def update_customer(self, customer_id, **options):
        valid_keys = (
            "given_name",
            "family_name",
            "company_name",
            "nickname",
            "email_address",
            "address",
            "phone_number",
            "reference_id",
            "note",
            "birthday",
        )
        payload = {k: v for k, v in options.items() if k in valid_keys}

        return self.request(
            self.Route(
                "PUT",
                "v2/customers/{customer_id}",
                customer_id=customer_id,
                json=payload,
            )
        )

    def delete_customer(self, customer_id):
        return self.request(
            self.Route("DELETE", "v2/customers/{customer_id}", customer_id=customer_id)
        )

    def search_customer(self, **filters):
        valid_keys = ("cursor", "limit", "query")

        payload = {k: v for k, v in filters.items() if k in valid_keys}
        return self.request(self.Route("POST", "v2/customers/search"), json=payload)

    def get_customer(self, customer_id):
        return self.request(
            self.Route("GET", "v2/customers/{customer_id}", customer_id=customer_id)
        )

    def create_card(self, customer_id, **options):
        valid_keys = (
            "card_nonce",
            "billing_address",
            "cardholder_name",
            "verification_token",
        )

        payload = {k: v for k, v in options.items() if k in valid_keys}

        return self.request(
            self.Route(
                "POST", "v2/customers/{customer_id}/cards", customer_id=customer_id
            ),
            json=payload,
        )

    def delete_card(self, customer_id, card_id):
        return self.request(
            self.Route(
                "DELETE",
                "v2/customers/{customer_id}/cards/{card_id}",
                customer_id=customer_id,
                card_id=card_id,
            )
        )

    def list_groups(self):
        return self.request(self.Route("GET", "v2/customers/groups"))

    @idempotent
    def create_group(self, **options):
        valid_keys = ("idempotency_key", "group")

        payload = {k: v for k, v in options.items() if k in valid_keys}

        return self.request(
            self.Route("POST", "v2/customers/groups"),
            json=payload,
        )

    def delete_group(self, group_id):
        return self.request(
            self.Route("DELETE", "v2/customers/groups/{group_id}", group_id=group_id)
        )

    def fetch_group(self, group_id):
        return self.request(
            self.Route("GET", "v2/customers/groups/{group_id}", group_id=group_id)
        )

    def update_group(self, group_id, **options):
        valid_keys = ("group",)

        payload = {k: v for k, v in options.items() if k in valid_keys}

        return self.request(
            self.Route("GET", "v2/customers/groups/{group_id}", group_id=group_id),
            json=payload,
        )

    def assign_group(self, customer_id, group_id):
        return self.request(
            self.Route(
                "PUT",
                "v2/customers/{customer_id}/groups/{group_id}",
                customer_id=customer_id,
                group_id=group_id,
            )
        )

    def unassign_group(self, customer_id, group_id):
        return self.request(
            self.Route(
                "DELETE",
                "v2/customers/{customer_id}/groups/{group_id}",
                customer_id=customer_id,
                group_id=group_id,
            )
        )

    def list_customer_segments(self):
        return self.request(self.Route("GET", "v2/customers/segments"))

    def fetch_customer_segment(self, segment_id):
        return self.request(
            self.Route(
                "GET", "v2/customers/segments/{segment_id}", segment_id=segment_id
            )
        )
