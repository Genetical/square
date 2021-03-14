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
from dateutil import parser

from square.group import Group
from square.helpers import yr_naive
from square.enums import CreationSource, try_enum
from square.errors import InvalidArgument
from square.card import Card, Cards
from square.objects import Address
from square.ABC import SquareObject


class Birthday:
    """Represents a Customer's birthday.

    This was created as a solution to the year-naive datetime objects
    sometimes given by the API for birthdays.

    Attributes
    ----------
    month: int
        The month of the birthday as an integer between 1 and 12 (incl)
    day: int
        The day of the birthday as an integer between 1 and 31 (incl)
    _dto: datetime
        The datetime object `Birthday` wraps around. This is documented
        in case you want a valid datetime object to manipulate.
        HOWEVER: The year will be set to 0004AD as a placeholder value.
    _timestamp: str
        The raw datetime string given by the API

    Methods
    -------
    from_timestamp(timestamp)
        Class method constructor for the object, will take an RFC3339
        datetime string.
    isoformat():
        Returns an ISO8601 (RFC3339 Compatible) datetime string.
        This serialises the internal datetime object and replaces the
        year, so it is (somewhat) safe to manipulate `_dto` and expect
        your output string to look somewhat normal.

    Warnings
        This is NOT a perfect solution. There are edge cases which you
        must consider:
          - `isoformat` assumes any year under 1000 is a placeholder and
            WILL replace it with 0000. This is so that it still
            serialises correctly if you were to increase the enough to
            make the year tick over.
          - If you do perform manipulations to the internal datetime
            and you increase the year, keep in mind that February 29th
            will not be considered valid as the dto will no longer
            think it is a leap year.

        Overall, DON'T mess with the internal datetime object if you
        can help it. You will likely have unexpected behaviour.

    """
    __slots__ = ("month", "day", "_timestamp", "_dto")

    def __repr__(self):
        return f"<Birthday(month={self.month}, day={self.day})>"

    @classmethod
    def from_timestamp(cls, timestamp):
        """Parses an RFC3339 datetime string.
        This method will manipulate the string so it becomes ISO
        compatible and therefore parsable by the datetime module.

        Parameters
        ----------
        timestamp: str
            An ISO8601 or RFC3339 datetime string.

        Notes
        -----
        The year 0004AD is used as it is a leap year.
        """
        self = object.__new__(cls)
        self._timestamp = timestamp

        if timestamp.startswith("0000"):
            timestamp = "0004" + timestamp[5:]

        self._dto = parser.parse(timestamp)
        self.month = self._dto.month
        self.day = self._dto.day

    def isoformat(self):
        """Serialises this object datetime string.

        Returns
        -------
        str
            An RFC3339 (ISO8601 compatible) datetime string.
        """
        timestamp = self._dto.isoformat()

        if timestamp.startswith("0004"):
            timestamp = "0000" + timestamp[5:]

        return timestamp


class Customer(SquareObject):
    """Represents a Square customer profile

    Attributes
    ----------
    id: str or None
        A unique Square-assigned ID for the customer profile.
    created_at: datetime
        The timestamp when the customer profile was created.
    updated_at: datetime
        The timestamp when the customer profile was last updated.
    cards: Cards
        Payment details of cards stored on file for the customer
        profile.
    given_name: str or None
        The given (i.e., first) name associated with the customer
        profile.
    family_name: str or None
        The family (i.e., last) name associated with the customer
        profile.
    nickname: str or None
        A nickname for the customer profile.
    company_name: str or None
        A business name associated with the customer profile.
    email_address: str or None
        The email address associated with the customer profile.
    address: Address or None
        The physical address associated with the customer profile.
    phone_number: str or None
        The 11-digit phone number associated with the customer profile.
    birthday: Birthday or None
        The birthday associated with the customer profile. See the
        `Birthday` docstring for more information.
    reference_id: str or None
        A second ID used to associate the customer profile with an
        entity in another system.
    note: str or None
        A custom note associated with the customer profile.
    preferences: CustomerPreferences
        Represents general customer preferences.
    groups: TODO: ADD
        The customer groups and segments the customer belongs to.
    creation_source: CreationSource
        A creation source represents the method used to create the
        customer profile.
    group_ids: List[str]
        The IDs of customer groups the customer belongs to.
    segment_ids: List[str]
        The IDs of segments the customer belongs to.
    name: str or None
        Gives the full name of the customer (if available).

    Methods
    -------
    edit(**fields)
        Change one or more attributes of a customer.
    delete()
        Delete a customer.
    assign_group(group)
        Adds a group membership to a customer.
    unassign_group(group)
        Removes a group membership from a customer.
    """
    __slots__ = (
        "id",
        "address",
        "birthday",
        "cards",
        "company_name",
        "created_at",
        "creation_source",
        "email_address",
        "family_name",
        "given_name",
        "group_ids",
        "nickname",
        "note",
        "phone_number",
        "preferences",
        "reference_id",
        "segment_ids",
        "updated_at",
        "_http",
    )

    def __repr__(self):
        return f"<Customer(id={self.id} name={self.name})>"

    def _from_data(self, customer):
        self.id = customer.get("id")
        _ = customer.get("address")
        self.address = Address(data=_) if _ is not None else _
        _ = customer.get("birthday")
        self.birthday = yr_naive(_) if _ is not None else _
        self.cards = Cards(
            [
                Card(data=data, http=self._http, customer=self)
                for data in customer.get("cards", [])
            ],
            customer=self,
            http=self._http,
        )
        self.company_name = customer.get("company_name")
        _ = customer.get("created_at")
        self.created_at = parser.parse(_) if _ is not None else _
        self.creation_source = try_enum(CreationSource, customer.get("creation_source"))
        self.email_address = customer.get("email_address")
        self.family_name = customer.get("family_name")
        self.given_name = customer.get("given_name")
        self.group_ids = customer.get("group_ids", [])
        self.nickname = customer.get("nickname")
        self.note = customer.get("note")
        self.phone_number = customer.get("phone_number")
        self.preferences = CustomerPreferences(data=customer.get("preferences", {}))
        self.reference_id = customer.get("reference_id")
        self.segment_ids = customer.get("segment_ids", [])
        _ = customer.get("updated_at")
        self.updated_at = parser.parse(_) if _ is not None else _

    @property
    def name(self):
        _name = self.given_name
        if self.family_name is not None:
            return _name + (" " + self.family_name)
        else:
            return _name

    def edit(self, **fields):
        """Updates the details of an existing customer.

        Parameters
        ----------
        given_name: str, optional
        family_name: str, optional
        company_name: str, optional
        nickname: str, optional
        email_address: str, optional
        address: Union[Address, dict], optional
        phone_number: str, optional
        reference_id: str, optional
        note: str, optional
        birthday: Birthday, optional

        Returns
        -------
        Customer
            The updated customer.

        Notes
        -----
        You do not need to capture the return value as this object
        will be updated too.
        """

        if not fields:
            # No need to make an API call if no changes are given.
            # TODO: Check fields with existing values.
            # TODO: If all are the same, just return.
            return self

        try:
            address = fields["address"]
        except KeyError:
            pass
        else:
            if isinstance(address, Address):
                fields["address"] = address._to_dict()
            elif isinstance(address, dict):
                pass
            else:

        resp = self._http.update_customer(self.id, fields)

        for field, value in resp.get("customer", {}).items():
            self.__setattr__(field, value)

        return self

    def delete(self):
        return self._http.delete_customer(self.id)

    @classmethod
    def _create(cls, http, **options):
        required_identifier = (
            "given_name",
            "family_name",
            "company_name",
            "email_address",
            "phone_number",
        )
        if not set(options.keys()).intersection(required_identifier):
            raise InvalidArgument(
                "create_customer requires at least one of the following:\n"
                f"{required_identifier}"
            )

        try:
            address = options["address"]
        except KeyError:
            pass
        else:
            if not isinstance(address, Address):
                raise TypeError("address field must be of type Address")
            options["address"] = address._to_dict()

        resp = http.create_customer(**options)

        return cls(data=resp.get("customer", {}), http=http)

    def assign_group(self, group):
        """Adds a group membership to a customer.

        Parameters
        ----------
        group: Union[Group, str]
            The Group to add the user to. The group ID can also be
            given as a string.
        """
        if isinstance(group, Group):
            group_id = group.id
        elif isinstance(group, str):
            group_id = group
        else:
            raise InvalidArgument(
                f"Unsupported type {type(group)} for argument group, must be str or Group."
            )
        self._http.assign_group(self.id, group_id)
        self.group_ids.append(group_id)

    def unassign_group(self, group):
        """Removes a group membership from a customer.

        Parameters
        ----------
        group: Union[Group, str]
            The Group to remove the user from. The group ID can also be
            given as a string.
        """
        if isinstance(group, Group):
            group_id = group.id
        elif isinstance(group, str):
            group_id = group
        else:
            raise InvalidArgument(
                f"Unsupported type {type(group)} for argument group, must be str or Group."
            )
        self._http.unassign_group(self.id, group_id)
        self.group_ids.remove(group_id)


class CustomerPreferences:
    """Represents general customer preferences.
    This object shadows the one on the Square API.

    Attributes
    ----------
    email_unsubscribed: bool
        The customer has unsubscribed from receiving marketing campaign
        emails.

    """
    def __init__(self, *, data):
        self._from_data(data)

    def _from_data(self, preferences):
        self.email_unsubscribed = preferences.get("email_unsubscribed")
