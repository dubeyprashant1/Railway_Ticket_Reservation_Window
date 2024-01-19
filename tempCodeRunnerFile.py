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