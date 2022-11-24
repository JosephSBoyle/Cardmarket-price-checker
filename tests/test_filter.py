from src.filter_ import build_query
import pytest


def test_filter_by_country_only():
    x = build_query(seller_country="GREAT_BRITAIN")
    assert x == "?sellerCountry=13"


def test_filter_by_country_and_condition():
    query = build_query(seller_country="GREAT_BRITAIN", min_condition="PL")
    assert query == "?sellerCountry=13&minCondition=6"


def test_filter_by_country_condition_and_foil():
    query = build_query(
        seller_country="GREAT_BRITAIN",
        min_condition="MT",
        is_foil=True,
    )
    assert query == "?sellerCountry=13&minCondition=1&isFoil=Y"


@pytest.mark.parametrize(
    "language, expected_code",
    [
        ("english", 1),
        ("french", 2),
        ("german", 3),
        ("spanish", 4),
        ("italian", 5),
        ("s-chinese", 6),
        ("japanese", 7),
        ("portuguese", 8),
        ("russian", 9),
        ("korean", 10),
        ("t-chinese", 11),
        # Test mixed-casing
        ("English", 1),
        ("ruSsiaN", 9),
        ("t-cHinese", 11),
    ],
)
def test_filter_by_language(language, expected_code):
    query = build_query(language=language)
    assert query == f"?language={expected_code}"