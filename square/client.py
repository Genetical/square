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
from datetime import datetime

from square import http
from square.ABC import SubEndpoint
from square.customer import Customer
from square.errors import *
from square.group import Group
from square.segment import Segment


class FuzzyQuery:
    def __init__(self, field, *, fuzzy=False):
        self.field = field
        self.fuzzy = fuzzy

    def as_query(self):
        if self.fuzzy:
            return {"fuzzy": self.field}
        else:
            return {"exact": self.field}


class GroupQuery:
    def __init__(self, any=None, all=None, none=None):
        self._any = any
        self._all = all
        self._none = none

    def as_query(self):
        r = {}

        if self._any is not None:
            r["any"] = self._any
        if self._all is not None:
            r["all"] = self._all
        if self._none is not None:
            r["none"] = self._none

        return r


class Customers(SubEndpoint):
    """Represents the customer sub-endpoint.
    Multi-function class representing the customer endpoints while providing
    idiomatic interfaces for the user.

    Methods
    -------
    list(**options)
        Returns a generator of customers.
    create(**options)
        Creates a new customer.
    search(limit=None, order=None, sort_by=None, **filters)
        Returns a list of customers who meet the filter.
    fetch(customer_id)
        Returns a customer with the given id.
    """

    def __repr__(self):
        return "<CustomerGenerator>"

    def list(self, **options):
        """Returns a generator of customers.
        Yields all customers. Sort can be changed by setting options.

        Parameters
        ----------
        cursor: Optional[str]
            Cursor used in the api to fetch the next chunk in a large response.
        sort_field: Optional[str]
            Specifies which fields should be used to sort.
            Must be either "default" or "created_at". This is an API restriction.
        sort_order: Optional[str]
            Order in which to sort. Must be either "ASC" or "DESC".

        Yields
        ------
        Customer
            Represents an individual customer.

        Notes
        -----
        This should always be accessed through the __iter__ dunder
        or the __call__ dunder if you want to set options however this function is set public
        for semantic reasons if someone wants to do `customers.list(**options)` over `customers(**options)`.

        As this function uses a generator, if you want to perform all the fetch calls at once,
        wrap this call in a list e.g:
        >>> list(customers.list())

        Examples
        --------
        Print the names of all customers
        >>> for customer in customer.list():
        >>>     print(customer.name)
        """
        while True:
            r = self._http.list_customers(**options)

            for customer in r.get("customers", []):
                yield Customer(data=customer, http=self._http)

            cursor = r.get("cursor")
            if cursor is not None:
                options.update({"cursor": cursor})
                continue
            else:
                break

    def __call__(self, **options):
        return self.list(**options)

    def create(self, **options):
        """Creates a new customer.
        Creates a customer with the values given in options.

        Parameters
        ----------
        idempotency_key: Optional[str]
            A unique idempotency key to ensure API calls are not repeated.
            If not given, one will be generated for you.
        given_name: Optional[str]
            The given (i.e., first) name associated with the customer profile.
        family_name: Optional[str]
            The family (i.e., last) name associated with the customer profile.
        company_name: Optional[str]
            A business name associated with the customer profile.
        nickname: Optional[str]
            A nickname for the customer profile.
        email_address: Optional[str]
            The email address associated with the customer profile.
        address: Optional[Address]
            The physical address associated with the customer profile.

        Returns
        -------
        Customer
            The newly created customer.

        Raises
        ------
        InvalidArgument
            If none of the minimum required parameters were given. See Warnings.
        TypeError
            If address was specified but was not of type Address.

        Notes
        -----
        At least one of the following parameters must be given:
            given_name, family_name, company_name, email_address, phone_number
        """
        return Customer._create(self._http, **options)

    def search(
        self, *, limit=None, order=None, sort_by=None, fetch_all=False, **filters
    ):
        """Searches for Customers.

        Returns a list of Customers which met the filters specified.

        limit: int
            The amount of results to return per page.

        sort_by: str, optional
            Specifies which fields should be used to sort.
            Must be either "default" or "created_at". This is an API restriction.

        order: str, optional
            Order in which to sort. Must be either "ASC" or "DESC".

        fetch_all: bool, default=False
            Will fetch all results at once if the response is paginated.
            Otherwise, the response will be fetched in blocks.

        created_at: Optional[Iterable[Datetime, Datetime]]
            Filter to Customers who were created between the
            first and second dates in the iterable.

        creation_source: Optional[Iterable]
            Filters to customers who were created by any method specified.
            See square.enums.CreationSource for more.
            Cannot be used with not_creation_source.

        not_creation_source: Optional[Iterable]
            Filters to customers who were not created by any method specified.
            See square.enums.CreationSource for more.
            Cannot be used with creation_source.

        email_address: Optional[Union[str, FuzzyQuery]]
            Filter by Customers with a specific email address.
            Use a FuzzyQuery object to specify if the request
            should be fuzzy (i.e: Doesn't look for exact match)

        groups: Optional[Union[Iterable, GroupQuery]]
            Filter by groups a user is in.
            If an Iterable is specified, the Customer must be in all of the
            specified groups. Use GroupQuery to specify all, any or none.

        phone_number: Optional[Union[str, FuzzyQuery]]
            Filter by Customers with a specific phone number.
            Use a FuzzyQuery object to specify if the request
            should be fuzzy (i.e: Doesn't look for exact match)
            Note: Must be in E.164 form.

        reference: Optional[Union[str, FuzzyQuery]]
            Filter by a users reference id. Specify a string for exact matching.
            Use a FuzzyQuery object to specify if the request
            should be fuzzy (i.e: Doesn't look for exact match)
            Note: This is case insensitive.

        updated_at: Optional[Iterable[Datetime, Datetime]]
            Filter to Customers who were updated between the
            first and second dates in the iterable.

        Yields
        ------
        Customer
            Represents an individual customer.

        Notes
        -----
        This function uses a generator. If you want to perform all the fetch calls at once,
        wrap this call in a list e.g:
        >>> list(customers.search())
        """

        options = {"query": {"filter": {}}}
        if limit is not None:
            if not 1 <= limit <= 100:
                raise InvalidArgument(
                    "limit must be within the ranges 1-100 inclusive."
                )
            else:
                options["limit"] = limit
        if order is not None:
            if order.upper() not in ("DESC", "ASC"):
                raise InvalidArgument("sort must be either ASC or DESC")
            else:
                options["query"]["order"] = order
        if sort_by is not None and sort_by.upper() not in ("DEFAULT", "CREATED_AT"):
            raise InvalidArgument("sort_by must be either DEFAULT or CREATED_AT")

        created_at = filters.get("created_at")
        if created_at is not None:
            if isinstance(created_at, (tuple, list)) and len(created_at) == 2:
                start_at, end_at = created_at
                if isinstance(start_at, datetime) and isinstance(end_at, datetime):
                    options["query"]["filter"]["created_at"] = {
                        "end_at": end_at,
                        "start_at": start_at,
                    }
                else:
                    raise InvalidArgument(
                        "created_at must contain two datetime objects"
                    )
            else:
                raise InvalidArgument("created_at must be a tuple with length of two")

        creation_source = filters.get("creation_source")
        not_creation_source = filters.get("not_creation_source")

        if creation_source and not_creation_source:
            raise InvalidArgument(
                "Cannot specify both creation_source and not_creation_source"
            )
        elif creation_source or not_creation_source:
            if creation_source:
                rule = "INCLUDE"
                values = creation_source
            else:
                rule = "EXCLUDE"
                values = not_creation_source

            if not isinstance(values, list):
                values = [values]

            options["query"]["filter"]["creation_source"] = {
                "rule": rule,
                "values": values,
            }

        email_address = filters.get("email_address")
        if email_address is not None:
            if isinstance(email_address, str):
                options["email_address"] = {"exact": email_address}
            elif isinstance(email_address, FuzzyQuery):
                options["email_address"] = email_address.as_query()
            else:
                raise InvalidArgument(
                    f"email_address must be str or FuzzyQuery, not {type(email_address)}"
                )

        groups = filters.get("groups")
        if groups is not None:
            if isinstance(groups, GroupQuery):
                options["query"]["group_ids"] = groups.as_query()
            elif isinstance(groups, (list, tuple, set)):
                options["query"]["group_ids"] = {"all": groups}

        phone_number = filters.get("phone_number")
        if phone_number is not None:
            if isinstance(phone_number, str):
                options["query"]["filter"]["phone_number"] = {"exact": phone_number}
            elif isinstance(phone_number, FuzzyQuery):
                options["query"]["filter"]["phone_number"] = phone_number.as_query()
            else:
                raise InvalidArgument(
                    f"phone_number must be str or FuzzyQuery, not {type(phone_number)}"
                )

        reference = filters.get("reference")
        if reference is not None:
            if isinstance(reference, str):
                options["query"]["filter"]["reference_id"] = {"exact": reference}
            elif isinstance(phone_number, FuzzyQuery):
                options["query"]["filter"]["reference_id"] = reference.as_query()
            else:
                raise InvalidArgument(
                    f"reference must be str or FuzzyQuery, not {type(reference)}"
                )

        updated_at = filters.get("updated_at")
        if updated_at is not None:
            if isinstance(updated_at, (tuple, list)) and len(updated_at) == 2:
                start_at, end_at = updated_at
                if isinstance(start_at, datetime) and isinstance(end_at, datetime):
                    options["query"]["filter"]["updated_at"] = {
                        "end_at": end_at,
                        "start_at": start_at,
                    }
                else:
                    raise InvalidArgument(
                        "updated_at must contain two datetime objects"
                    )
            else:
                raise InvalidArgument("updated_at must be a tuple with length of two")

        customers = []
        while True:
            resp = self._http.search_customer(**options)
            if fetch_all:
                customers += [
                    Customer(data=c, http=self._http) for c in resp.get("customers", [])
                ]
            else:
                for c in resp.get("customers", []):
                    yield Customer(data=c, http=self._http)
            cursor = resp.get("cursor")
            if cursor is not None:
                options.update({"cursor": cursor})
            else:
                break
        if fetch_all:
            return customers
        else:
            return

    def fetch(self, customer_id):
        return Customer(data=self._http.get_customer(customer_id), http=self._http)


class Groups(SubEndpoint):
    """Represents the Group sub-endpoints

    Multi-function class representing the group endpoints while providing
    idiomatic interfaces for the user.

    Methods
    -------
    list(**options)
        Returns a generator of Groups.
    create(**options)
        Creates a new Group.
    fetch(group_id)
        Returns a Group with the given id if it exists.
    """

    def __repr__(self):
        return "<CustomerGroups>"

    def list(self, **options):
        while True:
            r = self._http.list_groups()

            for customer in r.get("groups", []):
                yield Group(data=customer, http=self._http)

            cursor = r.get("cursor")
            if cursor is not None:
                options.update({"cursor": cursor})
                continue
            else:
                break

    def fetch(self, group_id):
        return Group(data=self._http.fetch_group(group_id), http=self._http)

    def create(self, **options):
        return Group.create(self._http, **options)


class CustomerSegments(SubEndpoint):
    """Represents the Customer Segments sub-endpoints

    Multi-function class representing the Customer Segment endpoints while providing
    idiomatic interfaces for the user.

    Methods
    -------
    list(**options)
        Returns a generator of customers.
    fetch(group_id)
        Returns a customer with the given id.
    """

    def __repr__(self):
        return "<CustomerSegments>"

    def list(self, **options):
        while True:
            r = self._http.list_customer_segments()

            for segment in r.get("segments", []):
                yield Segment(data=segment, http=self._http)

            cursor = r.get("cursor")
            if cursor is not None:
                options.update({"cursor": cursor})
                continue
            else:
                break

    def fetch(self, segment_id):
        return Segment(
            data=self._http.fetch_customer_segment(segment_id), http=self._http
        )


class SquareClient:
    """Represents an API client for the Square API.
    This class is used to interact with the Square API and Webhooks.

    Parameters
    ----------
    token: str
        The API authentication _token. Do not prefix this _token with
        Bearer or anything else, this will be done for you.

    environment: str
        The development environment. This will affect which endpoint
        will be used. Must be either "sandbox" or "production".

    Attributes
    ----------
    api_version: str
        The version of the API to be used.
    """

    def __init__(self, token, *, environment, api_version=None):
        self._token = token
        self._client = http.HTTPClient(self._token, environment, api_version)
        self.api_version = api_version

        self.customers: Customers = Customers(self._client)
        self.groups: Groups = Groups(self._client)
