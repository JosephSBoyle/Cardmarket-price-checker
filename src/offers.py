"""Module for extracting a user's cardmarket offers based on their unique cardmarket name."""
import pandas as pd
import requests
import bs4
from decimal import Decimal
from re import sub


def extract_user_offers(url: str) -> pd.DataFrame:
    """Extract a dataframe containing each of a user's offers.

    - TODO find the next page link and recursively append to the pandas dataframe.
    """
    rows = _get_table_rows(url)

    table_values = []
    for row in rows:
        # list(row.stripped_strings) example:
        # ['CardName', 'condition (e.g NM | PO | EX ), 'n avail.', '0.20 $', '0.20', '2']
        row_values = list(row.stripped_strings)

        # TODO get rid of magic number: use a helper that filters on conditions perhaps?
        # It's important to ensure this link is correct, we can create a validate row method perhaps.
        product_url = row.find_all("a")[0]["href"]
        table_values.append(
            {
                "card_name": row_values[0],
                "cond": row_values[1],
                "price": _euro_money_to_decimal(row_values[-2]),
                "avail": int(row_values[-1]),
                "marketplace_url": product_url,
            }
        )

    return pd.DataFrame(table_values)


def extract_market_offers(url: str) -> pd.DataFrame:
    """Extract a dataframe of offers on a product page."""
    rows = _get_table_rows(url)

    table_values = []
    for row in rows:
        # list(row.stripped_strings) example:
        # ['207', 'MarinaMagic', 'PO', 'Realmete ex pero marcas en la parte e ariba', '1 avail.', '0,02 €', '0,02 €', '1']
        row_values = list(row.stripped_strings)

        # TODO get rid of magic number: use a helper that filters on conditions perhaps?
        # It's important to ensure this link is correct, we can create a validate row method perhaps.
        user_uri = row.find_all("a")[0]["href"]
        table_values.append(
            {
                "cond": row_values[2],
                "custom_text": row_values[3],
                "price": _euro_money_to_decimal(row_values[-2]),
                "avail": int(row_values[-1]),
                "user_name": row_values[1],
                "user_sales": int(row_values[0]),
                "user_uri": user_uri,
            }
        )

    return pd.DataFrame(table_values)


def _get_table_rows(url):
    """Extract the table rows from a url.
    
    Assumes that table row's match a given html class name.
    """
    res = requests.get(url)
    assert res.status_code == 200, "panic: request failed"

    soup = bs4.BeautifulSoup(res.content, "lxml")

    # Match all rows in the table.
    # We can't use `pd.read_table` unfortunately since the table doesn't use the correct <table>, <th>, <td> encoding
    rows = soup.find_all("div", {"class": "row no-gutters article-row"})
    return rows


def _euro_money_to_decimal(string: str) -> Decimal:
    stripped = sub(r"[^\d,]", "", string)  # "0,20 €" -> "0,20"
    stripped = stripped.replace(",", ".")  # "0,20" -> "0.20"
    return Decimal(stripped)


