# 1. Get a set of the product urls of all products offered by the user.
# 2. Visit each of these urls and get a list of offers.
#   2.5 (Deferred) filter the offers by:
#   2.5.1 Location
#   2.5.2 Condition
# 3. Compute the difference in price between the user and the lowest value.
# 4. Render this data (possibly sort by difference along the way).

import logging
from decimal import Decimal

import pandas as pd

from src import offers, filter_
from src.config import ROOT, USER_OFFERS


def get_lowest_market_price(df: pd.DataFrame) -> Decimal:
    """Get the lowest market price

    The dataframe is sorted by default.
    """
    return df.iloc[0].price


###### Start - create a list of user offers ######

user_offers = offers.extract_user_offers(ROOT + USER_OFFERS)
market_offer_dfs = []

for i, offer in list(user_offers.iterrows()):
    logging.info("collecting marketplace offers for: %s", offer.card_name)

    query_suffix = filter_.build_query(
        seller_country="GREAT_BRITAIN",
        min_condition=offer.cond,
        is_foil=offer.is_foil,
    )
    marketplace_url = ROOT + offer.marketplace_url + query_suffix

    market_offers = offers.extract_market_offers(marketplace_url)
    market_offer_dfs.append(market_offers)

###### Add the difference between the lowest market price matching the criteria and the user's price ######

user_offers["price_delta"] = pd.Series(dtype=object)

for (i, user_offer), market_offers in zip(
    list(user_offers.iterrows()), market_offer_dfs
):
    logging.info("checking user offer vs the market rate for: %s", user_offer.card_name)
    # Get the lowest price for the given filtered view
    lowest_market_price = market_offers.iloc[0].price

    # Warning: df.iterrows provides us with a **copy** of the original data.
    # Edit the table directly.
    user_offers.loc[i, "price_delta"] = Decimal(user_offer.price - lowest_market_price)

###### Sort the user offers by price delta and render them ######

user_offers.sort_values("price_delta", inplace=True, ascending=False)

# Convert the URI into a full URL.
user_offers["marketplace_url"] = ROOT + user_offers["marketplace_url"]

print(user_offers.to_string())
