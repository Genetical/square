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
    __slots__ = ("month", "day", "_timestamp", "_dto")

    def __repr__(self):
        return f"<Birthday(month={self.month}, day={self.day})>"

    @classmethod
    def from_timestamp(cls, timestamp):
        self = object.__new__(cls)
        self._timestamp = timestamp

        if timestamp.startswith("0000"):
            timestamp = "0004" + timestamp[5:]

        self._dto = parser.parse(timestamp)
        self.month = self._dto.month
        self.day = self._dto.day

    def isoformat(self):
        timestamp = self._dto.isoformat()

        if timestamp.startswith("0004"):
            timestamp = "0000" + timestamp[5:]

        return timestamp


class Customer(SquareObject):
    __slots__ = (
        "id",
        "address",
        "birthday",
        "cards",
        "company_name",
        "created_at",
        "creation_source",
        "email_source",
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
        self.email_source = customer.get("email_address")
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
        try:
            address = fields["address"]
        except KeyError:
            pass
        else:
            if not isinstance(address, Address):
                raise InvalidArgument("address field must be of type Address")
            fields["address"] = address.to_dict()

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
        if not len(set(options.keys()).intersection(required_identifier)):
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
            options["address"] = address.to_dict()

        resp = http.create_customer(**options)

        return cls(data=resp.get("customer", {}), http=http)

    def assign_group(self, group):
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
    def __init__(self, *, data):
        self._from_data(data)

    def _from_data(self, preferences):
        self.email_unsubscribed = preferences.get("email_unsubscribed")
