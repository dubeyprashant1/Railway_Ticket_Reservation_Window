import tkinter as tk
import datetime
from tkinter import ttk, messagebox
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from register import *
from rail_ticket import *
from datetime import datetime, timedelta
from datetime import date
import mysql.connector
from tkcalendar import DateEntry 

class TicketBookingApp:
    def __init__(self, root, username, date_of_journey, train_class):
        self.root = root
        self.root.title("Railway Ticket Booking")
        self.root.geometry("500x400")
        
        self.date_of_journey = date_of_journey
        self.train_class = train_class

        self.train_name = "Express123"
        self.available_seats = 70  # Updated maximum available seats

        self.label_train_info = tk.Label(root, text="Train: {}".format(self.train_name))
        self.label_train_info.pack(pady=10)

        self.label_seats_available = tk.Label(root, text="Available Seats: {}".format(self.available_seats))
        self.label_seats_available.pack(pady=10)

        self.passenger_entries = []

        self.add_passenger_button = tk.Button(root, text="Add Passenger", command=self.add_passenger_entry)
        self.add_passenger_button.pack(pady=5)

        self.cancel_passenger_button = tk.Button(root, text="Cancel Passenger", command=self.cancel_passenger)
        self.cancel_passenger_button.pack(pady=5)

        self.book_button = tk.Button(root, text="Book Tickets", command=self.book_tickets)
        self.book_button.pack(pady=10)
        self.username=username
        
        self.view_existing_tickets_button = tk.Button(root, text="View Existing Tickets", command=self.view_existing_tickets)
        self.view_existing_tickets_button.pack(pady=10)
        self.available_seats = 70  # Updated maximum available seats
        self.update_available_seats()

    def create_passenger_widgets(self, num_passengers):
        for _ in range(num_passengers):
            frame = tk.Frame(self.root)
            frame.pack(pady=5)

            name_label = tk.Label(frame, text="Name:")
            name_label.pack(side=tk.LEFT)
            name_entry = tk.Entry(frame)
            name_entry.pack(side=tk.LEFT)

            age_label = tk.Label(frame, text="Age:")
            age_label.pack(side=tk.LEFT)
            age_entry = tk.Entry(frame)
            age_entry.pack(side=tk.LEFT)

            sex_label = tk.Label(frame, text="Sex:")
            sex_label.pack(side=tk.LEFT)
            sex_combobox = ttk.Combobox(frame, values=["Male", "Female", "Others"])
            sex_combobox.set("Male")
            sex_combobox.pack(side=tk.LEFT)

            self.passenger_entries.append((name_entry, age_entry, sex_combobox))

    def add_passenger_entry(self):
        self.create_passenger_widgets(1)

    def cancel_passenger(self):
        if self.passenger_entries:
            last_passenger_frame = self.passenger_entries.pop()
            last_passenger_frame[0].destroy()  # Destroy the name entry widget
            last_passenger_frame[1].destroy()  # Destroy the age entry widget
            last_passenger_frame[2].destroy()  # Destroy the sex combobox widget
            self.update_available_seats()

    def book_tickets(self):
        try:
            total_passengers = len(self.passenger_entries)
            if total_passengers > 0:
                selected_seats = total_passengers
                available_seats = self.check_seat_availability(self.date_of_journey, self.train_class, selected_seats)
                if 1 <= selected_seats <= available_seats:
                    self.save_ticket_info(selected_seats)
                    confirmation_message = "Booking successful!\n{} seat(s) booked for {} passengers on {}".format(
                        selected_seats, total_passengers, self.train_name
                    )
                    self.update_available_seats(selected_seats)
                    messagebox.showinfo("Success", confirmation_message)
                else:
                    messagebox.showerror("Error", "Not enough seats available.")
            else:
                messagebox.showerror("Error", "Please add at least one passenger.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers for age.")

    def check_seat_availability(self, date_of_journey, train_class, num_seats):
        conn = mysql.connector.connect(host="localhost", username="root", password="123456", database="passengerregister")
        my_cursor = conn.cursor()

        query = "SELECT available_seats FROM seat_availability WHERE date_of_journey = %s AND train_class = %s"
        values = (date_of_journey, train_class)
        my_cursor.execute(query, values)
        result = my_cursor.fetchone()

        conn.close()

        if result:
            return result[0]  # Return available seats
        else:
            return 0  # If there's no information, consider 0 available seats

    def update_available_seats(self, booked_seats=0):
        self.available_seats -= booked_seats
        self.label_seats_available.config(text="Available Seats: {}".format(self.available_seats))

    def update_available_seats_in_database(self, num_seats):
        conn = None  # Initialize conn with None
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="123456", database="passengerregister")
            my_cursor = conn.cursor()

            # Deduct booked seats from available seats
            update_query = "UPDATE seat_availability SET available_seats = available_seats - %s WHERE date_of_journey = %s AND train_class = %s"
            update_values = (num_seats, self.date_of_journey, self.train_class)
            my_cursor.execute(update_query, update_values)

            conn.commit()
        except mysql.connector.Error as err:
            print("Error updating available seats:", err)
        finally:
            if conn is not None and conn.is_connected():
                conn.close()    
    
    def save_ticket_info(self, num_passengers):
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="123456", database="passengerregister")
            my_cursor = conn.cursor()
            booking_date = date.today()
            query = "INSERT INTO tickets (username, train_name, num_passengers, booking_date, date_of_journey, train_class) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (self.username, self.train_name, num_passengers, booking_date, self.date_of_journey, self.train_class)
            my_cursor.execute(query, values)
            conn.commit()
        except mysql.connector.Error as err:
            print("Error saving ticket information:", err)
        finally:
            if conn.is_connected():
                conn.close()

    def view_existing_tickets(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="123456", database="passengerregister")
        my_cursor = conn.cursor()
        query = "SELECT train_name, num_passengers, booking_date, date_of_journey, train_class FROM tickets WHERE username = %s"
        values = (self.username,)
        my_cursor.execute(query, values)
        tickets = my_cursor.fetchall()
        conn.close()

        if tickets:
            self.show_ticket_table(tickets)
        else:
            messagebox.showinfo("No Upcoming Journeys", "You have no upcoming journeys.")    
    
    def show_ticket_table(self, tickets):
       # Destroy previous table to update with new data
        for row in self.ticket_table.get_children():
            self.ticket_table.delete(row)

        # Create a new table with a scrollbar
        frame = ttk.Frame(self.root)
        frame.place(x=10, y=300)

        ticket_table = ttk.Treeview(frame, columns=("Ticket ID", "Name", "Source", "Destination", "Date"))
        ticket_table.heading("#0", text="Ticket ID")
        ticket_table.heading("#1", text="Name")
        ticket_table.heading("#2", text="Source")
        ticket_table.heading("#3", text="Destination")
        ticket_table.heading("#4", text="Date")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=ticket_table.yview)
        ticket_table.configure(yscrollcommand=vsb.set)

        ticket_table.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        for ticket in tickets:
            ticket_table.insert("", "end", values=ticket)

        # Create Cancel Tickets button
        cancel_button = tk.Button(frame, text="Cancel Tickets", command=lambda: self.cancel_tickets(ticket_table))
        cancel_button.pack(pady=10)
    
    def cancel_tickets(self, ticket_table):
        selected_tickets = []

        # Iterate through the items in the table and check which ones are selected
        for item in ticket_table.get_children():
            if ticket_table.item(item, "values")[0]:  # Check if the checkbox is selected
                selected_tickets.append(ticket_table.item(item, "values"))

        if selected_tickets:
            confirmation = messagebox.askquestion("Confirm Cancel", "Are you sure you want to cancel the selected tickets?")
            if confirmation == "yes":
                for ticket_info in selected_tickets:
                    self.cancel_ticket(ticket_info)
                ticket_table.delete(*ticket_table.get_children())  # Clear the table
                messagebox.showinfo("Cancellation Successful", "Selected tickets have been canceled successfully.")
        else:
            messagebox.showinfo("No Selection", "Please select at least one ticket to cancel.")

    def confirm_cancel_tickets(self, selected_tickets):
        if selected_tickets:
            confirmation = messagebox.askquestion("Confirm Cancel", "Are you sure you want to cancel the selected tickets?")
            if confirmation == "yes":
                for selected_ticket in selected_tickets:
                    ticket_info = selected_ticket.split(", ")
                    train_name = ticket_info[0].split(": ")[1]
                    num_passengers = int(ticket_info[1].split(": ")[1])
                    journey_date = ticket_info[2].split(": ")[1]
                    train_class = ticket_info[3].split(": ")[1]
                    self.cancel_ticket(train_name, num_passengers, journey_date, train_class)
        else:
            messagebox.showinfo("No Selection", "Please select at least one ticket to cancel.")

    def cancel_ticket(self, ticket_info):
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="123456", database="passengerregister")
            my_cursor = conn.cursor()
            query = "DELETE FROM tickets WHERE username = %s AND train_name = %s AND num_passengers = %s AND booking_date = %s AND date_of_journey = %s AND train_class = %s"
            values = (self.username, ticket_info[0], ticket_info[1], ticket_info[2], ticket_info[3], ticket_info[4])
            my_cursor.execute(query, values)
            conn.commit()
            self.update_available_seats_in_database(int(ticket_info[1]), increase=True)
            self.update_available_seats(booked_seats=int(ticket_info[1]))
        except mysql.connector.Error as err:
            print("Error canceling tickets:", err)
        finally:
            if conn.is_connected():
                conn.close()
                
class JourneyInfo:
    def __init__(self, win, username):
        self.win = win
        self.username = username
        self.win.title("Journey Information")

        self.label_date = Label(win, text="Select Date of Journey:")
        self.label_date.pack(pady=5)

        # Use DateEntry instead of ttk.Entry for date selection
        self.entry_date = DateEntry(win, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.entry_date.pack(pady=5)

        self.label_class = Label(win, text="Class of Train:")
        self.label_class.pack(pady=5)
        self.combo_class = ttk.Combobox(win, values=["Sleeper", "1st AC", "2nd AC", "3rd AC"])
        self.combo_class.set("Sleeper")
        self.combo_class.pack(pady=5)

        self.confirm_button = Button(win, text="Confirm", command=lambda: self.confirm_journey(username))
        self.confirm_button.pack(pady=10)

        self.view_existing_tickets_button = Button(win, text="View Existing Tickets", command=self.view_existing_tickets)
        self.view_existing_tickets_button.pack(pady=10)

    def confirm_journey(self, username):
        date_of_journey = self.entry_date.get_date().strftime("%Y-%m-%d")
        train_class = self.combo_class.get()

        # You may want to validate date_of_journey here

        if date_of_journey and train_class:
            self.win.destroy()  # Destroy the current window
            ticket_booking_window = Toplevel()  # Create a new top-level window
            ticket_booking_window.title("Railway Ticket Booking")
            ticket_booking_window.geometry("500x400")
            ticket_booking_app = TicketBookingApp(ticket_booking_window, username, date_of_journey, train_class)
            selected_seats = 1
            # Call the method to update available seats in the database
            ticket_booking_app.update_available_seats_in_database(selected_seats)
          
    def view_existing_tickets(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="123456", database="passengerregister")
        my_cursor = conn.cursor()
        query = "SELECT train_name, num_passengers, booking_date, date_of_journey, train_class FROM tickets WHERE username = %s"
        values = (self.username,)
        my_cursor.execute(query, values)
        tickets = my_cursor.fetchall()
        conn.close()

        if tickets:
            self.show_ticket_table(tickets)
        else:
            messagebox.showinfo("No Upcoming Journeys", "You have no upcoming journeys.")    
    
    def show_ticket_table(self, tickets):
        # Destroy previous table to update with new data
        for row in self.ticket_table.get_children():
            self.ticket_table.delete(row)

        # Create a new table with a scrollbar
        frame = ttk.Frame(self.root)
        frame.place(x=10, y=300)

        ticket_table = ttk.Treeview(frame, columns=("Ticket ID", "Name", "Source", "Destination", "Date"))
        ticket_table.heading("#0", text="Ticket ID")
        ticket_table.heading("#1", text="Name")
        ticket_table.heading("#2", text="Source")
        ticket_table.heading("#3", text="Destination")
        ticket_table.heading("#4", text="Date")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=ticket_table.yview)
        ticket_table.configure(yscrollcommand=vsb.set)

        ticket_table.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        for ticket in tickets:
            ticket_table.insert("", "end", values=ticket)

        # Create Cancel Tickets button
        cancel_button = tk.Button(frame, text="Cancel Tickets", command=lambda: self.cancel_tickets(ticket_table))
        cancel_button.pack(pady=10)
    
    def cancel_tickets(self, ticket_table):
        selected_tickets = []

        # Iterate through the items in the table and check which ones are selected
        for item in ticket_table.get_children():
            if ticket_table.item(item, "values")[0]:  # Check if the checkbox is selected
                selected_tickets.append(ticket_table.item(item, "values"))

        if selected_tickets:
            confirmation = messagebox.askquestion("Confirm Cancel", "Are you sure you want to cancel the selected tickets?")
            if confirmation == "yes":
                for ticket_info in selected_tickets:
                    self.cancel_ticket(ticket_info)
                ticket_table.delete(*ticket_table.get_children())  # Clear the table
                messagebox.showinfo("Cancellation Successful", "Selected tickets have been canceled successfully.")
        else:
            messagebox.showinfo("No Selection", "Please select at least one ticket to cancel.")

    def confirm_cancel_tickets(self, selected_tickets):
        if selected_tickets:
            confirmation = messagebox.askquestion("Confirm Cancel", "Are you sure you want to cancel the selected tickets?")
            if confirmation == "yes":
                for selected_ticket in selected_tickets:
                    ticket_info = selected_ticket.split(", ")
                    train_name = ticket_info[0].split(": ")[1]
                    num_passengers = int(ticket_info[1].split(": ")[1])
                    journey_date = ticket_info[2].split(": ")[1]
                    train_class = ticket_info[3].split(": ")[1]
                    self.cancel_ticket(train_name, num_passengers, journey_date, train_class)
        else:
            messagebox.showinfo("No Selection", "Please select at least one ticket to cancel.")

    def cancel_ticket(self, ticket_info):
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="123456", database="passengerregister")
            my_cursor = conn.cursor()
            query = "DELETE FROM tickets WHERE username = %s AND train_name = %s AND num_passengers = %s AND booking_date = %s AND date_of_journey = %s AND train_class = %s"
            values = (self.username, ticket_info[0], ticket_info[1], ticket_info[2], ticket_info[3], ticket_info[4])
            my_cursor.execute(query, values)
            conn.commit()
            self.update_available_seats_in_database(int(ticket_info[1]), increase=True)
            self.update_available_seats(booked_seats=int(ticket_info[1]))
        except mysql.connector.Error as err:
            print("Error canceling tickets:", err)
        finally:
            if conn.is_connected():
                conn.close()
    
    
if __name__ == "__main__":
    root = tk.Tk()
    # Provide the required arguments for TicketBookingApp
    app = TicketBookingApp(root, "your_username", "2024-01-20", "Sleeper")
    root.mainloop()
