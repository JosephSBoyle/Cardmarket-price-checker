from functools import partial
from unittest.mock import patch

import pandas as pd
from requests import Response

from src.offers import extract_market_offers, extract_user_offers


def _mock_get_request(*_args, content_fp: str, **_kwargs):
    """Mock of ``requests.get`` that loads content from disk as the response.

    :param content_fp: The path of the file to load response content from.
    """
    with open(content_fp, "r") as f:
        content = f.read()

    res = Response()
    res._content = content
    res.status_code = 200
    return res


_mock_get_user_offers = partial(
    _mock_get_request,
    content_fp="tests/fixtures/sample_user_offers.html",
)

_mock_get_market_offers = partial(
    _mock_get_request,
    content_fp="tests/fixtures/sample_market_offers.html",
)


@patch("requests.get", _mock_get_user_offers)
def test_extract_from_users_offers_page():
    """Test extracting offers from user's page into a pandas dataframe."""

    df = extract_user_offers(
        "https://www.cardmarket.com/en/Magic/Users/Extasia1/Offers/Singles", max_pages=1
    )
    assert isinstance(df, pd.DataFrame)

    assert df.card_name.dtype == object  # str
    assert df.cond.dtype == object  # str

    assert df.price.dtype == object  # Decimal
    assert df.is_foil.dtype == bool  # bool

    # assert df.avail.dtype == int  # int64 FIXME BROKEN on WINDOWS
    
    assert df.language.dtype == object  # str
    assert df.marketplace_url.dtype == object  # str

    assert len(df.index) >= 1


@patch("requests.get", _mock_get_market_offers)  # Avoid making a network call.
def test_extract_market_offers():
    """Test extracting offers from the public marketplace url."""

    test_product_url = "https://www.cardmarket.com/en/Magic/Products/Singles/Friday-Night-Magic-Promos/Aether-Hub"
    df = extract_market_offers(test_product_url)
    assert isinstance(df, pd.DataFrame)

    assert df.price.dtype == object  # Decimal
    assert df.cond.dtype == object  # Decimal

    assert df.user_name.dtype == object  # str
    assert df.user_uri.dtype == object  # str
    # assert df.avail.dtype == int  # int64 FIXME BROKEN on WINDOWS
    # assert df.user_sales.dtype == int  # int64 BROKEN on WINDOWS

    # Assert that there is at least 1 copy of this item for sale
    # (if they don't then find another item url.)
    assert len(df.index) >= 1
