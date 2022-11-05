from src.filter_ import build_query


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
