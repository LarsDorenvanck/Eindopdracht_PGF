from geopy.distance import geodesic
from utils import transform_place_to_latlong, get_closest_place

def get_escape_time(start_location, end_location, missile_speed):
    """
    Get the escape time between two locations for a given missile speed.
    
    :param start_location: Starting location (city name or coordinates)
    :param end_location: Ending location (city name or coordinates)
    :param missile_speed: Speed of the missile in km/h
    :return: Escape time in minutes, or None if coordinates couldn't be found
    """
    start_coords = transform_place_to_latlong(start_location)
    print(get_closest_place(start_location))
    end_coords = transform_place_to_latlong(end_location)
    print(get_closest_place(end_location))

    if start_coords is None or end_coords is None:
        return None

    distance = geodesic(start_coords, end_coords).kilometers
    time_minutes = (distance / missile_speed) * 60

    return round(time_minutes, 2)

if __name__ == "__main__":
    start_location = "Amsterdam"
    end_location = "New York City"
    missile_speed = 7000  # km/h, approximate speed of an ICBM

    escape_time = get_escape_time(start_location, end_location, missile_speed)
    if escape_time is not None:
        print(f"Estimated escape time: {escape_time} minutes")
    else:
        print("Could not calculate escape time due to invalid locations.")
