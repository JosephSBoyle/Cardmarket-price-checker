"""Construct a query string suffix for filtering on specific attributes.

Supported attributes are:

- Condition
- Country  
- Foil
- Language
- Quantity  TODO

"""
from typing import Optional
from urllib.parse import urlencode


def build_query(
    *,
    seller_country: Optional[str] = None,
    min_condition: Optional[str] = None,
    language: Optional[str] = None,
    is_foil: Optional[bool] = None,
):
    """Return a query string of the given filters."""

    filters = []
    if seller_country:
        filters.append(_by_seller_country(seller_country))

    if min_condition:
        filters.append(_by_condition(min_condition))

    if language:
        filters.append(_by_language(language))

    if is_foil is not None:  # False is a valid value!
        filters.append(_by_foil(is_foil))

    return "?" + urlencode(filters)


# TODO fill in other countries
COUNTRIES: dict[str, int] = {
    "GREAT_BRITAIN": 13,
}

CONDITIONS: dict[str, int] = {
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

FOIL: dict[bool, str] = {
    True: "Y",
    False: "N",
}

LANGUAGES: dict[str, int] = {
    "english": 1,
    "french": 2,
    "german": 3,
    "spanish": 4,
    "italian": 5,
    "s-chinese": 6,
    "japanese": 7,
    "portuguese": 8,
    "russian": 9,
    "korean": 10,
    "t-chinese": 11,
}
"""Map of languages to integer cardmarket codes.

Note: is public since it's used in ``offers.py`` to create a regex pattern.
"""


def _by_seller_country(country: str):
    code = COUNTRIES[country]
    return ("sellerCountry", code)


def _by_condition(condition: str):
    code = CONDITIONS[condition]
    return ("minCondition", code)


def _by_foil(is_foil: bool):
    code = FOIL[is_foil]
    return ("isFoil", code)


def _by_language(language: str):
    language = language.lower()
    code = LANGUAGES[language]
    return ("language", code)
