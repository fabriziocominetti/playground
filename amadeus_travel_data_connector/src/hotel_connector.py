import os
import logging
from amadeus import Client, ResponseError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename='./logs/hotel_connector.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

class HotelConnector:
    def __init__(self):
        api_key = os.getenv('AMADEUS_API_KEY')
        api_secret = os.getenv('AMADEUS_API_SECRET')
        if not api_key or not api_secret:
            raise ValueError('Missing Amadeus API credentials in .env file')
        self.amadeus = Client(
            client_id=api_key,
            client_secret=api_secret
        )

    def fetch_hotels(self, city_code, check_in_date, check_out_date, adults=1, max_results=5):
        """
        Fetch hotel offers from Amadeus API.
        :param city_code: IATA code of the city or airport (e.g., 'DEL' for Delhi)
        :param check_in_date: Check-in date in 'YYYY-MM-DD' format
        :param check_out_date: Check-out date in 'YYYY-MM-DD' format
        :param adults: Number of adult guests
        :param max_results: Max number of results to return
        :return: List of hotel offers (dicts)
        """
        try:
            logging.info(f"Fetching hotels: {city_code} {check_in_date} to {check_out_date}")

            # Step 1: Fetch hotels in the city by cityCode
            hotels_by_city = self.amadeus.reference_data.locations.hotels.by_city.get(cityCode=city_code)

            # If no hotels were found
            if not hotels_by_city.data:
                logging.warning(f"No hotels found for city code: {city_code}")
                return []

            # Step 2: Get hotelIds for the first `max_results` hotels
            hotel_ids = [hotel.get('hotelId') for hotel in hotels_by_city.data[:max_results]]
            
            if not hotel_ids:
                logging.warning("No hotel IDs found.")
                return []

            logging.info(f"Found {len(hotel_ids)} hotels.")

            # Step 3: Fetch hotel offers for the specific hotelIds
            hotel_offers = self.amadeus.shopping.hotel_offers_search.get(
                hotelIds=hotel_ids,
                adults=adults,
                checkInDate=check_in_date,
                checkOutDate=check_out_date,
            )

            # If no offers are found
            if not hotel_offers.data:
                logging.warning("No hotel offers found.")
                return []

            # Log the fetched data and return it
            logging.info(f"Fetched {len(hotel_offers.data)} hotel offers")
            return hotel_offers.data

        except ResponseError as error:
            logging.error(f"Amadeus API error: {error}")
            return []

