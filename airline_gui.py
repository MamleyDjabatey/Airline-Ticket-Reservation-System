import tkinter as tk  # Import the tkinter module for GUI creation
from tkinter import ttk, messagebox  # Import ttk for themed widgets and messagebox for dialogs
from airline_core import AirlineReservationSystem  # Import the AirlineReservationSystem class

# Class for the Airline Reservation GUI
class AirlineReservationGUI:
    def __init__(self, root):
        self.root = root  # Main application window
        self.root.title("Airline Reservation System")  # Set the window title
        self.system = AirlineReservationSystem()  # Instantiate the airline reservation system
        
        self.setup_gui()  # Set up the GUI components
        self.update_seats_label()  # Update the available seats label initially
        
    # Method to set up the GUI components
    def setup_gui(self):
        main_frame = ttk.Frame(self.root, padding="10")  # Create a frame for main content
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.N, tk.S))  # Place the frame in the grid
        
        # Available seats label
        self.seats_label = ttk.Label(main_frame, text="")  # Label to display available seats
        self.seats_label.grid(row=0, column=0, columnspan=2, pady=5)  # Place label in the grid
        
        # Buttons for various functionalities
        ttk.Button(main_frame, text="Book Ticket", command=self.reserve_ticket).grid(row=1, column=0, pady=5, padx=5)  # Book Ticket button
        ttk.Button(main_frame, text="Cancel Ticket", command=self.show_cancel_dialog).grid(row=1, column=1, pady=5, padx=5)  # Cancel Ticket button
        ttk.Button(main_frame, text="View Ticket Info", command=self.show_ticket_info_dialog).grid(row=2, column=0, pady=5, padx=5)  # View Ticket Info button
        ttk.Button(main_frame, text="Update Booking", command=self.show_update_dialog).grid(row=2, column=1, pady=5, padx=5)  # Update Booking button
        ttk.Button(main_frame, text="View Window Seats", command=self.show_window_seats).grid(row=3, column=0, pady=5, padx=5)  # View Window Seats button
        ttk.Button(main_frame, text="Quit", command=self.quit_application).grid(row=3, column=1, pady=5, padx=5)  # Quit button
    
    # Method to update the available seats label
    def update_seats_label(self):
        self.seats_label.config(text=f"Available seats: {self.system.get_available_seats_count()}")  # Update label with available seats count
        
    # Method to book a ticket and show result message
    def reserve_ticket(self):
        reservation, message = self.system.reserve_ticket()  # Attempt to book a ticket
        if reservation:  # Check if reservation was successful
            messagebox.showinfo("Booking Successful", f"Ticket number: {reservation.ticket_number}\n" f"Seat number: {reservation.seat_number}")  # Show success message
        else:
            messagebox.showerror("Booking Error", message)  # Show error message if reservation failed
        self.update_seats_label()  # Update available seats label after reservation
            
    # Method to show dialog for cancelling a ticket
    def show_cancel_dialog(self):
        dialog = tk.Toplevel(self.root)  # Create a new top-level window for cancellation
        dialog.title("Cancel Ticket")  # Set title for the dialog
        
        ttk.Label(dialog, text="Enter ticket number: ").grid(row=0, column=0, pady=5, padx=5)  # Label for ticket number
        ticket_entry = ttk.Entry(dialog)  # Entry widget for ticket number
        ticket_entry.grid(row=0, column=1, pady=5, padx=5)  # Place entry in the grid
        
        def cancel():  # Inner function to handle cancellation
            ticket_number = ticket_entry.get()  # Get ticket number from entry
            success, message = self.system.cancel_ticket(ticket_number)  # Attempt to cancel the ticket
            messagebox.showinfo("Cancellation Result", message)  # Show result message
            
            if success:  # If cancellation was successful
                self.update_seats_label()  # Update available seats label
                dialog.destroy()  # Close the dialog
                
        ttk.Button(dialog, text="Cancel Ticket", command=cancel).grid(row=1, column=0, columnspan=2, pady=5)  # Button to perform cancellation
                
    # Method to show dialog for viewing ticket information
    def show_ticket_info_dialog(self):
        dialog = tk.Toplevel(self.root)  # Create a new top-level window for ticket information
        dialog.title("View Ticket Information")  # Set title for the dialog
        
        ttk.Label(dialog, text="Enter ticket number: ").grid(row=0, column=0, pady=5, padx=5)  # Label for ticket number
        ticket_entry = ttk.Entry(dialog)  # Entry widget for ticket number
        ticket_entry.grid(row=0, column=1, pady=5, padx=5)  # Place entry in the grid
        
        def view_info():  # Inner function to view ticket information
            ticket_number = ticket_entry.get()  # Get ticket number from entry
            reservation = self.system.get_ticket_info(ticket_number)  # Retrieve booking information
            if reservation:  # Check if reservation exists
                messagebox.showinfo("Ticket Information",
                                    f"Passenger ID: {reservation.passenger_id}\n"
                                    f"Ticket number: {reservation.ticket_number}\n"
                                    f"Seat number: {reservation.seat_number}\n"
                                    f"Reservation time: {reservation.reservation_time}")  # Show ticket information
            else:
                messagebox.showerror("Error", "Ticket not found")  # Show error if ticket is not found
            dialog.destroy()  # Close the dialog
            
        ttk.Button(dialog, text="View Info", command=view_info).grid(row=1, column=0, columnspan=2, pady=5)  # Button to view info
            
    # Method to show dialog for updating a reservation
    def show_update_dialog(self):
        dialog = tk.Toplevel(self.root)  # Create a new top-level window for updating reservation
        dialog.title("Update Booking")  # Set title for the dialog
        
        ttk.Label(dialog, text="Ticket number:").grid(row=0, column=0, pady=5, padx=5)  # Label for ticket number
        ticket_entry = ttk.Entry(dialog)  # Entry widget for ticket number
        ticket_entry.grid(row=0, column=1, pady=5, padx=5)  # Place entry in the grid
        
        ttk.Label(dialog, text="New seat number:").grid(row=1, column=0, pady=5, padx=5)  # Label for new seat number
        seat_entry = ttk.Entry(dialog)  # Entry widget for new seat number
        seat_entry.grid(row=1, column=1, pady=5, padx=5)  # Place entry in the grid
        
        def update():  # Inner function to perform update
            try:
                ticket_number = ticket_entry.get()  # Get ticket number from entry
                new_seat = int(seat_entry.get())  # Get new seat number from entry
                if not 1 <= new_seat <= 100:  # Validate seat number range
                    messagebox.showerror("Error", "Invalid seat number")  # Show error if invalid
                    return  # Exit function if invalid
                success, message = self.system.update_reservation(ticket_number, new_seat)  # Attempt to update booking
                messagebox.showinfo("Update Result", message)  # Show result message
                if success:  # If update was successful
                    self.update_seats_label()  # Update available seats label
                    dialog.destroy()  # Close the dialog
            except ValueError:  # Handle non-integer input
                messagebox.showerror("Error", "Seat number must be a number")  # Show error if input is not a number
                
        ttk.Button(dialog, text="Update Booking", command=update).grid(row=2, column=0, columnspan=2, pady=5)  # Button to perform update

    # Method to show window seat tickets in a message box
    def show_window_seats(self):
        window_seats = self.system.get_window_seats()  # Retrieve list of window seat tickets
        if window_seats:  # Check if there are any window seats booked
            seat_info = "\n".join([f"Seat {seat_num} : Ticket {ticket_num}" for seat_num, ticket_num in window_seats])  # Format seat info
            messagebox.showinfo("Window Seat Tickets", seat_info)  # Show window seat tickets in a message box
        else:
            messagebox.showinfo("Window Seat Tickets", "No window seats are currently booked")  # Inform user if no window seats are booked

    # Method to quit the application
    def quit_application(self):
        self.system.save_reservations()
        self.root.destroy()  # Close the main application window

# Entry point of the application
if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    app = AirlineReservationGUI(root)  # Create an instance of the AirlineReservationGUI
    root.mainloop()  # Start the GUI event loop