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
from square.ABC import SquareObject, CreateUpdatedAtMixin


class Group(CreateUpdatedAtMixin, SquareObject):
    """Represents a group of customer profiles.

    Represents a customer group belonging to the current merchant.

    Attributes
    ----------
    id: str
        Unique Square-generated ID for the customer group.
    name: str
        Name of the customer group.
    created_at: datetime
        The timestamp when the customer group was created.
    updated_at: datetime
        The timestamp when the customer group was last updated.

    Methods
    -------
    edit(**options)
        Updates a customer group.
    delete()
        Deletes a customer group.
    """

    __slots__ = ("id", "name", "created_at", "updated_at", "_http")

    def __repr__(self):
        return f"<Group(id={self.id}, name={self.name})>"

    @classmethod
    def _create(cls, http, idempotency_key, *, name, **group):
        data = {"group": {**group}, "idempotency_key": idempotency_key}
        data.update({"name": name})

        resp = http.create_group(group=data)

        return cls(data=resp.get("group", {}), http=http)

    def edit(self, **options):
        """Updates a customer group.

        Parameters
        ----------
        id: int
        name: str
        created_at: datetime
        updated_at: datetime

        Returns
        -------
        Group
            The updated group

        Notes
        -----
        You can discard the return as this object will also be updated.
        """

        if not options:
            return self

        fields = {"group": {}}

        name = options.get("name")
        if name is not None:
            fields["group"]["name"] = name

        resp = self._http.update_group(self.id, **fields)

        for field, value in resp.get("group", {}).items():
            self.__setattr__(field, value)

        return self

    def delete(self):
        """Deletes a customer group."""
        return self._http.delete_group(self.id)
