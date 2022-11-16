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
from tqdm import tqdm

from src import filter_, offers
from src.config import ROOT
from datetime import datetime
import sys

DEBUG = False

# TODO refactor
# Use click or something?
if len(sys.argv) >= 2:
    # Load a username
    # python -m src <username>
    USERNAME = sys.argv[1]

    if "-d" in sys.argv:
        DEBUG = True
else:
    USERNAME = "Extasia1"

max_pages = 1 if DEBUG else None

USER_OFFERS = "en/Magic/Users/" + USERNAME + "/Offers/Singles"
logging.info(USERNAME)

###### Start - create a list of user offers ######

user_offers = offers.extract_user_offers(ROOT + USER_OFFERS, max_pages=max_pages)

market_offer_dfs = []


user_offers["marketplace_url_with_filter"] = pd.Series(dtype=object)
for i, offer in tqdm(list(user_offers.iterrows())):
    logging.debug("collecting marketplace offers for: %s", offer.card_name)

    query_suffix = filter_.build_query(
        seller_country="GREAT_BRITAIN",
        min_condition=offer.cond,
        is_foil=offer.is_foil,
    )
    marketplace_url_with_filter = ROOT + offer.marketplace_url + query_suffix
    user_offers.loc[i, "marketplace_url_with_filter"] = marketplace_url_with_filter

    market_offers = offers.extract_market_offers(marketplace_url_with_filter)
    market_offer_dfs.append(market_offers)


###### Add the difference between the lowest market price matching the criteria and the user's price ######

user_offers["price_delta"] = pd.Series(dtype=object)

for (i, user_offer), market_offers in tqdm(
    zip(list(user_offers.iterrows()), market_offer_dfs)
):
    logging.debug(
        "checking user offer vs the market rate for: %s", user_offer.card_name
    )
    # Get the lowest price for the given filtered view
    if market_offers.empty:
        logging.warning(
            "no market offers found for: %s\n url: %s",
            user_offer.card_name,
            user_offer.marketplace_url,
        )
    else:
        lowest_market_price = market_offers.loc[0, "price"]

    # Warning: df.iterrows provides us with a **copy** of the original data.
    # Edit the table directly.
    user_offers.loc[i, "price_delta"] = Decimal(user_offer.price - lowest_market_price)


###### Sort the user offers by price delta and render them ######

# Index the columns and drop the `marketplace_url`.
user_offers = user_offers[
    [
        "card_name",
        "price",
        "cond",
        "is_foil",
        "avail",
        "price_delta",
        "marketplace_url_with_filter",
    ]
]
logging.info(user_offers.to_string())

user_offers["price_delta_over_price"] = (
    user_offers["price_delta"] / user_offers["price"]
)
user_offers.sort_values(by="price_delta_over_price", inplace=True)

user_offers.to_csv(f"./results/{USERNAME}_{datetime.now().isoformat()}.csv")
