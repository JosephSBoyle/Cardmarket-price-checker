from src.offers import extract

import pandas as pd


def test_extract_offers():
    """Test extracting offers from user's page into a pandas dataframe."""
    test_username = "Extasia1"

    df = extract(test_username)

    assert isinstance(df, pd.DataFrame)

    assert df.name.dtype == object  # str
    assert df.cond.dtype == object  # str

    assert df.avail.dtype == int  # int64
    assert df.price.dtype == object  # Decimal

    # Assert this user has at least 1 item for sale 
    # (if they don't then change the test user.)
    assert len(df.index) >= 1
