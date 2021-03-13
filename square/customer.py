from dateutil import parser

from square.group import Group
from square.helpers import yr_naive
from square.enums import CreationSource, try_enum
from square.errors import InvalidArgument
from square.card import Card, Cards
from square.objects import Address
from square.ABC import SquareObject


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
        self.address = Address(data=customer.get("address", {}))
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
