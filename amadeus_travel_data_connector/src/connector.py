import os
import logging
from amadeus import Client, ResponseError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename='./logs/amadeus_connector.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

class AmadeusConnector:
    def __init__(self):
        api_key = os.getenv('AMADEUS_API_KEY')
        api_secret = os.getenv('AMADEUS_API_SECRET')
        if not api_key or not api_secret:
            raise ValueError('Missing Amadeus API credentials in .env file')
        self.amadeus = Client(
            client_id=api_key,
            client_secret=api_secret
        )

    def fetch_flights(self, origin, destination, departure_date, adults=1, max_results=5):
        """
        Fetch flight offers from Amadeus API.
        :param origin: IATA code of origin airport (e.g., 'FCO')
        :param destination: IATA code of destination airport (e.g., 'TFS')
        :param departure_date: Departure date in 'YYYY-MM-DD' format
        :param adults: Number of adult passengers
        :param max_results: Max number of results to return
        :return: List of flight offers (dicts)
        """
        try:
            logging.info(f"Fetching flights: {origin} -> {destination} on {departure_date}")
            response = self.amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=departure_date,
                adults=adults,
                max=max_results
            )
            return response.data
        except ResponseError as error:
            logging.error(f"Amadeus API error: {error}")
            return []
