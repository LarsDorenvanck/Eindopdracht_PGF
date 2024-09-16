from geopy.distance import geodesic
from utils import transform_place_to_latlong, get_closest_place

def get_escape_time(start_location, end_location, missile_speed):
    """
    Calculate the estimated escape time from a start location to an end location based on the speed of a missile.

    Args:
        start_location (str): The starting location.
        end_location (str): The ending location.
        missile_speed (float): The speed of the missile in kilometers per hour.

    Returns:
        float or None: The estimated escape time in minutes, rounded to two decimal places. Returns None if the locations cannot be converted to coordinates.
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
