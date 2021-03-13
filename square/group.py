#  The MIT License (MIT)
#  Copyright (c) 2021-present Genetical
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
from dateutil import parser

from square.ABC import SquareObject


class Group(SquareObject):
    __slots__ = (
        "id",
        "name",
        "created_at",
        "updated_at",
        "_http"
    )

    def __repr__(self):
        return f"<Group(id={self.id}, name={self.name})>"

    def _from_data(self, group):
        self.id = group.get("id")
        self.name = group.get("name")
        _ = group.get("created_at")
        self.created_at = (
            parser.parse(_) if _ is not None else _
        )

        _ = group.get("updated_at")
        self.updated_at = (
            parser.parse(_) if _ is not None else _
        )

    @classmethod
    def create(cls, http, **options):
        try:
            name = options["name"]
        except KeyError:
            raise ValueError("Missing required argument name")

        data = {"group": {"name": name}}

        resp = http.create_group(group=data)

        return cls(data=resp.get("group", {}), http=http)

    def edit(self, **options):
        fields = {"group": {}}

        name = options.get("name")
        if name is not None:
            fields["group"]["name"] = name

        resp = self._http.update_group(self.id, **fields)

        for field, value in resp.get("group", {}).items():
            self.__setattr__(field, value)

    def delete(self):
        return self._http.delete_group(self.id)