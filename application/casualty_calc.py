from utils import transform_place_to_latlong
from get_population_count import get_population_count
from get_weather_data import calculate_fallout_radius_and_risk, get_weather_and_wind
import os

def casualty_calculator(place_name, radius, kt):
    """
    Calculate and report casualties and effects of a nuclear explosion.

    This function takes a place name, blast radius, and explosion yield in kilotons,
    then calculates various effects including casualties, injuries, and fallout.
    It generates a detailed report and saves it to a file.

    Args:
        place_name (str): The name of the location for the explosion.
        radius (float): The blast radius in kilometers.
        kt (float): The yield of the explosion in kilotons.

    Returns:
        None: This function doesn't return a value, but prints the report
              and saves it to a file.

    Side effects:
        - Prints the casualty report to the console.
        - Saves the report to a text file in the 'reports' directory.
    """
    coordinates = transform_place_to_latlong(place_name)
    if not coordinates:
        print(f"Could not find coordinates for {place_name}")
        return

    latitude, longitude = coordinates
    report = []
    report.append(f"Coordinates for {place_name}: Latitude: {latitude}, Longitude: {longitude}")
    report.append(f"Size of the explosion is {kt} kt")
    report.append("--------------------------------")
    total_victims, _ = get_population_count(latitude, longitude, radius)
    vaporized_victims = int(total_victims * 0.05)  # Assume 5% are vaporized in the blast
    severely_injured = int(total_victims * 0.15)  # Assume 15% are severely injured in the blast
    third_degree_burns = int(total_victims * 0.30)  # Assume 30% have 3rd degree burns
    second_degree_burns = int(total_victims * 0.35)  # Assume 35% have 2nd degree burns
    first_degree_burns = int(total_victims * 0.15)  # Assume 15% have 1st degree burns
    
    report.append(f"Total Population Affected (first 1st degree burns or worse): {total_victims:,}")
    report.append(f"Population Vaporized: {vaporized_victims:,}")
    report.append(f"Severely Injured: {severely_injured:,}")
    report.append(f"3rd Degree Burns: {third_degree_burns:,}")
    report.append(f"2nd Degree Burns: {second_degree_burns:,}")
    report.append(f"1st Degree Burns: {first_degree_burns:,}")
    report.append("--------------------------------")
    weather_description, wind_speed = get_weather_and_wind(latitude, longitude)
    report.append(f"Weather Description: {weather_description}")
    report.append(f"Wind Speed: {wind_speed} m/s")
    
    fallout_radius, risk_percentage = calculate_fallout_radius_and_risk(wind_speed, radius, weather_description)
    report.append(f"Calculated Fallout Radius: {fallout_radius:.2f} km")
    report.append(f"Calculated Risk Percentage: {risk_percentage:.2f}%")

    total_affected_population, _ = get_population_count(latitude, longitude, fallout_radius)
    fallout_potential_victims = total_affected_population - vaporized_victims
    report.append(f"Day 1: Fallout Potential Victims (leftover from vaporized): {fallout_potential_victims:,}")

    fallout_actual_victims = int(fallout_potential_victims * risk_percentage / 100)
    report.append(f"Day 1: Fallout Actual Victims (risk percentage applied based on weather): {fallout_actual_victims:,}")
    report.append("--------------------------------")
    total_casualties = vaporized_victims + fallout_actual_victims + severely_injured + third_degree_burns + second_degree_burns + first_degree_burns
    report.append(f"Total Estimated Casualties: {total_casualties:,}")
    report.append("--------------------------------")

    # Print the report
    for line in report:
        print(line)

    # Save the report to a file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = f"casualty_report_{place_name.replace(' ', '_')}.txt"
    reports_dir = os.path.join(current_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    file_path = os.path.join(reports_dir, file_name)
    
    with open(file_path, 'w') as f:
        for line in report:
            f.write(line + '\n')
    
    print(f"Report saved to: {file_path}")

if __name__ == "__main__":
    place_name = "Amsterdam"
    radius = 10
    kt = 10000
    casualty_calculator(place_name, radius, kt)
