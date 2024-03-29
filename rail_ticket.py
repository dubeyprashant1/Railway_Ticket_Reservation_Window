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

class JourneyInfo:
    def __init__(self, win, username):
        self.win = win
        self.win.title("Journey Information")
        self.win.geometry("1550x800+0+0")
        self.win.configure(bg="black")
        self.username = username
        self.select_all_counter = 0
        
        self.journey_info_heading = Label(self.win, text="Journey Information",font=("times new roman",35,"bold"),fg="blue",highlightbackground="green",highlightthickness=4)
        self.journey_info_heading.place(x=455, y=40)

        self.label_date = Label(win, text="Select Date of Journey:",font="verdana 15 bold",bg="black",fg="white")
        self.label_date.place(x=180,y=120)
        self.entry_date = DateEntry(win, width=12, background='darkblue', foreground='white', borderwidth=2,font="verdana 10 bold")
        self.entry_date.place(x=920,y=130,width=170)
        
        self.label_train_name = Label(win, text="Name of Train:",font="verdana 15 bold",bg="black",fg="white")
        self.label_train_name.place(x=180,y=165)
        self.combo_train_name = ttk.Combobox(win, values=["Select Train","Humsafar Express", "Prayagraj Express", "Duranto Express", "Vande-Bharat Express","Rajdhani Express",
                                                          "Purushottam Express","Sampark-Kranti Express","North-East Express","Telangana Express","KSR Bengaluru Rajdhani","Jhelum Express",
                                                          "Paschim express","Malwa Express","Jammu-Tawi Express","Geeta-Jayanti Express","Mahabodhi Express","Gorakhdham Express",
                                                          "Kerala Express","Magadh Express","NandanKanan Express","ANVT Superfast","ShivGanga Express","Ganga-Tapti Express","Goa Express",
                                                          "Karnataka Express","SVDK Express","Delhi SF Express","Kalka Mail","Brahmaputra Mail","Himalaya-Queen Express","Shatabdi Express",
                                                          "Rani-kamalaPati Express","Silcher Express","Bhrigu SF Express","Rewa SF express","Sampoorna-Kranti Express","Tamil-Nadu Express",
                                                          "GareebRath Express","Lichhavi Express","Mahananda Express","Unchahhar Express"],state="readonly",font="verdana 10 bold")
        self.combo_train_name.set("Select Train")
        self.combo_train_name.place(x=920,y=170,width=170)

        self.label_class = Label(win, text="Class of Train:",font="verdana 15 bold",bg="black",fg="white")
        self.label_class.place(x=180,y=210)
        self.combo_class = ttk.Combobox(win, values=["Select Class","Chair-Car(CC)","Sleeper(SL)", "3rd AC(3A)", "2nd AC(2A)", "1st AC(1A)"],state="readonly",font="verdana 10 bold")
        self.combo_class.set("Select Class")
        self.combo_class.place(x=920,y=215,width=170)
        
        self.view_existing_tickets_button = Button(win, text="Already Booked", command=self.view_existing_tickets,cursor="hand2",bd=3,relief=RIDGE, font="verdana 15 bold",fg="white",bg="blue", activeforeground="white", activebackground="blue")
        self.view_existing_tickets_button.place(x=150,y=315,width=200,height=35)
        
        self.confirm_button = Button(win, text="Confirm", command=lambda: self.confirm_journey(username),cursor="hand2",bd=3,relief=RIDGE, font="verdana 15 bold",fg="white",bg="green",activeforeground="white",activebackground="green")
        self.confirm_button.place(x=640,y=255,width=120,height=35)

        self.bck_button0= Button(win, text="Log Out", command=lambda:self.back(win),cursor="hand2",bd=3,relief=RIDGE, font="verdana 15 bold",fg="white",bg="purple",activeforeground="white",activebackground="purple")
        self.bck_button0.place(x=1040,y=315,width=120,height=35)
        
        self.delete_acc_btn= Button(win, text="Delete Account", command=lambda:self.delete_acc(win),cursor="hand2",bd=3,relief=RIDGE, font="verdana 15 bold",fg="black",bg="white",activeforeground="black",activebackground="white")
        self.delete_acc_btn.place(x=1000,y=620,width=200,height=35)
            
    def delete_acc(self, win):
        password_confirm = simpledialog.askstring("Password Confirmation", "Please re-enter your password for confirmation:", show='*')
        if password_confirm is None:
            return

        if self.check_password(password_confirm):
            conn=None
            try:
                confirmation = messagebox.askquestion("Delete Account", "Are you sure you want to delete your account?", icon='warning',parent=self.win)
                if confirmation == "yes":
                    conn = mysql.connector.connect(host="localhost", username="root", password="123456", database="passengerregister")
                    my_cursor = conn.cursor()
                    delete_user_query = "DELETE FROM register WHERE email = %s"
                    delete_user_values = (x.get(),)
                    my_cursor.execute(delete_user_query, delete_user_values)
                    conn.commit()
                    y.delete(0, 'end')
                    x.delete(0, 'end')
                    win.destroy()
            except mysql.connector.Error as err:
                print("Error deleting user account:", err)
            finally:
                if conn.is_connected():
                    conn.close()
        else:
            messagebox.showerror("Password Mismatch", "Incorrect password. Please enter the correct password.",parent=self.win)
    
    def check_password(self, entered_password):
        stored_password = y.get()
        return entered_password == stored_password
        
    def back(self,win):
        confirmation = messagebox.askquestion("LogOut Account", "Are you sure you want to Log-Out from your account?", icon='warning',parent=self.win)
        if confirmation == "yes":
            y.delete(0, 'end')
            x.delete(0, 'end')
            win.destroy()
        
    def confirm_journey(self, username):
        date_of_journey = self.entry_date.get_date().strftime("%Y-%m-%d")
        train_class = self.combo_class.get()
        train_name=self.combo_train_name.get()
        global a,b,c
        a=self.entry_date
        b=self.combo_class
        c=self.combo_train_name
        today = datetime.now().date()
        selected_date = datetime.strptime(date_of_journey, "%Y-%m-%d").date()
        if selected_date < today:
            messagebox.showwarning("Invalid Date", "Please select a future date for your journey.", parent=self.win)
            return
        if train_name=="Select Train":
            messagebox.showwarning("Invalid Train", "Please select any Train for your journey.", parent=self.win)
            return
        if train_class=="Select Class":
            messagebox.showwarning("Invalid Class", "Please select any Class of Train for your journey.", parent=self.win)
            return
        elif date_of_journey and train_class:
            ticket_booking_window = Toplevel() 
            ticket_booking_window.title("Railway Ticket Booking")
            ticket_booking_window.geometry("500x400")
            ticket_booking_app = TicketBookingApp(ticket_booking_window, username, date_of_journey, train_name, train_class)
          
    def view_existing_tickets(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="123456", database="passengerregister")
        my_cursor = conn.cursor()
        query = "SELECT id,train_name, num_passengers, date_of_journey, train_class FROM tickets WHERE username = %s"
        values = (self.username,)
        my_cursor.execute(query, values)
        tickets = my_cursor.fetchall()
        conn.close()
        if tickets:
            self.show_ticket_table(tickets)
        else:
            messagebox.showinfo("No Upcoming Journeys", "You have no upcoming journeys.",parent=self.win)

    def show_ticket_table(self, tickets):
        frame = ttk.Frame(self.win, border="4px solid")
        frame.place(x=2, y=370)

        style = ttk.Style()
        style.configure("Red.Treeview", background="yellow", foreground="black", font=("verdana", 10,"bold"), bordercolor="blue")
        style.configure("Red.Treeview.Heading", background="green", foreground="black", font=("verdana", 10, "bold"))

        style.configure("selected.Treeview", background="green", foreground="white", font=("verdana", 10, "bold"))
        style.configure("unselected.Treeview", background="yellow", foreground="black", font=("verdana", 10,"bold"))

        ticket_table = ttk.Treeview(frame, columns=("Select", "Ticket ID", "TrainName", "No. of Passengers", "JourneyDate", "Class"), style="Red.Treeview")
        ticket_table.heading("#0", text="Select", anchor=tk.S)
        ticket_table.heading("#1", text="Ticket ID", anchor=tk.S)
        ticket_table.heading("#2", text="TrainName", anchor=tk.S)
        ticket_table.heading("#3", text="No. of Passengers", anchor=tk.S)
        ticket_table.heading("#4", text="JourneyDate", anchor=tk.S)
        ticket_table.heading("#5", text="Class", anchor=tk.S)

        vsb = ttk.Scrollbar(frame, orient="vertical", command=ticket_table.yview)
        ticket_table.configure(yscrollcommand=vsb.set)

        ticket_table.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        def toggle_select(item):
            current_value = ticket_table.item(item, "values")[0]
            new_value = 1 - int(current_value)
            ticket_table.item(item, values=(new_value, *ticket_table.item(item, "values")[1:]))
            update_background_color(item)

        def update_background_color(item):
            current_value = ticket_table.item(item, "values")[0]
            tag = "selected" if current_value == "1" else "unselected"
            ticket_table.tag_configure(tag, background=style.lookup("{}.Treeview".format(tag), 'background'),foreground=style.lookup("{}.Treeview".format(tag), 'foreground'),font=style.lookup("{}.Treeview".format(tag), 'font'))
            ticket_table.item(item, tags=(tag,))

        def on_item_click(event):
            item = ticket_table.selection()[0]      
            toggle_select(item)

        for ticket in tickets:
            ticket_table.insert("", "end", values=("0", *ticket))

        ticket_table.bind("<ButtonRelease-1>", on_item_click)
        
        show_tkt_btn = Button(self.win, text="Show Ticket", command=lambda: self.show_ticket(ticket_table),cursor="hand2",bd=3,relief=RIDGE, font="verdana 15 bold",fg="white",bg="grey", activeforeground="white", activebackground="grey")
        show_tkt_btn.place(x=600,y=315,width=200,height=35)

        select_all_button = tk.Button(self.win, text="Select All", command=lambda: self.select_all(ticket_table,update_background_color), cursor="hand2",bd=3, relief=RIDGE, font="verdana 15 bold", fg="black", bg="aqua",activeforeground="Black", activebackground="aqua")
        select_all_button.place(x=150, y=620, width=200, height=35)

        cancel_button = tk.Button(self.win, text="Cancel Tickets", command=lambda: self.cancel_tickets(ticket_table),cursor="hand2", bd=3, relief=RIDGE, font="verdana 15 bold", fg="white", bg="red",activeforeground="white", activebackground="red")
        cancel_button.place(x=600, y=620, width=200, height=35)
    
    def show_ticket(self,ticket_table):
        one_ticket=[]
        for item in ticket_table.get_children():
            if ticket_table.item(item, "values")[0]=="1":
                one_ticket.append(ticket_table.item(item, "values")[1:])
        
        if len(one_ticket)==0:
            messagebox.showwarning("Invalid Selection", "Please select any one ticket for viewing.", parent=self.win)
        elif len(one_ticket)==1:
            confirm_mess="\t\t  INDIAN RAILWAYS\n\t\t      (Ticket Slip)\nTrain Name\t :-{}\nDate of Journey      :-{}\nClass of Train\t :-{}\n{} Berths was Booked on {}\n\n\t\tPassenger Details\n{}\nRs.{} amount is Booking Cost\nRs.15.71 amount is Booking Charges\nRs.{} is the Total Charged Amount for the Booking\n\n\n\nPlease take a Screenshot of the same for your Journey*".format(
                str(one_ticket[0][1]),str(one_ticket[0][3]),str(one_ticket[0][4]),str(one_ticket[0][2]),str(self.find_booking_date(one_ticket)),str(self.ticket_slip(one_ticket)),str(self.find_amt(one_ticket)),str((self.find_amt(one_ticket)+15.71)))
            messagebox.showinfo("Ticket Slip",confirm_mess ,parent=self.win)
        else:
            messagebox.showwarning("Invalid Selection", "Please select only One ticket at a time for viewing.", parent=self.win)
    
    def ticket_slip(self,one_ticket):
        all_info=[]
        conn = mysql.connector.connect(host="localhost", username="root", password="123456", database="passengerregister")
        my_cursor = conn.cursor()
        current_seats_query = "SELECT name,age,sex FROM passenger_info WHERE id = %s"
        current_seats_values = (one_ticket[0][0])
        my_cursor.execute(current_seats_query, (current_seats_values,))
        all_info = my_cursor.fetchall()
        s=""
        i=1
        for item in all_info:
            s+=(str(i)+".  "+str(item[0])+"------"+str(item[1])+"------"+str(item[2])+"\n")
            i+=1
        conn.commit
        conn.close()
        return s             
        
    def find_booking_date(self,one_ticket):
        conn = mysql.connector.connect(host="localhost", username="root", password="123456", database="passengerregister")
        my_cursor = conn.cursor()
        current_seats_query = "SELECT booking_date FROM tickets WHERE id = %s"
        current_seats_values = (one_ticket[0][0])
        my_cursor.execute(current_seats_query, (current_seats_values,))
        bookdate = my_cursor.fetchone()[0]
        conn.commit
        conn.close()
        return bookdate
    
    def find_amt(self,one_ticket):
        p=int(one_ticket[0][2])
        q=str(one_ticket[0][4])
        if q=="Chair-Car(CC)":
            return 210*p
        if q=="Sleeper(SL)":
            return 430*p
        if q=="1st AC(1A)":
            return 2780*p
        if q=="2nd AC(2A)":
            return 1860*p
        else:
            return 870*p
            
    def select_all(self, ticket_table,update_background_color):
        self.select_all_counter += 1

        new_value = 1 if self.select_all_counter % 2 != 0 else 0
        for item in ticket_table.get_children():
            ticket_table.item(item, values=(new_value, *ticket_table.item(item, "values")[1:]))
            update_background_color(item)

    def cancel_tickets(self, ticket_table):
        selected_tickets = []
        for item in ticket_table.get_children():
            if ticket_table.item(item, "values")[0]=="1":
                selected_tickets.append(ticket_table.item(item, "values")[1:])

        if selected_tickets:
            confirmation = messagebox.askquestion("Confirm Cancel", "Are you sure you want to cancel the selected tickets?",parent=self.win)
            if confirmation == "yes":
                for ticket_info in selected_tickets:
                    self.cancel_ticket(ticket_info, ticket_table)
                for item in ticket_table.get_children():
                    if ticket_table.item(item, "values")[1:] in selected_tickets:
                        ticket_table.delete(item)
                confirm_message="Selected Seats have been Canceled Successfully.\nRs.{} amount has been Refunded to your Bank Account afte deducting 20% of Booking Cost.\nYou may Expect Your Refund within 7 Business Days.".format(self.calculate_refund(selected_tickets))
                messagebox.showinfo("Cancellation Successful",confirm_message ,parent=self.win)
        else:
            messagebox.showinfo("No Selection", "Please select at least one ticket to cancel.",parent=self.win)

    def calculate_refund(self,selected_seats):
        clas=[]
        numb=[]
        sum=0
        for kt in selected_seats:
            clas.append(kt[4])
            numb.append(kt[2])
        for j in range(len(clas)):
            if(clas[j]=="Chair-Car(CC)"):
                sum+=int((168*int(numb[j])))
            elif(clas[j]=="Sleeper(SL)"):
                sum+=int((344*int(numb[j])))
            elif(clas[j]=="1st AC(1A)"):
                sum+=int((2224*int(numb[j])))
            elif(clas[j]=="2nd AC(2A)"):
                sum+=int((1488*int(numb[j])))
            else:
                sum+=int((696*int(numb[j])))
        return sum

    def cancel_ticket(self, ticket_info, ticket_table):
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="123456", database="passengerregister")
            my_cursor = conn.cursor()
            current_seats_query = "SELECT available_seats FROM seat_availability WHERE date_of_journey = %s AND train_class = %s"
            current_seats_values = (ticket_info[3], ticket_info[4])
            my_cursor.execute(current_seats_query, current_seats_values)
            current_seats = my_cursor.fetchone()[0]
            updated_seats = current_seats + int(ticket_info[2])

            update_seats_query = "UPDATE seat_availability SET available_seats = %s WHERE date_of_journey = %s AND train_class = %s"
            update_seats_values = (updated_seats, ticket_info[3], ticket_info[4])
            my_cursor.execute(update_seats_query, update_seats_values)

            delete_ticket_query = "DELETE FROM tickets WHERE username = %s AND id = %s AND train_name = %s AND num_passengers = %s AND date_of_journey = %s AND train_class = %s"
            delete_ticket_values = (self.username, *ticket_info)
            my_cursor.execute(delete_ticket_query, delete_ticket_values)
            
            delete_passenger_query = "DELETE FROM passenger_info WHERE id = %s"
            delete_passenger_values = (ticket_info[0],)
            my_cursor.execute(delete_passenger_query,(delete_passenger_values))
            conn.commit()
        except mysql.connector.Error as err:
            print("Error canceling tickets:", err)
        finally:
            if conn.is_connected():
                conn.close()           
        
class TicketBookingApp:
    def __init__(self, root, username, date_of_journey,train_name, train_class):
        self.root = root
        self.root.title("Railway Ticket Booking")
        self.root.geometry("1550x800+0+0")
        self.root.configure(bg="black")
        
        self.date_of_journey = date_of_journey
        self.train_class = train_class
        self.username =username
        self.train_name = train_name
        self.available_seats = self.fetch_available_seats()

        self.label_train_info = tk.Label(root, text=self.train_name,font=("times new roman",35,"bold"),fg="red",highlightbackground="blue",highlightthickness=4)
        self.label_train_info.place(x=100, y=45)

        self.label_seats_available = tk.Label(root, text="Available Seats :    {}".format(self.available_seats),font="verdana 15 bold",bg="black",fg="white")
        self.label_seats_available.place(x=900,y=40)
        self.label_selected_date = tk.Label(root, text="Selected Date   :    {}".format(self.date_of_journey),font="verdana 15 bold",bg="black",fg="white")
        self.label_selected_date.place(x=900,y=65)
        self.label_train_class = tk.Label(root, text="Selected Class  :    {}".format(self.train_class),font="verdana 15 bold",bg="black",fg="white")
        self.label_train_class.place(x=900,y=90)

        self.passenger_entries = []

        self.add_passenger_button = tk.Button(root, text="Add Passenger",cursor="hand2", command=self.add_passenger_entry,bd=3,relief=RIDGE, font="verdana 15 bold",fg="white",bg="blue",activeforeground="white",activebackground="blue")
        self.add_passenger_button.place(x=300,y=170,width=200,height=35)

        self.cancel_passenger_button = tk.Button(root, text="Cancel Passenger",cursor="hand2", command=self.cancel_passenger,bd=3,relief=RIDGE, font="verdana 15 bold",fg="white",bg="red",activeforeground="white",activebackground="red")
        self.cancel_passenger_button.place(x=900,y=170,width=200,height=35)

        self.book_button = tk.Button(root, text="Book Tickets", command=self.book_tickets,cursor="hand2",bd=3,relief=RIDGE, font="verdana 15 bold",fg="white",bg="green",activeforeground="white",activebackground="green")
        self.book_button.place(x=300,y=220,width=200,height=35)
        
        self.bck_button1= Button(root, text="Go Back", command=lambda:self.back(root),cursor="hand2",bd=3,relief=RIDGE, font="verdana 15 bold",fg="white",bg="purple",activeforeground="white",activebackground="purple")
        self.bck_button1.place(x=900,y=220,width=200,height=35)
        self.username=username
        
    def back(self,root):
        a.set_date(datetime.now().date())
        b.set("Select Class")
        c.set("Select Train")
        root.destroy()

    def fetch_available_seats(self):
        conn = None
        available_seats = 70  

        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="123456", database="passengerregister")
            my_cursor = conn.cursor()

            check_query = "SELECT available_seats FROM seat_availability WHERE (date_of_journey = %s AND train_class = %s AND train_name = %s)"
            check_values = (self.date_of_journey, self.train_class,self.train_name)
            my_cursor.execute(check_query, check_values)
            existing_record = my_cursor.fetchone()

            if existing_record:
                available_seats = existing_record[0]

        except mysql.connector.Error as err:
            print("Error fetching available seats:", err)
        finally:
            if conn is not None and conn.is_connected():
                conn.close()

        return available_seats

    def create_passenger_widgets(self, num_passengers):
        if len(self.passenger_entries)>=10:
            messagebox.showwarning("No more Passenger","Book atmost 10 seats at a time",parent=self.root)
            return
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        name_label = tk.Label(frame, text="Name:",font="verdana 15",bg="black",fg="white")
        name_label.pack(side=tk.LEFT)
        name_entry = tk.Entry(frame)
        name_entry.pack(side=tk.LEFT)

        age_label = tk.Label(frame, text="Age:",font="verdana 15",bg="black",fg="white")
        age_label.pack(side=tk.LEFT)
        age_entry = tk.Entry(frame)
        age_entry.pack(side=tk.LEFT)

        sex_label = tk.Label(frame, text="Sex:",font="verdana 15",bg="black",fg="white")
        sex_label.pack(side=tk.LEFT)
        sex_combobox = ttk.Combobox(frame, values=["Select","Male", "Female", "Others"],state="readonly")
        sex_combobox.set("Select")
        sex_combobox.pack(side=tk.LEFT)
        
        y_offset = 290 if len(self.passenger_entries) == 0 else 10
        frame.pack(pady=(y_offset, 0))
        self.passenger_entries.append((frame,name_entry, age_entry, sex_combobox))

    def add_passenger_entry(self):
        self.create_passenger_widgets(1)

    def cancel_passenger(self):
        if not self.passenger_entries:
            messagebox.showinfo("No Passengers", "There are no passengers to cancel.", parent=self.root)
            return
        last_passenger_frame = self.passenger_entries.pop()
        for widget in last_passenger_frame:
            widget.destroy()
        if not self.passenger_entries:
            messagebox.showinfo("No Passengers", "All passengers have been canceled.", parent=self.root)

    def book_tickets(self):
        try:
            total_passengers = len(self.passenger_entries)
            if total_passengers > 0:
                valid_entries = all(self.validate_passenger_entry(entry) for entry in self.passenger_entries)
                if valid_entries:
                    selected_seats = total_passengers
                    available_seats = self.check_seat_availability()
                    if 1 <= selected_seats <= available_seats:
                        password_confirm = simpledialog.askstring("Payment Confirmation", "Please re-enter your password to continue:", show='*')
                        if password_confirm is None:
                            return
                        if self.check_password(password_confirm):
                            confirmation = messagebox.askquestion("Final Confirmation", "Are you sure that all info of the passengers are correct?", icon='warning',parent=self.root)
                            if confirmation == "yes":
                                self.save_ticket_info(selected_seats)
                                self.save_passengers()
                                self.update_available_seats_in_database(selected_seats)
                                confirmation_message = "Booking successful!\n{} seat(s) booked for {} passengers on {}.\nRs.{} amount has been charged for this Booking".format(selected_seats, total_passengers, self.train_name,self.calculate_fare(selected_seats))
                                self.update_available_seats(selected_seats)
                                messagebox.showinfo("Success", confirmation_message, parent=self.root)
                                self.back(self.root)
                            else:
                                return
                        else:
                            messagebox.showerror("Password Mismatch", "Incorrect password. Please enter the correct password.",parent=self.root)                 
                    else:
                        messagebox.showerror("Error", "Not enough seats available.", parent=self.root)    
            else:
                messagebox.showerror("Error", "Please add at least one passenger.", parent=self.root)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers for age.", parent=self.root)

    def calculate_fare(self,selected_seats):
        if self.train_class=="Chair-Car(CC)":
            return (210*selected_seats)+15.71
        if self.train_class=="Sleeper":
            return (430*selected_seats)+15.71
        if self.train_class=="1st AC":
            return (2780*selected_seats)+15.71
        if self.train_class=="2nd AC":
            return (1860*selected_seats)+15.71
        else:
            return (870*selected_seats)+15.71
    
    def check_password(self, entered_password):
        stored_password = y.get()
        return entered_password == stored_password

    def validate_passenger_entry(self, entry):
        frame, name_entry, age_entry, sex_combobox = entry
        name = name_entry.get().strip()
        age = age_entry.get().strip()
        sex = sex_combobox.get()
        if not name or not age or not sex:
            messagebox.showerror("Error", "Please enter all fields", parent=self.root)
            return False
        try:
            age = int(age)
            if age <= 5:
                messagebox.showerror("Error", "Please enter age Greater than 5", parent=self.root)
                return False
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for age.", parent=self.root)
            return False
        if sex not in ["Male", "Female", "Others"]:
            messagebox.showerror("Error", "Please Select any Gender", parent=self.root)
            return False
        return True
    
    def check_seat_availability(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="123456", database="passengerregister")
        my_cursor = conn.cursor()

        query = "SELECT available_seats FROM seat_availability WHERE date_of_journey = %s AND train_class = %s AND train_name = %s"
        values = (self.date_of_journey, self.train_class, self.train_name)
        my_cursor.execute(query, values)
        result = my_cursor.fetchone()

        if result:
            conn.close()
            return result[0]
        else:
            try:
                insert_query = "INSERT INTO seat_availability (date_of_journey, train_class, available_seats, train_name) VALUES (%s, %s, %s, %s)"
                available_seats = 70
                insert_values = (self.date_of_journey, self.train_class, available_seats, self.train_name)
                my_cursor.execute(insert_query, insert_values)
                conn.commit()
            except mysql.connector.Error as err:
                print("Error inserting available seats:", err)
            finally:
                conn.close()
                return available_seats

    def update_available_seats(self, booked_seats):
        self.available_seats -= booked_seats
        self.label_seats_available.config(text="Available Seats: {}".format(self.available_seats))

    def update_available_seats_in_database(self, num_seats):
        conn = None
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="123456", database="passengerregister")
            my_cursor = conn.cursor()

            check_query = "SELECT * FROM seat_availability WHERE (date_of_journey = %s AND train_class = %s AND train_name = %s)"
            check_values = (self.date_of_journey, self.train_class,self.train_name)
            my_cursor.execute(check_query, check_values)
            existing_record = my_cursor.fetchone()

            if existing_record:
                update_query = "UPDATE seat_availability SET available_seats = available_seats - %s WHERE (date_of_journey = %s AND train_class = %s AND train_name = %s)"
                update_values = (num_seats, self.date_of_journey, self.train_class,self.train_name)
                my_cursor.execute(update_query, update_values)
            else:
                insert_query = "INSERT INTO seat_availability (date_of_journey, train_class, available_seats,train_name) VALUES (%s, %s, %s,%s)"
                available_seats = 70 - num_seats  
                insert_values = (self.date_of_journey, self.train_class, available_seats,self.train_name)
                my_cursor.execute(insert_query, insert_values)

            conn.commit()
        except mysql.connector.Error as err:
            print("Error updating/inserting available seats:", err)
        finally:
            if conn is not None and conn.is_connected():
                conn.close()   
    
    def save_passengers(self):
        try:
            conn=mysql.connector.connect(host="localhost", username="root", password="123456", database="passengerregister")
            my_cursor = conn.cursor()
            query = "SELECT max(id) from tickets"
            my_cursor.execute(query)
            uid=my_cursor.fetchone()[0]
            conn.commit()
        except mysql.connector.Error as err:
            print("Error saving ticket information:", err)
        finally:
            if conn.is_connected():
                conn.close()
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="123456", database="passengerregister")
            my_cursor = conn.cursor()
            for item in self.passenger_entries:
                name = item[1].get()
                age = item[2].get()
                sex = item[3].get()
                query = "INSERT INTO passenger_info (id, name, age, sex) VALUES (%s, %s, %s, %s)"
                values = (uid, name, age, sex)
                my_cursor.execute(query, values)
                conn.commit()
        except mysql.connector.Error as err:
            print("Error saving ticket information:", err)
        finally:
            if conn.is_connected():
                conn.close()     
    
    def save_ticket_info(self, num_passengers):
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="123456", database="passengerregister")
            my_cursor = conn.cursor()

            fetch_username_query = "SELECT email FROM register WHERE email = %s"
            fetch_username_values = (self.username,)
            my_cursor.execute(fetch_username_query, fetch_username_values)
            fetched_username = my_cursor.fetchone()

            if fetched_username:
                username = fetched_username[0]
                booking_date = date.today()
                query = "INSERT INTO tickets (username, train_name, num_passengers, booking_date, date_of_journey, train_class) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (username, self.train_name, num_passengers, booking_date, self.date_of_journey, self.train_class)
                my_cursor.execute(query, values)
                conn.commit()
            else:
                print("Error: Unable to fetch username for the provided email.")

        except mysql.connector.Error as err:
            print("Error saving ticket information:", err)
        finally:
            if conn.is_connected():
                conn.close()
    
    
if __name__ == "__main__":
    root = tk.Tk()
    # Provide the required arguments for TicketBookingApp
    app = TicketBookingApp(root, "your_username", "2024-01-20", "Sleeper")
    root.mainloop()
