import pycountry


class Address:
    def __init__(self, *, data):
        self._from_data(data)

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
        return (
            f"{self.first_name} {self.last_name}"
            if self.last_name is not None
            else self.first_name
        )

    @property
    def district(self):
        return ",".join(
            filter(
                None,
                (
                    self.administrative_district_level_1,
                    self.administrative_district_level_2,
                    self.administrative_district_level_3,
                ),
            )
        )

    @property
    def full_address(self):
        return "\n".join(
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
                if line
            ]
        )

    def __str__(self):
        return self.full_address

    def to_dict(self):
        data = {k: v for k, v in self.__dict__.items() if v is not None}

        if "country" in data.keys():
            data["country"] = data["country"].alpha_2

        return data
