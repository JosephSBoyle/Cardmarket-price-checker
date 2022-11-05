# 1. Get a set of the product urls of all products offered by the user.
# 2. Visit each of these urls and get a list of offers.
#   2.5 (Deferred) filter the offers by:
#   2.5.1 Location
#   2.5.2 Condition
# 3. Compute the difference in price between the user and the lowest value.
# 4. Render this data (possibly sort by difference along the way).

# 1.

import logging
from decimal import Decimal

import pandas as pd

from . import offers

USERNAME = "Extasia1"  # TODO make this configurable
ROOT = "https://www.cardmarket.com/"
USER_OFFERS = "en/Magic/Users/" + USERNAME + "/Offers/Singles"
N = -1
CURRENCY_SYMBOL = "€"
logging.basicConfig(level=logging.INFO)


def get_lowest_market_price(df: pd.DataFrame) -> Decimal:
    """TODO"""
    return df.iloc[0].price


def monify(s) -> str:
    return str(s) + CURRENCY_SYMBOL


###### Start - create a list of user offers ######

user_offers = offers.extract_user_offers(ROOT + USER_OFFERS)
market_offer_dfs = []

for _, offer in list(user_offers.iterrows())[:N]:
    logging.info("collecting marketplace offers for: %s", offer.card_name)

    market_offers = offers.extract_market_offers(ROOT + offer.marketplace_url)
    market_offer_dfs.append(market_offers)

###### Add the difference between the lowest market price matching the criteria and the user's price ######

user_offers["price_delta"] = pd.Series(dtype=object)

for (i, user_offer), market_offers in zip(
    list(user_offers.iterrows())[:N], market_offer_dfs
):
    logging.info("checking user offer vs the market rate for: %s", user_offer.card_name)
    lowest_market_price = get_lowest_market_price(market_offers)

    # Iterrows provides us with a copy - we want to edit the table directly.
    user_offers.loc[i, "price_delta"] = Decimal(user_offer.price - lowest_market_price)

###### Sort the user offers by price delta and render them ######

user_offers.sort_values("price_delta", inplace=True, ascending=False)
print(user_offers.to_string())
