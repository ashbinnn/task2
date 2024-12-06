
import os
from datetime import datetime

# Data Storage
room_inventory = {}  # Stores room details
room_bookings = {}  # Stores room allocation details
DATA_FILE = "LHMS_Studentid.txt"

# Ensure the data file exists
if not os.path.exists(DATA_FILE):
    open(DATA_FILE, "w").close()

# Core Hotel Management Functions
def display_main_menu():
    print("\n=== LANGHAM Hotel Management System ===")
    print("1. Register New Room")
    print("2. Remove Room")
    print("3. Show All Room Details")
    print("4. Book a Room")
    print("5. View Room Booking Status")
    print("6. Generate Invoice & Release Room")
    print("7. Save Booking Data to File")
    print("8. Read Bookings from File")
    print("9. Backup Booking File and Clear Data")
    print("0. Exit")


def register_room():
    """Registers a new room in the system."""
    try:
        room_id = input("Enter the room ID: ")
        if not room_id:
            raise ValueError("Room ID cannot be empty.")
        if room_id in room_inventory:
            print(f"Room {room_id} is already registered.")
            return

        category = input("Enter room category (e.g., Standard, Suite): ").strip()
        rate = input("Enter room rate (per night): ").strip()
        rate = float(rate)  # Corrected type casting
        amenities = input("List amenities (separated by commas): ").strip().split(",")

        if not category or rate <= 0:
            raise ValueError("Invalid room category or rate. Please try again.")

        room_inventory[room_id] = {
            "category": category,
            "rate": rate,
            "amenities": [amenity.strip() for amenity in amenities]
        }
        print(f"Room {room_id} successfully registered.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except ZeroDivisionError as zde:
        print(f"Error: Division by zero occurred during rate calculation.")
    except IndexError as ie:
        print(f"Error: List index out of range while processing amenities.")
    except NameError as ne:
        print(f"Error: Variable not defined during room registration.")
    except TypeError as te:
        print(f"Error: Incorrect data type encountered during room rate input.")
    except OverflowError as oe:
        print(f"Error: Calculation exceeded allowable numeric range.")
    except IOError as ioe:
        print(f"File error: Unable to access room data file.")
    except ImportError as ie:
        print(f"Error: A required module is missing.")
    except EOFError as eof:
        print(f"Error: End of file reached unexpectedly during input.")
    except FileNotFoundError as fnf:
        print(f"File error: The data file does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def delete_room():
    """Deletes a room from the system."""
    try:
        room_id = input("Enter the room ID to delete: ")
        if not room_id:
            raise ValueError("Room ID cannot be empty.")
        
        # Logical error fix: Check if room is booked before deleting
        if room_id in room_bookings:
            print(f"Room {room_id} is currently booked and cannot be deleted.")
        elif room_id in room_inventory:
            del room_inventory[room_id]
            print(f"Room {room_id} has been deleted.")
        else:
            print(f"Room {room_id} does not exist.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except KeyError:
        print("Error: Room ID does not exist in the system.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def show_room_details():
    """Displays details of all registered rooms."""
    if not room_inventory:
        print("No rooms have been registered.")
        return

    print("\nRegistered Rooms:")
    for room_id, details in room_inventory.items():
        amenities = ", ".join(details["amenities"])
        print(f"Room ID: {room_id}, Category: {details['category']}, Rate: ${details['rate']}, Amenities: {amenities}")


def book_room():
    """Books a room for a customer."""
    try:
        room_id = input("Enter the room ID to book: ")
        if not room_id:
            raise ValueError("Room ID cannot be empty.")
        if room_id not in room_inventory:
            print(f"Room {room_id} does not exist.")
            return

        if room_id in room_bookings:
            print(f"Room {room_id} is already booked for {room_bookings[room_id]}.")
        else:
            guest_name = input("Enter the guest's name: ").strip()
            if not guest_name:
                raise ValueError("Guest name cannot be empty.")
            room_bookings[room_id] = guest_name
            print(f"Room {room_id} successfully booked for {guest_name}.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def generate_invoice_and_release():
    """Generates the bill for a booking and releases the room."""
    try:
        room_id = input("Enter the room ID to release: ")
        if not room_id:
            raise ValueError("Room ID cannot be empty.")
        
        # Fix: Check if the room is booked before generating invoice
        if room_id not in room_bookings:
            print(f"Room {room_id} is not currently booked.")
            return

        guest_name = room_bookings.pop(room_id)
        room_rate = room_inventory[room_id]["rate"]
        print(f"Invoice for {guest_name}:")
        print(f"Room ID: {room_id}, Total Amount: ${room_rate}")
        print(f"Room {room_id} is now available for booking.")
    except KeyError:
        print("Error: Room details could not be found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# File Handling Functions
def save_bookings_to_file():
    """Saves the current bookings to a file."""
    try:
        if not room_bookings:
            print("No bookings to save.")
            return

        with open(DATA_FILE, "w") as file:
            for room_id, guest_name in room_bookings.items():
                file.write(f"{room_id},{guest_name}\n")
        print(f"Booking data saved to {DATA_FILE}.")
    except FileNotFoundError:
        print("Error: Data file not found. Please ensure the file exists.")
    except IOError as e:
        print(f"File error: {e}")


def backup_and_clear_file():
    """Backs up the booking file and clears its content."""
    try:
        if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
            print(f"No data to backup in {DATA_FILE}.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"Backup_LHMS_{timestamp}.txt"

        with open(DATA_FILE, "r") as original_file, open(backup_file, "w") as backup:
            backup.write(original_file.read())

        open(DATA_FILE, "w").close()  # Clear the original file
        print(f"Data backed up to {backup_file}. Original file cleared.")
    except FileNotFoundError:
        print("Backup failed: Data file not found.")
    except IOError as e:
        print(f"File error: {e}")


# Main Function
def main():
    while True:
        display_main_menu()
        try:
            option = input("Select an option: ").strip()
            if option == "1":
                register_room()
            elif option == "2":
                delete_room()
            elif option == "3":
                show_room_details()
            elif option == "4":
                book_room()
            elif option == "5":
                print("View Room Booking Status - (Not Implemented in this example)")
            elif option == "6":
                generate_invoice_and_release()
            elif option == "7":
                save_bookings_to_file()
            elif option == "9":
                backup_and_clear_file()
            elif option == "0":
                print("Thank you for using LANGHAM Hotel Management System. Goodbye!")
                break
            else:
                print("Invalid selection. Please try again.")
        except (ValueError, SyntaxError, TypeError) as e:
            print(f"Input error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
