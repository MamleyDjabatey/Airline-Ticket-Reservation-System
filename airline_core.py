8# The Core of the Airline Reservation System; airline_core.py 
import csv  # Import the csv module for handling CSV file operations
import random  # Import the random module for generating random numbers
from datetime import datetime  # Import datetime for handling date and time
import os  # Import os module for interacting with the operating system

# Class to represent a booking
class Reservation:
    def __init__(self, passenger_id, ticket_number, seat_number, reservation_time):
        self.passenger_id = passenger_id  # Unique ID for the passenger
        self.ticket_number = ticket_number  # Unique ticket number for the reservation
        self.seat_number = seat_number  # Assigned seat number for the reservation
        self.reservation_time = reservation_time  # Time when the booking was made
        self.cancellation_time = None  # Time when the reservation was cancelled (initially None)

# Class for managing the airline reservation system
class AirlineReservationSystem:
    def __init__(self, csv_file="reservations.csv"):
        self.csv_file = csv_file  # Path to the CSV file storing bookings
        self.reservations = {}  # Dictionary to store bookings with ticket_number as key
        self.seats = set(range(1, 101))  # Set of available seats (1-100)
        self.used_passenger_ids = set()  # Set to track passenger IDs that have been used
        self.load_reservations()  # Load existing bookings from the CSV file

    # Method to generate a unique passenger ID
    def generate_passenger_id(self):
        while True:
            passenger_id = random.randint(100, 999)  # Generate a random passenger ID
            if passenger_id not in self.used_passenger_ids:  # Check if the ID is unique
                self.used_passenger_ids.add(passenger_id)  # Add to used IDs
                return passenger_id  # Return the unique passenger ID

    # Method to generate a unique ticket number based on passenger ID
    def generate_ticket_number(self, passenger_id):
        extension = random.randint(10000, 99999)  # Generate a random extension
        return f"{passenger_id}-{extension}"  # Return formatted ticket number

    # Method to get an available seat at random
    def get_available_seat(self):
        if not self.seats:  # Check if there are no available seats
            return None  # Return None if no seats are available
        return random.choice(list(self.seats))  # Return a random available seat

    # Method to book a ticket
    def reserve_ticket(self):
        if not self.seats:  # Check if there are no seats available
            return None, "No seats available"  # Return error message if no seats are available

        passenger_id = self.generate_passenger_id()  # Generate a new passenger ID
        ticket_number = self.generate_ticket_number(passenger_id)  # Generate a ticket number
        seat_number = self.get_available_seat()  # Get an available seat

        if seat_number is None:  # Check if seat_number is None
            return None, "No seats available"  # Return error if no seat is available

        self.seats.remove(seat_number)  # Remove the reserved seat from available seats
        reservation = Reservation(
            passenger_id=passenger_id,  # Create a new reservation instance
            ticket_number=ticket_number,
            seat_number=seat_number,
            reservation_time=datetime.now()  # Set the current time as reservation time
        )
        self.reservations[ticket_number] = reservation  # Store the reservation in the reservations dictionary
        return reservation, "Booking successful"  # Return the reservation and success message

    # Method to cancel a reserved ticket
    def cancel_ticket(self, ticket_number):
        if ticket_number not in self.reservations:  # Check if the ticket number exists
            return False, "Ticket not found"  # Return error if ticket not found

        reservation = self.reservations[ticket_number]  # Retrieve reservation details
        if reservation.cancellation_time:  # Check if the ticket is already cancelled
            return False, "Ticket already cancelled"  # Return error if already cancelled

        self.seats.add(reservation.seat_number)  # Add the seat back to available seats
        reservation.cancellation_time = datetime.now()  # Set the cancellation time to now
        del self.reservations[ticket_number]  # Remove the reservation from the dictionary
        return True, "Cancellation Successful"  # Return success message

    # Method to retrieve information about a ticket using its ticket number
    def get_ticket_info(self, ticket_number):
        return self.reservations.get(ticket_number)  # Return reservation details if found

    # Method to count how many seats are available
    def get_available_seats_count(self):
        return len(self.seats)  # Return the number of available seats

    # Method to get a list of window seats
    def get_window_seats(self):
        window_seats = []  # List to hold window seats
        for reservation in self.reservations.values():  # Iterate through all reservations
            if reservation.seat_number % 3 == 1:  # Check if seat is a window seat
                window_seats.append((reservation.seat_number, reservation.ticket_number))  # Add to list
        return sorted(window_seats)  # Return sorted list of window seats

    # Method to load existing reservations from the CSV file
    def load_reservations(self):
        if not os.path.exists(self.csv_file):  # Check if the CSV file exists
            return  # Exit if the file does not exist

        try:
            with open(self.csv_file, 'r', newline='') as file:  # Open the CSV file
                reader = csv.DictReader(file)  # Create a CSV reader
                for row in reader:  # Iterate through each row in the CSV
                    reservation = Reservation(
                        passenger_id=int(row['passenger_id']),  # Create a reservation object
                        ticket_number=row['ticket_number'],
                        seat_number=int(row['seat_number']),
                        reservation_time=datetime.fromisoformat(row['reservation_time'])  # Convert time to datetime object
                    )
                    self.reservations[reservation.ticket_number] = reservation  # Store reservation in dictionary
                    self.seats.remove(reservation.seat_number)  # Remove seat from available seats
                    self.used_passenger_ids.add(reservation.passenger_id)  # Add customer ID to used IDs

        except (FileNotFoundError, csv.Error) as e:  # Handle file not found or CSV errors
            print(f"Error loading reservations: {e}")  # Print error message

    # Method to save current reservations to the CSV file
    def save_reservations(self):
        try:
            with open(self.csv_file, 'w', newline='') as file:  # Open the CSV file for writing
                writer = csv.DictWriter(file, fieldnames=[
                    'passenger_id', 'ticket_number', 'seat_number',
                    'reservation_time', 'cancellation_time'  # Define fieldnames for CSV
                ])
                writer.writeheader()  # Write the header row to the CSV
                for reservation in self.reservations.values():  # Iterate through all reservations
                    writer.writerow({
                        'passenger_id': reservation.passenger_id,  # Write reservation details to CSV
                        'ticket_number': reservation.ticket_number,
                        'seat_number': reservation.seat_number,
                        'reservation_time': reservation.reservation_time.isoformat(),  # Convert datetime to ISO format
                        'cancellation_time': reservation.cancellation_time.isoformat() if reservation.cancellation_time else '' }) # Handle optional cancellation time
                    

        except Exception as e:  # Handle any exception during file operation
            print(f"Error saving reservations: {e}")  # Print error message

    # Method to update a reservation with a new seat number
    def update_reservation(self, ticket_number, new_seat_number):
        if ticket_number not in self.reservations:  # Check if the ticket number exists
            return False, "Ticket not found"  # Return error if ticket not found

        if new_seat_number not in self.seats:  # Check if the new seat is available
            return False, "Selected seat is not available"  # Return error if seat is not available

        reservations = self.reservations[ticket_number]  # Retrieve the reservation
        old_seat = reservations.seat_number  # Store the old seat number
        self.seats.add(old_seat)  # Add the old seat back to available seats
        self.seats.remove(new_seat_number)  # Remove the new seat from available seats
        reservations.seat_number = new_seat_number  # Update the reservation with the new seat number
        return True, "Booking updated successfully"  # Return success message