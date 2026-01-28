import pandas as pd
import logging
from datetime import datetime

def merge_and_clean_data(flights, hotels):
    """
    Merge flight and hotel data, clean, and calculate package price.
    :param flights: List of flight offer dicts
    :param hotels: List of hotel offer dicts
    :return: Cleaned pandas DataFrame
    """
    # Convert to DataFrames
    flights_df = pd.DataFrame(flights)
    hotels_df = pd.DataFrame(hotels)

    # Extract relevant columns and flatten nested structures if needed
    flights_df['flight_price'] = flights_df['price'].apply(lambda x: float(x['total']) if isinstance(x, dict) and 'total' in x else None)
    hotels_df['hotel_price'] = hotels_df['offers'].apply(lambda offers: float(offers[0]['price']['total']) if isinstance(offers, list) and offers and 'price' in offers[0] else None)
    hotels_df['hotel_name'] = hotels_df['hotel'].apply(lambda h: h.get('name') if isinstance(h, dict) else None)

    # Merge: Cartesian product (all combinations)
    merged = flights_df.assign(key=1).merge(hotels_df.assign(key=1), on='key').drop('key', axis=1)

    # Calculate package price
    merged['package_price'] = merged['flight_price'] + merged['hotel_price']

    # Clean: drop rows with missing prices
    merged = merged.dropna(subset=['flight_price', 'hotel_price', 'package_price'])

    # Format dates (example: extract departure date)
    if 'itineraries' in flights_df.columns:
        merged['departure_date'] = merged['itineraries'].apply(
            lambda its: its[0]['segments'][0]['departure']['at'][:10] if isinstance(its, list) and its and 'segments' in its[0] else None
        )
    if 'offers' in hotels_df.columns:
        merged['check_in'] = merged['offers'].apply(
            lambda offers: offers[0]['checkInDate'] if isinstance(offers, list) and offers and 'checkInDate' in offers[0] else None
        )
        merged['check_out'] = merged['offers'].apply(
            lambda offers: offers[0]['checkOutDate'] if isinstance(offers, list) and offers and 'checkOutDate' in offers[0] else None
        )

    # Log the merge
    logging.info(f"Merged {len(flights_df)} flights with {len(hotels_df)} hotels. Result: {len(merged)} packages.")

    return merged.reset_index(drop=True)
