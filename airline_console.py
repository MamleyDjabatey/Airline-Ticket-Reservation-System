#The Console of the Airline Reservation System; airline_console.py
from airline_core import AirlineReservationSystem  # Import the AirlineReservationSystem class from airline_core module

# Class for interacting with the user via the console
class ConsoleInterface:
    def __init__(self):
        self.system = AirlineReservationSystem()  # Instantiate the AirlineReservationSystem

    # Method to display the main menu options
    def display_menu(self):
        print("\nAirline Reservation System")  # Display title
        print("1. Book a ticket")  # Option to book a ticket
        print("2. Cancel a ticket")  # Option to cancel a ticket
        print("3. View available seats")  # Option to view available seats
        print("4. Update a booking")  # Option to update a booking
        print("5. View ticket information")  # Option to view ticket information
        print("6. View window seat tickets")  # Option to view window seat tickets
        print("7. Quit")  # Option to quit the application
        print(f"\nAvailable seats: {self.system.get_available_seats_count()}")  # Display current count of available seats
        
    # Method to handle ticket booking
    def book_ticket(self):
        reservation, message = self.system.reserve_ticket()  # Call the book_ticket method from the system
        if reservation:  # Check if booking was successful
            print(f"\n Booking successful!")  # Inform user about successful booking
            print(f"Ticket number: {reservation.ticket_number}")  # Show the ticket number
            print(f"Seat number: {reservation.seat_number}")  # Show the assigned seat number
            print(f"Available seats: {self.system.get_available_seats_count()}")  # Show updated count of available seats
        else:
            print(f"\nError: {message}")  # Display error message if booking failed
            
    # Method to handle ticket cancellation
    def cancel_ticket(self):
        ticket_number = input("\nEnter ticket number to cancel: ")  # Prompt user for ticket number
        success, message = self.system.cancel_ticket(ticket_number)  # Attempt to cancel the ticket
        print(f"\n{message}")  # Display message returned from the cancellation attempt
        if success:  # If cancellation was successful
            print(f"\n{message}")  # Inform user about successful cancellation
            print(f"Available seats: {self.system.get_available_seats_count()}")  # Show updated count of available seats
                
    # Method to view ticket information
    def view_ticket_info(self):
        ticket_number = input("\nEnter ticket number: ")  # Prompt user for ticket number
        reservation = self.system.get_ticket_info(ticket_number)  # Retrieve ticket information
        if reservation:  # Check if booking exists
            print(f"\n Ticket Information: ")  # Display ticket information header
            print(f"passenger ID: {reservation.passenger_id}")  # Show customer ID
            print(f"Ticket number: {reservation.ticket_number}")  # Show ticket number
            print(f"Seat number: {reservation.seat_number}")  # Show seat number
            print(f"Booking time: {reservation.reservation_time}")  # Show booking time
        else:
            print("\nTicket not found")  # Inform user if ticket is not found
            
    # Method to update an existing booking
    def update_reservation(self):
        ticket_number = input("\nEnter ticket number: ")  # Prompt user for ticket number
        try:
            new_seat = int(input("Enter new seat number (1-100): "))  # Prompt for new seat number
            if not 1 <= new_seat <= 100:  # Validate seat number range
                print("\nInvalid seat number. Must be between 1 and 100.")  # Inform user of invalid seat number
                return  # Exit method if invalid
        except ValueError:  # Handle non-integer input
            print("\nInvalid input. Seat must be a number.")  # Inform user of invalid input
            return  # Exit method
        
        success, message = self.system.update_reservation(ticket_number, new_seat)  # Attempt to update booking
        print(f"\n{message}")  # Display result message
        
    # Method to view tickets for window seats
    def view_window_seats(self):
        window_seats = self.system.get_window_seats()  # Retrieve list of window seat tickets
        if window_seats:  # Check if there are any window seats booked
            print("\nWindow Seat Tickets:")  # Display header for window seat tickets
            for seat_num, ticket_num in window_seats:  # Iterate through window seat tickets
                print(f"Seat {seat_num} : Ticket {ticket_num}")  # Display seat and ticket number
        else:
            print("\nNo window seats are currently booked")  # Inform user if no window seats are booked
            
    # Method to run the console interface
    def run(self):
        while True:  # Infinite loop to keep the menu running
            self.display_menu()  # Display the menu
            choice = input("\nEnter your choice (1-7) : ")  # Prompt user for menu choice
            
            if choice == '1':  # If user chooses to book a ticket
                self.book_ticket()
            elif choice == '2':  # If user chooses to cancel a ticket
                self.cancel_ticket()
            elif choice == '3':  # If user chooses to view available seats
                print(f"\nAvailable seats: {self.system.get_available_seats_count()}")  # Display available seats
            elif choice == '4':  # If user chooses to update a booking
                self.update_reservation()
            elif choice == '5':  # If user chooses to view ticket information
                self.view_ticket_info()
            elif choice == '6':  # If user chooses to view window seat tickets
                self.view_window_seats()
            elif choice == '7':  # If user chooses to quit
                self.system.save_reservations()  # Save bookings to CSV
                print("\nThank you for using the Airline Reservation System!")  # Thank user for using the system
                break  # Exit the loop
            else:
                print("\nInvalid Choice. Please try again.")  # Inform user of invalid choice
    
# Main entry point of the program
if __name__ == "__main__":
    console = ConsoleInterface()  # Create an instance of ConsoleInterface
    console.run()  # Run the console interface