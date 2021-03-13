import warnings
from dateutil import parser


def yr_naive(data):
    if data[0:4] == "0000":
        data = "0001" + data[4:]
        warnings.warn(
            "Year naive datetimes are not supported by the datetime module. As such, a default year of "
            f"0001 has been set. ({data})\n"
            "This will be automatically replaced with 0000 if used in an api call."
        )

    return parser.parse(data)
