from src.connector import AmadeusConnector
from src.hotel_connector import HotelConnector
from src.data_merger import merge_and_clean_data
from src.report import generate_summary_report
import pandas as pd

# Example parameters
ORIGIN = 'LON'  # London
DESTINATION = 'PAR'  # Paris
DEPARTURE_DATE = '2026-01-29'
CHECK_IN_DATE = '2026-01-29'
CHECK_OUT_DATE = '2026-01-31'
ADULTS = 1
MAX_RESULTS = 5

if __name__ == "__main__":
    # Fetch flights
    flight_connector = AmadeusConnector()
    flights = flight_connector.fetch_flights(
        origin=ORIGIN,
        destination=DESTINATION,
        departure_date=DEPARTURE_DATE,
        adults=ADULTS,
        max_results=MAX_RESULTS
    )
    print(f"Fetched {len(flights)} flights.")

    # Fetch hotels
    hotel_connector = HotelConnector()
    hotels = hotel_connector.fetch_hotels(
        city_code=DESTINATION,
        check_in_date=CHECK_IN_DATE,
        check_out_date=CHECK_OUT_DATE,
        adults=ADULTS,
        max_results=MAX_RESULTS
    )
    print(f"Fetched {len(hotels)} hotels.")

    # Merge and clean data
    merged_df = merge_and_clean_data(flights, hotels)
    print(f"Merged into {len(merged_df)} package combinations.")

    # Generate summary report
    summary_df = generate_summary_report(merged_df)
    print("\nSummary Report:")
    print(summary_df.to_string(index=False))
