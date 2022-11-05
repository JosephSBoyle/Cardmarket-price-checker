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

        is_foil = False
        if row.find("span", {"data-original-title", "Foil"}):
            is_foil = True

        table_values.append(
            {
                "card_name": row_values[0],
                "cond": row_values[1],
                "price": _euro_money_to_decimal(row_values[-2]),
                "is_foil": is_foil,
                "avail": int(row_values[-1]),
                "marketplace_url": product_url,
            }
        )

    return pd.DataFrame(table_values)


# TODO refactor me
def extract_market_offers(url: str) -> pd.DataFrame:
    """Extract a dataframe of offers on a product page."""
    rows = _get_table_rows(url)

    table_values = []
    for row in rows:
        # list(row.stripped_strings) example:
        # ['207', 'MarinaMagic', 'PO', 'Realmete ex pero marcas en la parte e ariba', '1 avail.', '0,02 €', '0,02 €', '1']
        row_values = list(row.stripped_strings)

        cond = (
            row.find("a", {"class": "article-condition"})
            .find("span", {"class": "badge"})
            .text
        )
        user_uri = row.find("a")["href"]

        price_div = row.find("div", {"class": "price-container"})

        # Sometimes there will be a 'PPU' field. For instance if the item is a playset of 4 cards.
        price_per_unit = price_div.find_all("span", {"class": "extra-small"})
        if price_per_unit:
            price = _euro_money_to_decimal(price_per_unit[0].text)
        else:
            price = _euro_money_to_decimal(price_div.text)

        user_name = row.find("span", {"class": "seller-name"}).find("a").text

        # FIXME: custom_text sometimes shows 'N avail.' instead of empty when there is no custom text
        row_info = {
            "cond": cond,
            "custom_text": row_values[3],
            "price": price,
            "avail": int(row_values[-1]),
            "user_name": user_name,
            "user_sales": int(row_values[0]),
            "user_uri": user_uri,
        }
        table_values.append(row_info)

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
