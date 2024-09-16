from geopy.geocoders import Nominatim

def transform_place_to_latlong(place_name):
    """
    Transform a place name to its latitude and longitude coordinates.

    param place_name: A string representing the name of the place
    return: A tuple containing (latitude, longitude) if successful, None otherwise
    """
    geolocator = Nominatim(user_agent="my_app")
    try:
        location = geolocator.geocode(place_name)
        if location:
            #print(location.address)
            return location.latitude, location.longitude
        else:
            return None
    
    except Exception as e:
        print(f"Error fetching location data: {e}")
        return None
    
def get_closest_place(input_location):
    """
    Get the closest place to the input location. (usefull in case of typos/errors during input)

    param input_location: A string representing the input location
    return: A string representing the address of the closest place if successful, None otherwise
    """
    geolocator = Nominatim(user_agent="my_app")
    try:
        location = geolocator.geocode(input_location)
        if location:
            return location.address
        else:
            return None
    except Exception as e:
        print(f"Error fetching location data: {e}")
        return None


def convert_keys_to_lowercase(dictionary):
    """
    Convert all keys in the given dictionary to lowercase. (the make the comparison between bombs.json and input case-insensitive)
    
    :param dictionary: The input dictionary
    :return: A new dictionary with lowercase keys
    """
    return {k.lower(): v for k, v in dictionary.items()}