import requests

def get_population_count(latitude, longitude, radius):
    """
    Fetch population data for a given location and radius using the GeoNames API.

    Args:
        latitude (float): The latitude of the center point.
        longitude (float): The longitude of the center point.
        radius (int): The radius in kilometers to search for populated places.

    Returns:
        tuple: A tuple containing the total population (int) and a list of geonames data (list).
               Returns 0 if an error occurs.

    Raises:
        requests.RequestException: If there's an error with the API request.
    """
    # GeoNames API endpoint and parameters
    base_url = "http://api.geonames.org/findNearbyPlaceNameJSON"
    params = {
        "lat": latitude,
        "lng": longitude,
        "radius": radius,
        "maxRows": 500,  # Maximum number of FREE results
        "username": "lars_bela",  # Your GeoNames username
        "cities": "cities1000"  # Only cities with population > ####
    }

    try:
        # Make the API request
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            return f"Error fetching population data: Status code {response.status_code}"
        data = response.json()
        
        # Calculate total population and count cities
        geonames = data.get('geonames', [])
        total_population = sum(int(place.get('population', 0)) for place in geonames)
        #cities_count = len(geonames)
        
        #print(f"Population result: {total_population}")
        #print(f"Number of cities found: {cities_count}")
        
        if total_population == 0:
            print("A problem arose:")
            print("1: Over 500 cities were found in the blast radius. Upgrade to premium API access.")
            print("2: Blast radius too small.")
            print("3: 'city' too small, try a different city.")
            print("3: API has freak data, try a different city.")
        
        return total_population, geonames

    except requests.RequestException as e:
        print(f"Error fetching population data: {e}")
        return 0

def main():
    """
    Main function to demonstrate the usage of get_population_count.

    This function sets up example coordinates for Amsterdam and calls the
    get_population_count function to retrieve population data.
    """
    print("Population Count Calculator")
    latitude = 52.3676  # Amsterdam latitude
    longitude = 4.9041  # Amsterdam longitude
    radius = 1000

    population = get_population_count(latitude, longitude, radius)
    
    print(f"Total population within {radius} km radius of Amsterdam: {population}")

if __name__ == "__main__":
    main()
