"""Construct a query string suffix for filtering on specific attributes.

Supported attributes are:

- Condition
- Country  
- Quantity  TODO

"""
from urllib.parse import urlencode


def build_query(
    *,
    seller_country: str = None,
    min_condition: str = None,
):
    """Return a query string of the given filters"""

    filters = []
    if seller_country:
        filters.append(_by_seller_country(seller_country))

    if min_condition:
        filters.append(_by_condition(min_condition))

    return "?" + urlencode(filters)


# TODO fill in other countries
_COUNTRIES: dict[str, int] = {
    "GREAT_BRITAIN": 13,
}

_CONDITIONS: dict[str, int] = {
    "MT": 1,  # mint
    "NM": 2,  # near mint
    "EX": 3,  # excellent
    "GD": 4,  # good
    "LP": 5,  # lightly played
    "PL": 6,  # played
    "PO": 7,  # poor
}
"""Map of conditions to cardmarket's numerical encoding.

e.g "MT" -> 1, "GD" -> 4
"""


def _by_seller_country(country: str):
    code = _COUNTRIES[country]
    return ("sellerCountry", code)


def _by_condition(condition: str):
    code = _CONDITIONS[condition]
    return ("minCondition", code)
