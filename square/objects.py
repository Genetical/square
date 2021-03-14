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
import pycountry

from square.ABC import SquareObject


class Address(SquareObject):
    """Represents a physical address.

    Attributes
    ----------
    address_line_1: str
        The first line of the address.
    address_line_2: str, optional
        The second line of the address.
    address_line_3: str, optional
        The third line of the address.
    administrative_district_level_1: str
        A civil entity within the address's country.
        In the US, this is the state.
    administrative_district_level_2: str
        A civil entity within the address's
        `administrative_district_level_1`.
        In the US, this is the county.
    administrative_district_level_3: str
        A civil entity within the address's
        `administrative_district_level_2`.
    country: pycountry.db.Country
        The address's country
    first_name: str, optional
        First name when it's representing recipient.
    last_name: str, optional
        Last name when it's representing recipient.
    locality: str
        The city or town of the address.
    organization: str, optional
        Organization name when it's representing recipient.
    postal_code: str
        The address's postal code.
    sublocality: str, optional
    A civil region within the address's locality.
    sublocality_2: str, optional
        A civil region within the address's sublocality.
    sublocality_3: str, optional
        A civil region within the address's sublocality_2.
    name: str, optional
        Returns a full name (if available).
    district: str, optional
        Returns a full district (if available).
    full_address: str, optional
        Returns a full address (if available).
    """
    def _from_data(self, address):
        self.address_line_1 = address.get("address_line_1")
        self.address_line_2 = address.get("address_line_2")
        self.address_line_3 = address.get("address_line_3")
        self.administrative_district_level_1 = address.get(
            "administrative_district_level_1"
        )
        self.administrative_district_level_2 = address.get(
            "administrative_district_level_2"
        )
        self.administrative_district_level_3 = address.get(
            "administrative_district_level_3"
        )
        try:
            self.country = pycountry.countries.get(alpha_2=address.get("country"))
        except LookupError:
            self.country = None
        self.first_name = address.get("first_name")
        self.last_name = address.get("last_name")
        self.locality = address.get("locality")
        self.organization = address.get("organization")
        self.postal_code = address.get("porstal_code")
        self.sublocality = address.get("sublocality")
        self.sublocality_2 = address.get("sublocality_2")
        self.sublocality_3 = address.get("sublocality_3")

    @property
    def name(self):
        """Attempts to construct a full name.

        Will return the first name and last name as a string or just
        the first name if no last name exists or None if neither are
        available.

        Returns
        -------
        str or None:
            The full name of the person (If available).
        """
        _ = (
            f"{self.first_name} {self.last_name}"
            if self.last_name is not None
            else self.first_name
        )
        return _ if _ else None

    @property
    def district(self):
        """Attempts to construct a full district name.

        Will return all three administrative districts separated by
        commas. If any are none, they will be skipped. None will be
        returned if no administrative district is set.

        Returns
        -------
        str or None:
            The full administrative district
        """
        _ = ",".join(
            filter(
                None,
                (
                    self.administrative_district_level_1,
                    self.administrative_district_level_2,
                    self.administrative_district_level_3,
                ),
            )
        )
        if _:
            return _
        else:
            return None

    @property
    def full_address(self):
        """Attempts to construct a full user address.

        Follows the standard format of an international address.
        Each element is separated by a new line and only added
        if it is not None.

        Returns
        -------
        str or None:
            A fully qualified physical address (Or less).
        """
        _ = "\n".join(
            [
                line
                for line in (
                    self.name,
                    self.address_line_1,
                    self.address_line_2,
                    self.address_line_3,
                    self.locality,
                    self.postal_code,
                    self.district,
                    self.country,
                )
                if line is not None
            ]
        )
        if _:
            return _
        else:
            return None

    def __str__(self):
        return self.full_address

    def _to_dict(self):
        data = {k: v for k, v in self.__dict__.items() if v is not None}

        if "country" in data.keys():
            data["country"] = data["country"].alpha_2

        return data
