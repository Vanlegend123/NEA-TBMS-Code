import requests
from dotenv import load_dotenv
import os
import math
from datetime import datetime
import json
import User_Detail_Processes
    
def priceCalculator(Pickup, Dropoff, CurrentTime):
    # Extracts values from multipliers.json 
    Multipliers = User_Detail_Processes.openFile("multipliers.json")

    Four = Multipliers["1-4 Passenger"] 
    Five = Multipliers["5-6 Passenger"]
    Seven = Multipliers["7-8 Passenger"] 
    Night = Multipliers["Night"]

    # Gets the distance between the two postcodes and handles errors
    try:
        Status, Distance = getDrivingDistance(Pickup, Dropoff)
        if Status == False:
            print(Distance)
            return False
    except Exception as e:
        print(f"Error running getDrivingDistance function: {e}")
        return False
    # Convert to datetime object for easier comparison
    CurrentTime = datetime.strptime(CurrentTime, "%H:%M").time()

    # Check if it's between 22:00 and 06:00
    if CurrentTime >= datetime.strptime("22:00", "%H:%M").time() or CurrentTime < datetime.strptime("06:00", "%H:%M").time():
        Distance = Distance * Night
    
    # Calculates taxi quotes
    FourPrice = round(float(Distance) * float(Four), 2)
    FivePrice = round(float(Distance) * float(Five), 2)
    SevenPrice = round(float(Distance) * float(Seven), 2)
    Values = [FourPrice, FivePrice, SevenPrice]
    # Rounds values for floating-point precision error

    return Values

def getDrivingDistance(postcode1, postcode2):
    # Load environment variables from .env file
    load_dotenv()
    # Access the API key
    API_KEY = os.getenv('API_KEY')
    endpoint = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": postcode1,
        "destinations": postcode2,
        "mode": "driving",
        "key": API_KEY
    }
    
    Response = requests.get(endpoint, params=params)
    
    # Checks if HTTP request to the API was not successful
    if Response.status_code != 200:
        return False, (f"API request failed with status code: {Response.status_code}")
    
    Data = Response.json() # Converts API response from JSON format into a Python Dictionary

    # Checks if the API worked or not
    if Data['status'] != 'OK':
        print("API response error:", Data.get('status'), "-", Data.get('error_message'))
        return False, "API did not work"
    
    try:
        Element = Data['rows'][0]['elements'][0]
        # Checks if the route is possible or not
        if Element['status'] != 'OK':
            print("Route status error:", Element['status'])
            return False, "Route is not possible/drivable"

        DistanceText = Element['distance']['text']
        # Extract numeric value and unit
        DistanceValue, unit = DistanceText.split(' ')
        DistanceValue = float(DistanceValue.replace(',', ''))

        if unit in ['km', 'kilometers']:
            Miles = DistanceValue / 1.609 # Converts from km to miles
        elif unit in ['m', 'meters']:
            Miles = DistanceValue / 1609.34 # Converts from meters to miles
        elif unit in ['ft', 'feet']:
            Miles = DistanceValue / 5280 # Converts from feet to miles
        else:
            Miles = DistanceValue  # Assumes distance as miles if no unit found

        Miles = math.ceil(Miles) # Rounds the distance to next integer mile
        return True, Miles
    # Handles unexpected errors
    except Exception as e:
        print(f"Error parsing response: {e}")
        return False, (f"Error parsing response: {e}")