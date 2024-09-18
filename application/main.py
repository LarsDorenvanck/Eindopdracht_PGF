# Import generic functions
import os
import json
# Import functions from other files
from casualty_calc import casualty_calculator
from get_escape_time import get_escape_time
from utils import convert_keys_to_lowercase
from get_stored_reports import read_stored_reports

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))

# Sets the path to the bombs.json file
BOMBS_FILE_PATH = os.path.join(current_dir, 'bombs.json')
MAX_KT = 100000


def casualty_calculator_menu():
    """
    Displays a menu for the casualty calculator function.
    Prompts user to input:
        placename
        configured bomb from bombs.json || custom amount in 
    subsequently runs the casualty calculator with the provided information
    """
    place_name = input("Enter the place: ")

    # Load bombs from JSON file
    # The JSON file is expected to contain a dictionary where:
    # - Keys are the names of nuclear bombs (strings)
    # - Values are the blast radii of the bombs in kilometers (floats)
    with open(BOMBS_FILE_PATH, 'r') as f:
        nuclear_bombs = json.load(f)
    print("--------------------------------")
    print("Available nuclear bombs:")
    
    for bomb, data in nuclear_bombs.items():
        print(f"{bomb}: {data['kt']} kt, Speed: {data['speed']} km/h")
    print("")    
    print("Alternatively: Enter your own yield in kilotons (kt) (eg. 4000)")
    print("--------------------------------")  
    

    nuclear_bombs = convert_keys_to_lowercase(nuclear_bombs)
    
    bomb_choice = input("Enter the bomb name or a custom amount of TNT equivalent in kiloton (kt): ").lower()

    if bomb_choice in nuclear_bombs:
        kt = nuclear_bombs[bomb_choice]['kt']
    else:
        try:
            kt = float(bomb_choice)
            if kt > MAX_KT:
                print("You have chosen a bomb with a yield of 100000 kt or more.")
                print("This is oversized (beyond reason) and breaks the API request limit.(max 500 places in radius)")
                print("Bomb yield has been set to 100000 kt.")
                print("--------------------------------")
                kt = MAX_KT
        except ValueError:
            print("Invalid input. Please enter a valid bomb name or a number for kt.")
            return
    # Calculate radius for 1st degree burns (in km)
    # Using the formula: R = Y^(1/3) * 1.19
    # This formula gives the radius for 1st degree burns, which includes everyone up to 1st degree burns.
    radius = float((kt ** (1/3)) * 1.19)
    print(f"Calculated radius for up-to 1st degree burns: {radius:.2f} km")
    casualty_calculator(place_name, radius, kt)
    input("Hit ENTER to continue...")
    print("\n" * 10)  # Create 10 new lines in the terminal

def escape_time_calculator_menu():
    """
    Displays a menu for the escape time calculator function.
    
    This function prompts the user to input:
        a launch site
        a destination.
    It then allows the user to choose a configured bomb from bombs.json or enter a custom speed.
    It then runs the function that calculates your minimum escape time
    """
    print("Survival chance calculator")

    place_start = input("Enter the launch site location ('eg. Pyongyang'): ")
    place_destination = input("Enter your destination ('eg. Apeldoorn'): ")

    if not place_start or not place_destination:
        print("Invalid input for one or both locations.")
    else:
        print(f"Starting location: {place_start}")
        print(f"Destination: {place_destination}")

        with open(BOMBS_FILE_PATH, 'r') as f:
            bombs = json.load(f)

        print("Available payloads:")
        for bomb, data in bombs.items():
            print(f"{bomb}: Speed: {data['speed']} km/h")
        bombs = convert_keys_to_lowercase(bombs)

        while True:
            choice = input("Enter the payload name or a custom speed in km/h: ").lower()
            #create list of bomb keys
            bomb_keys = list(bombs.keys())
            #if choice is in bomb keys, use its according speed
            if choice in bomb_keys:
                payload_speed = bombs[choice]['speed']
                break
            #otherwise try the number being input
            try:
                payload_speed = float(choice)
                break
            except ValueError:
                print("Invalid input. Please enter a valid payload name or a number for speed.")

        print(f"Selected payload speed: {payload_speed} km/h")
        escape_time = get_escape_time(place_start, place_destination, payload_speed)
        print(f"You have {escape_time} minutes to get far, far away from there")

    input("Press Enter to continue...")
    print("\n" * 10)  # Create 10 new lines in the terminal

def read_report_menu():
    """
    Displays the menu for reading stored reports.
    
    This function calls the read_stored_reports function to retrieve and display
    the content of stored reports from the casualty_calculator function.
    """
    report_content = read_stored_reports()
    if report_content:
        print(report_content)
    else:
        print("No report was selected or an error occurred.")
    input("Press Enter to continue...")
    print("\n" * 10)  # Create 10 new lines in the terminal

def main_menu():
    """
    Displays the main menu of the Total Destruction Casualty Calculator program.
    
    This function repeatedly displays the main menu options to the user until they choose to exit.
    It calls other functions based on the user's choice, allowing them to access different features of the program.
    """
    while True:
        print("Welcome to total destruction casualty calculator")
        print("What function do you want to use?")
        print("1. Casualty calculator")
        print("2. Escape time calculator")
        print("3. Read stored reports")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            casualty_calculator_menu()
        elif choice == "2":
            escape_time_calculator_menu()
        elif choice == "3":
            read_report_menu()
        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
        
        print()  # Add a blank line for better readability between loops


#Run the program if file is executed
if __name__ == "__main__":
    main_menu()
