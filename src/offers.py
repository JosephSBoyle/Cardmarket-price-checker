"""Module for extracting a user's cardmarket offers based on their unique cardmarket name.

"""
import pandas as pd
import requests
import bs4
from decimal import Decimal
from re import sub


def _euro_string_to_decimal(string: str) -> Decimal:
    stripped = sub(r"[^\d,]", "", string)  # "0,20 €" -> "0,20"
    stripped = stripped.replace(
        ",",
        ".",
    )  # "0,20" -> "0.20"
    return Decimal(stripped)


def extract(user_id: str) -> pd.DataFrame:
    """Extract a dataframe containing each of a user's offers.

    - TODO Add a column linking to the product page with offers for the same item.
    - TODO find the next page link and recursively append to the pandas dataframe.
    """
    url = "https://www.cardmarket.com/en/Magic/Users/" + user_id + "/Offers/Singles"

    res = requests.get(url)
    assert res.status_code == 200, "panic: request failed"
    
    soup = bs4.BeautifulSoup(res.content, "lxml")
    
    # Match all rows in the table.
    # We can't use `pd.read_table` unfortunately since the table doesn't use the correct <table>, <th>, <td> encoding
    rows = soup.find_all("div", {"class": "row no-gutters article-row"})

    table_values = []
    for row in rows:
        # list(row.stripped_strings) example:
        # ['CardName', 'condition (e.g NM | PO | EX ), 'n avail.', '0.20 $', '0.20', '2']
        row_values = list(row.stripped_strings)

        table_values.append(
            {
                "name": row_values[0],
                "cond": row_values[1],
                "price": _euro_string_to_decimal(row_values[-2]),
                "avail": int(row_values[-1]),
            }
        )

    table = pd.DataFrame(table_values, columns=("name", "cond", "price", "avail"))
    table["avail"]
    return table
