import json
import os

# 1. Setup folder and file paths
DATA_FOLDER = "transport_data"
DRIVERS_FILE = os.path.join(DATA_FOLDER, "drivers.json")
PASSENGERS_FILE = os.path.join(DATA_FOLDER, "passengers.json")

# Create the folder if it does not exist yet
os.makedirs(DATA_FOLDER, exist_ok=True)


# 2. Functions to load and save data
def load_data(filepath):
    """Loads existing list of dictionaries from a JSON file."""
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            return json.load(file)
    return []  # Return an empty list if file doesn't exist yet


def save_data(filepath, data_list):
    """Saves the updated list of dictionaries back to the JSON file."""
    with open(filepath, "w") as file:
        json.dump(data_list, file, indent=4)


# 3. Load existing records into lists when the program starts
drivers = load_data(DRIVERS_FILE)
passengers = load_data(PASSENGERS_FILE)


# 4. Functions to collect user input and append to lists
def add_driver():
    print("\n--- Register New Driver ---")
    name = input("Enter driver's name: ").strip()
    sex = input("Enter driver's sex (M/F): ").strip()
    phone = input("Enter driver's phone number: ").strip()
    car_type = input("Enter car type (e.g., Sedan, SUV, Mini-bus): ").strip()

    driver_info = {
        "name": name,
        "sex": sex,
        "phone": phone,
        "car_type": car_type,
    }

    drivers.append(driver_info)
    save_data(DRIVERS_FILE, drivers)
    print(f"Success! {name} has been added to drivers.")


def add_passenger():
    print("\n--- Register New Passenger ---")
    name = input("Enter passenger's name: ").strip()
    sex = input("Enter passenger's sex (M/F): ").strip()
    phone = input("Enter passenger's phone number: ").strip()

    passenger_info = {"name": name, "sex": sex, "phone": phone}

    passengers.append(passenger_info)
    save_data(PASSENGERS_FILE, passengers)
    print(f"Success! {name} has been added to passengers.")


# 5. Example function showing how to use the lists for calculations/reference
def show_summary():
    print("\n--- System Summary & Statistics ---")
    print(f"Total Registered Drivers: {len(drivers)}")
    print(f"Total Registered Passengers: {len(passengers)}")

    # Example calculation: Count drivers with a specific car type
    suv_count = sum(1 for d in drivers if d["car_type"].lower() == "suv")
    print(f"Number of SUV Drivers: {suv_count}")

    print("\nDriver List:", drivers)
    print("Passenger List:", passengers)


# 6. Main Menu Loop
def main():
    while True:
        print("\n==============================")
        print("  STUDENT TRANSPORT PROJECT")
        print("==============================")
        print("1. Add a Driver")
        print("2. Add a Passenger")
        print("3. View Saved Data & Summary")
        print("4. Exit")

        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            add_driver()
        elif choice == "2":
            add_passenger()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            print("Data saved. Exiting program!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if _name_ == "_main_":
    main()