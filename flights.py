from amadeus import Client, ResponseError
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
client_id = os.getenv("AMADEUS_CLIENT_ID")
client_secret = os.getenv("AMADEUS_CLIENT_SECRET")

# Initialize the Amadeus client
amadeus = Client(
    client_id=client_id,
    client_secret=client_secret
)

# Function to search for flights
def search_flights(origin='SFO', destination='JFK', departure_date='2024-09-15', adults=1, children=0, max_price=None, limit=1):
    try:
        # Call the flight offers search API
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=departure_date,
            adults=adults,
            children=children,
            maxPrice=max_price
        )

        # Check if flight offers are returned
        if response.data:
            flights = response.data
            print(f"Found {len(flights)} flights.")
            print(f"Displaying first {limit} cheapest flight details.")

            # Display flight details
            for idx, flight in enumerate(flights):
                if idx >= limit: break
                print(f"\nFlight {idx + 1}:")
                print(f"Price: {flight['price']['total']} {flight['price']['currency']}")
                for itinerary in flight['itineraries']:
                    print("Itinerary:")
                    for segment in itinerary['segments']:
                        departure = segment['departure']
                        arrival = segment['arrival']
                        print(
                            f"From {departure['iataCode']} at {departure['at']} to {arrival['iataCode']} at {arrival['at']}")

            return flights
        else:
            print("No flights found.")
            return None

    except ResponseError as error:
        print(f"An error occurred during the search: {error}")
        return None


# Function to confirm flight pricing using Flight Offers Price API
def confirm_flight_price(flight_offer):
    try:
        # Call the flight offers price API
        response = amadeus.shopping.flight_offers.pricing.post(flight_offer)

        # Display confirmed price
        if response.data:
            print("Price confirmed:")
            print(f"response: {response.data}")
            confirmed_flight = response.data['flightOffers'][0]
            print(f"Price: {confirmed_flight['price']['total']} {confirmed_flight['price']['currency']}")
        else:
            print("No price confirmation available.")

    except ResponseError as error:
        print(f"An error occurred while confirming the price: {error}")


# Example usage to search for flights and confirm the price
def plan_flight(origin='SFO', destination='JFK', departure_date='2024-09-15', adults=1, children=0, max_price=None):
    flights = search_flights(
        origin,
        destination,
        departure_date,
        adults,
        children,
        max_price
    )

    if flights:
        # Select the first flight offer (you can select based on your criteria)
        selected_flight = flights[0]

        # Confirm pricing for the selected flight offer
        confirm_flight_price(selected_flight)