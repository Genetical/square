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
from square.enums import CardBrand, CardPrepaidType, try_enum
from square.objects import Address
from square.errors import InvalidArgument


class Cards:
    def __init__(self, cards, *, customer, http):
        self._cards = cards
        self._customer = customer
        self._http = http

    def __iter__(self):
        return self._cards

    def new(self, **options):
        try:
            options["card_nonce"]
        except KeyError:
            raise InvalidArgument("Missing required argument card_nonce")

        billing_address = options.get("billing_address")
        if billing_address is not None:
            if not isinstance(billing_address, Address):
                raise TypeError("billing_address must be type Address")
            else:
                options["billing_address"] = billing_address.to_dict()

        resp = self._http.create_customer(self._customer.id, **options).get("card")
        card = Card(data=resp, customer=self._customer, http=self._http)
        if resp is not None:
            self._cards.append(card)

        return card


class Card:
    def __init__(self, *, data, customer, http):
        self._from_data(data)
        self._customer = customer
        self._http = http

    def _from_data(self, card):
        self.id = card.get("id")
        _ = card.get("billing_address")
        self.billing_address = Address(data=_) if _ is not None else _
        self.bin = card.get("bin")
        self.card_brand = try_enum(CardBrand, card.get("card_brand"))
        self.card_type = card.get("card_type")
        self.cardholder_name = card.get("cardholder_name")
        self.exp_month = card.get("exp_month")
        self.exp_year = card.get("exp_year")
        self.fingerprint = card.get("fingerprint")
        self.last_4 = card.get("last_4")
        self.prepaid_type = try_enum(CardPrepaidType, card.get("prepaid_type"))

    def delete(self):
        self._http.delete_card(self.id, self._customer.id)
