import pandas as pd

from src.offers import extract_market_offers, extract_user_offers


def test_extract_from_users_offers_page():
    """Test extracting offers from user's page into a pandas dataframe."""

    test_username = "Extasia1"
    url = (
        "https://www.cardmarket.com/en/Magic/Users/" + test_username + "/Offers/Singles"
    )

    df = extract_user_offers(url)
    assert isinstance(df, pd.DataFrame)

    assert df.card_name.dtype == object  # str
    assert df.cond.dtype == object  # str

    assert df.avail.dtype == int  # int64
    assert df.price.dtype == object  # Decimal
    assert df.marketplace_url.dtype == object  # str

    # Assert this user has at least 1 item for sale
    # (if they don't then change the test user.)
    assert len(df.index) >= 1


def test_extract_market_offers():
    """Test extracting offers from the public marketplace url."""

    test_product_url = "https://www.cardmarket.com/en/Magic/Products/Singles/Friday-Night-Magic-Promos/Aether-Hub"
    df = extract_market_offers(test_product_url)
    assert isinstance(df, pd.DataFrame)

    assert df.price.dtype == object  # Decimal
    assert df.cond.dtype == object  # Decimal

    assert df.user_name.dtype == object  # str
    assert df.user_uri.dtype == object  # str
    assert df.user_sales.dtype == int

    # Assert that there is at least 1 copy of this item for sale
    # (if they don't then find another item url.)
    assert len(df.index) >= 1
