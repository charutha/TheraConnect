import tkinter as tk
import mysql.connector
from tkinter import ttk, messagebox
import credentials as cr
from tkcalendar import Calendar
from practice import UserSettingsPage
from datetime import datetime
import datetime
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage
import subprocess
import sys
class MyGUI:
    def __init__(self,U_NAME):
        root = tk.Tk()
        self.root = root
        self.username=U_NAME
        self.selected_time_slots = {}
        self.root.title("Doctor Search")
        self.bg_img = ImageTk.PhotoImage(file="appt1.png")
        self.image=ImageTk.PhotoImage(file="search.jpg")
        background = Label(self.root,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)
        #self.bg_img = PhotoImage(file="C:/Users/pchai/OneDrive/Desktop/dbms/theraconnect/project/appt.jpeg")
        #background = Label(root, image=self.bg_img)
        #background.place(x=0, y=0, relwidth=1, relheight=1)
        #self.root.attributes('-fullscreen', True)
        #self.overrideredirect(True)  # Remove window decorations (optional)
        self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.selected_option = tk.StringVar()
        label = tk.Label(root, text="Select an option:", font=("times new roman", 12))
        label.place(x=100, y=100)
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cursor = connection.cursor()
        cursor.execute("SELECT u_id FROM user WHERE username = %s", (self.username,))
        result= cursor.fetchone()
        if result:
            self.userid = result[0]
        else:
            # Handle the case where no results were found for the username
            self.userid = None
        #print("uid in s.py is",self.userid)
        connection.commit()
        cursor.close()
        connection.close()
        """options = ["Name", "Experience", "Age","Highest Rating","New Doctor","Highest Rating in Trauma_Informed","Maximum Reviews","Speciality"]
        dropdown = tk.OptionMenu(root, self.selected_option, *options)
        dropdown.config(bg="white", font=("times new roman", 12))
        dropdown.place(x=250, y=100)"""
        option_buttons = []
        options = ["Name", "Experience", "Highest Rating in Trauma_Informed", "Highest Rating", "New Doctor", "Age", "Maximum Reviews", "Speciality","Sex"]
        label = tk.Label(root, text="2.Select a button",font = ("Times New Roman", 12, "bold italic underline"))
        label.place(x=250, y=50)
        for i, option in enumerate(options):
            option_button = tk.Button(root, text=option, command=lambda opt=option: self.set_selected_option(opt))
            option_buttons.append(option_button)
            option_button.place(x=250 , y=100+ i*30)

        find_doctor_button = tk.Button(root, text="Find Doctor", command=self.find_doctor)
        find_doctor_button.place(x=100, y=150)
        label = tk.Label(root, text="3.Apply Selected Options",font = ("Times New Roman", 12, "bold italic underline"))
        label.place(x=50, y=125)
        label = tk.Label(root, text="Find MHP",font = ("Times New Roman", 12, "bold italic underline"))
        label.place(x=600, y=50)
        #font=("times new roman", 12)

        # Create an empty Treeview widget initially (hidden)
        self.tree = ttk.Treeview(root, columns=("FirstName", "LastName", "Age", "Experience", "Qualification","Sex"))
        self.tree.heading("#1", text="First Name")
        self.tree.heading("#2", text="Last Name")
        self.tree.heading("#3", text="Age")
        self.tree.heading("#4", text="Experience")
        self.tree.heading("#5", text="Qualification")
        self.tree.heading("#6", text="Sex")
        self.tree.column("#1", width=100)
        self.tree.column("#2", width=100)
        self.tree.column("#3", width=50)
        self.tree.column("#4", width=100)
        self.tree.column("#5", width=200)
        self.tree.column("#6", width=200)
        #self.tree.place(x=200,y=200)
        self.tree.tag_configure("button", foreground="blue")
        self.tree.tag_bind("button", "<Button-1>", self.show_schedule)
        self.username=U_NAME
        #user_settings = UserSettingsPage(root, username)
        #settings_button = tk.Button(root, text="Settings", command=user_settings.display_user_data)
        settings_button = tk.Button(root, text="Settings", command=self.redirect)
        #print("s.py uname",self.username)
        """settings_button.pack()

        settings_button = tk.Button(root, text="Settings", command=self.open_settings)"""
        settings_button.place(x=700, y=10) 
        self.date_dropdown = tk.StringVar()
        self.date_dropdown.set("Select Date")
        self.date_dropdown_menu = ttk.Combobox(root, textvariable=self.date_dropdown)
        self.date_dropdown_menu.place(x=100, y=100)
        label = tk.Label(root, text="1.Select A Date",font = ("Times New Roman", 12, "bold italic underline"))
        label.place(x=100, y=50)

        # Calculate the next 5 days
        today = datetime.date.today()
        print("todays date",today)
        #today="2023-11-06"
        #if new_start_day not in ["Sunday","Saturday"]:       
        #next_5_days = [today + datetime.timedelta(days=i) for i in range(1, 6)]
        #print("next 5 days",next_5_days)
        next_5_days = [today + datetime.timedelta(days=i-1) if (today + datetime.timedelta(days=i)).strftime('%A') in ["Saturday", "Sunday"] else today + datetime.timedelta(days=i) for i in range(1, 6)]
        
        #next_5_days = [today + datetime.timedelta(days=i) for i in range(1, 6) if (today + datetime.timedelta(days=i)).weekday() not in [5, 6]]
        print(next_5_days)

        # Format and add the next 5 days to the dropdown menu
        formatted_dates = [date.strftime("%Y/%m/%d") for date in next_5_days]
        self.date_dropdown_menu['values'] = formatted_dates
        root.mainloop()
    def set_selected_option(self, option):
        selected_option = self.selected_option.get()
        self.selected_option.set(option)
        """if selected_option == "Speciality":
            self.text_entry1.destroy()  # Remove the "Enter Speciality" entry box
            self.label1.destroy()"""
        if option=="Name":
            self.label = tk.Label(self.root, text="Enter First Name")
            self.label.place(x=250, y=50)
            self.text_entry = tk.Entry(self.root)
            self.text_entry.place(x=350, y=100)
        elif option=="Speciality":
            self.label1 = tk.Label(self.root, text="Enter Speciality(trauma informed(T), child specialist(C) ,disability friendly(D) ,Queer friendly(Q))")
            self.label1.place(x=250, y=50)
            self.text_entry1 = tk.Entry(self.root)
            self.text_entry1.place(x=350, y=100)
        
    def find_doctor(self):
        selected_option = self.selected_option.get()
        #print(selected_option)
        #user_input="hello"

        """if selected_option=="Name" or selected_option=="Name" or selected_option=="Name" or selected_option=="Name":
            label1 = tk.Label(self.root, text="Enter First Name")
            label1.place(x=250, y=50)
            self.text_entry = tk.Entry(self.root)
            self.text_entry.place(x=350, y=100)"""
    

        if selected_option=="Name":
            user_input = self.text_entry.get()
            self.text_entry.destroy()  # Remove the "Enter Speciality" entry box
            self.label.destroy()
            if user_input=="":
             messagebox.showerror("Please enter valid details", parent=self.root)
             return
        


        """if user_input == "" or (selected_option!="Highest Rating" and selected_option!="New Doctor" and selected_option!="Highest Rating in Trauma_Informed" and selected_option!="Maximum Reviews"):
            messagebox.showerror("Please enter valid details", parent=self.root)
            return"""

        try:
            connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cur = connection.cursor()
            query = ""

            if selected_option == "Name":
                query = "SELECT first_name, last_name, age, experience, qualification FROM mhp WHERE First_Name = %s"
                cur.execute(query, (user_input,))

            elif selected_option == "Experience":
                query = "SELECT first_name, last_name, age, experience, qualification FROM mhp order by experience"
                cur.execute(query)
            elif selected_option == "Highest Rating":
                query = """SELECT m.first_name, m.last_name, m.age, m.experience, m.qualification,m.sex
                FROM mhp m
                JOIN (
                    SELECT m_id, Rating
                    FROM Review
                    WHERE Rating = (
                        SELECT MAX(Rating)
                        FROM Review
                    )
                ) max_rated_doctors
                ON m.m_id = max_rated_doctors.m_id;"""
                #print("executed query")
                #cur.execute(query, (user_input,))
                cur.execute(query)
            elif selected_option == "New Doctor":
                query = "SELECT first_name, last_name, age, experience, qualification,sex FROM mhp where m_id NOT IN (SELECT m_id FROM Review)"
                cur.execute(query)
            elif selected_option == "Maximum Reviews":
                query = """SELECT D.First_Name, D.Last_Name, D.Age, D.Experience, D.Qualification
                    FROM mhp D
                    WHERE D.M_ID = (
                        SELECT Subquery.DoctorID
                        FROM (
                            SELECT D.M_ID AS DoctorID, COUNT(*) AS ReviewCount
                            FROM Review R
                            JOIN mhp D ON R.M_ID = D.M_ID
                            GROUP BY DoctorID
                            ORDER BY ReviewCount DESC
                            LIMIT 1
                        ) AS Subquery
                    );

                    """
                cur.execute(query)
            elif selected_option == "Highest Rating in Trauma_Informed":
                print("entered rt")
                query = """
                    SELECT D.first_name, D.last_name, D.age, D.experience, D.qualification
                    FROM mhp D
                    JOIN speciality S ON D.m_id = S.m_id
                    WHERE (SELECT AVG(R.rating) FROM review R WHERE R.m_id = D.m_id) > (
                        SELECT AVG(avgrating)
                        FROM (
                            SELECT D1.m_id, AVG(R1.rating) AS avgrating
                            FROM mhp D1
                            JOIN review R1 ON D1.m_id = R1.m_id
                            JOIN speciality S1 ON D1.m_id = S1.m_id
                            WHERE S1.Trauma_Informed = 1
                            GROUP BY D1.m_id
                        ) AS subquery
                    )
                """
                cur.execute(query)

            elif selected_option == "Age":
                query = "SELECT first_name, last_name, age, experience, qualification FROM mhp order by age"
                #print(user_input)
                #cur.callproc("SearchDoctorsByAge", (user_input,))
                cur.execute(query)
            elif selected_option == "Sex":
                query = "SELECT first_name, last_name, age, experience, qualification ,sex FROM mhp order by sex"
                #print(user_input)
                #cur.callproc("SearchDoctorsByAge", (user_input,))
                cur.execute(query)

            elif selected_option == "Speciality":
                user_input = self.text_entry1.get()
                self.text_entry1.destroy()  # Remove the "Enter Speciality" entry box
                self.label1.destroy()
                print("user_input",user_input)
                speciality_codes = user_input.split(",")  
                print("Sc",speciality_codes)
                specialities = []
                speciality_mapping = {
                    'D': "disability_friendly",
                    'T': "trauma_informed",
                    'Q': "queer_friendly",
                    'C': "child_specialist"
                }
                for code in speciality_codes:
                    if code in speciality_mapping:
                        specialities.append(speciality_mapping[code])

                for i in specialities:
                    print("value",i)

                speciality_conditions = " AND ".join([f"s.{speciality} = 1" for speciality in specialities])
                print("Speciality conditions are",speciality_conditions)

                query = f"""
                    SELECT m.first_name, m.last_name, m.age, m.experience, m.qualification
                    FROM mhp m
                    JOIN speciality s ON m.m_id = s.m_id
                    WHERE {speciality_conditions};
                """
                print("Query is:",query)
                cur.execute(query)
                Rows = cur.fetchall()
                print("Rows are",Rows)
                print("Error:")
            else:
                messagebox.showerror("Invalid Option", "Please select a valid option", parent=self.root)
                return

            #cur.execute(query, (user_input,))
            rows = cur.fetchall()
            if selected_option=="Speciality":
                rows=Rows
            print("rows",rows)

            if rows:
                # Clear previous entries in the Treeview
                for item in self.tree.get_children():
                    self.tree.delete(item)

                # Insert retrieved data into the Treeview
                # Inside your find_doctor function
                for row in rows:
                    item_id = self.tree.insert("", "end", values=row)
                    self.tree.item(item_id, tags=("button",))  # Apply the "button" tag

                # Bind the click event outside the loop
                self.tree.bind("<Button-1>", self.handle_tree_click)
                #self.tree.pack(padx=100, pady=200)
                self.tree.place(x=400,y=200)

            else:
                messagebox.showinfo("Doctor Not Found", "No doctor found for the provided details", parent=self.root)

        except Exception as e:
            print(e)





    def redirect(self):
        print("s.py inside redirect uname",self.username)
        subprocess.Popen(["python","user_settings.py",self.username])



    def show_schedule(self, item_id):
        # Check if the selected item_id exists in the Treeview
        if self.tree.exists(item_id):
            # Get the selected doctor's data from the Treeview
            selected_doctor_data = self.tree.item(item_id, "values")
            if selected_doctor_data:
                doctor_name = selected_doctor_data[0]
                try:
                    connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                    cur = connection.cursor()

                    # Query to fetch the M_ID based on the doctor's name
                    m_id_query = "SELECT M_ID FROM mhp WHERE First_name = %s"
                    cur.execute(m_id_query, (doctor_name,))
                    m_id = cur.fetchone()

                    if m_id:
                        m_id = m_id[0] 
                        self.m_id=m_id
                        #print("m_id is",m_id)
                        # Create a new window for displaying the schedule
                        selected_date = self.date_dropdown.get()
                        print("selcted date is",selected_date)
                        if selected_date=="Select Date":
                            messagebox.showinfo("No Date Selected", "Select a Date", parent=self.root)
                        else:
                            schedule_window = tk.Toplevel(self.root)
                            schedule_window.title(f"Schedule for Dr. {doctor_name}")


                        

                        # Query to fetch the schedule of the selected doctor using the M_ID
                        
                        
                        print(selected_date)
                        formatted_date = datetime.datetime.strptime(selected_date, "%Y/%m/%d").strftime("%Y-%m-%d")
                        schedule_query = f"SELECT 9_10AM, 10_11AM, 11_12AM, 12_1PM, 1_2PM, 2_3PM, 3_4PM, 4_5PM FROM schedule WHERE M_ID = {m_id} AND Date = '{formatted_date}'"
                        #schedule_query = f"SELECT 9_10AM, 10_11AM, 11_12AM, 12_1PM, 1_2PM, 2_3PM, 3_4PM, 4_5PM FROM schedule WHERE M_ID = {m_id}"
                        cur.execute(schedule_query)
                        schedule_data = cur.fetchone()
                        print(schedule_data)
                        if schedule_data:
                            time_slots = ["9_10AM", "10_11AM", "11_12AM", "12_1PM", "1_2PM", "2_3PM", "3_4PM", "4_5PM"]
                            schedule_frame = tk.Frame(schedule_window)
                            schedule_frame.pack(padx=20, pady=20)

                            label1 = tk.Label(schedule_frame, text="Choose your time slots")
                            label1.grid(row=0, column=0, columnspan=2)

                            self.selected_time_slots = {}  # Dictionary to store selected time slots
                            self.mode_var = tk.StringVar()
                            self.location_var = tk.StringVar()

                            for i, bit in enumerate(schedule_data):
                                print(i,int(bit))
                                if int(bit) == 0:
                                    time_slot = time_slots[i]
                                    checkbox_var = tk.IntVar()
                                    checkbox = tk.Checkbutton(schedule_frame, text=time_slot, variable=checkbox_var)
                                    checkbox.grid(row=i + 1, column=0, sticky="w")

                                    # Save the selected time_slot along with its Checkbutton's variable for later use
                                    self.selected_time_slots[time_slot] = checkbox_var

                            # Create labels and entry boxes for mode and location
                            mode_label = tk.Label(schedule_frame, text="Mode:")
                            mode_label.grid(row=len(time_slots) + 1, column=0, sticky="w")

                            mode_entry = tk.Entry(schedule_frame, textvariable=self.mode_var)
                            mode_entry.grid(row=len(time_slots) + 1, column=1)

                            location_label = tk.Label(schedule_frame, text="Location:")
                            location_label.grid(row=len(time_slots) + 2, column=0, sticky="w")

                            location_entry = tk.Entry(schedule_frame, textvariable=self.location_var)
                            location_entry.grid(row=len(time_slots) + 2, column=1)

                            submit_button = tk.Button(schedule_frame, text="Submit", command=self.submit_selected_time_slots)
                            submit_button.grid(row=len(time_slots) + 5, column=0, columnspan=2, pady=10)

                        else:
                            messagebox.showinfo("Schedule Not Found", "Doctor is unavailable.Choose Different Date", parent=schedule_window)
                    else:
                        messagebox.showinfo("Doctor Not Found", "Doctor with the given name not found in the database", parent=self.root)

                except Exception as e:
                    print(e)

    def submit_selected_time_slots(self):
   
        selected_time_slots = []
        start_times = []
        end_times = []
        time_slot_mapping = {
                "9_10AM": {"start_time": "09:00:00", "end_time": "10:00:00"},
                "10_11AM": {"start_time": "10:00:00", "end_time": "11:00:00"},
                "11_12AM": {"start_time": "11:00:00", "end_time": "12:00:00"},
                "12_1PM": {"start_time": "12:00:00", "end_time": "13:00:00"},
                "1_2PM": {"start_time": "13:00:00", "end_time": "14:00:00"},
                "2_3PM": {"start_time": "14:00:00", "end_time": "15:00:00"},
                "3_4PM": {"start_time": "15:00:00", "end_time": "16:00:00"},
                "4_5PM": {"start_time": "16:00:00", "end_time": "17:00:00"},
                }
        for time_slot, checkbox_var in self.selected_time_slots.items():
            if checkbox_var.get() == 1:
                selected_time_slots.append(time_slot)
        for i in selected_time_slots:
            if i in time_slot_mapping:
                start_time = time_slot_mapping[i]["start_time"]
                #print("start time",start_time)
                end_time = time_slot_mapping[i]["end_time"]
                #print("end time",end_time)
                start_times.append(start_time)
                end_times.append(end_time)

        overall_start_time = min(start_times)
        overall_end_time = max(end_times)
        start_time = datetime.datetime.strptime(overall_start_time, '%H:%M:%S')
        end_time = datetime.datetime.strptime(overall_end_time, '%H:%M:%S')
        time_difference = end_time - start_time
        hours, remainder = divmod(time_difference.seconds, 3600)
        self.insert_appointment(overall_start_time,overall_end_time,hours)
            
    def payment(self,hours):        
        price = self.get_price_from_database(self.m_id, hours)
        #print(price)
        def submit_payment():
            method = payment_entry.get()
            #print("Method is", method)
            self.finish_payment(price, method)
            user_details_window.destroy()

        user_details_window = tk.Toplevel(self.root)
        user_details_window.title("Payment Form")
        user_details_window.geometry("300x300")
        price_label = tk.Label(user_details_window, text=f"Price: ${price}")
        price_label.pack()

        payment_label = tk.Label(user_details_window, text="Method Of Payment(CASH/PAYMENT/GOOGLE PAY):")
        payment_label.pack()

        payment_entry = tk.Entry(user_details_window)
        payment_entry.pack()

        submit_button = tk.Button(user_details_window, text="Submit", command=submit_payment, width=10, height=2)
        submit_button.pack()
    
    def insert_appointment(self,start_time,end_time,hours):
        try:
            connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM appointment")
                a_id = cursor.fetchone()[0] + 1
                #print("a_id is",a_id)
                status = "pending"
                mode=self.mode_var.get()
                location=self.location_var.get()
                userid=self.userid
                #print("userid,",userid)
                mid=self.m_id
                prescription="hello"
                appointment_query = "INSERT INTO appointment (U_ID,M_id,Date,START_TIME,END_TIME,MODE,LOCATION,STATUS) VALUES (%s, %s,%s, %s,%s, %s, %s, %s)"
                appointment_values = (userid,mid,self.date_dropdown.get(),start_time,end_time,mode,location,status)
                cursor.execute(appointment_query, appointment_values)
                connection.commit()
                cursor.execute("SELECT LAST_INSERT_ID()")
                self.a_id = cursor.fetchone()[0]
                #print("a_id is",self.a_id)
                #print("Appointment and payment details inserted successfully.")
                self.payment(hours)

        except mysql.connector.Error as error:
            print("Error: ", error)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def finish_payment(self,price,method):
        #print("entered into finish payment")
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cursor = connection.cursor()
        status="pending"
        #print(self.userid,self.a_id,price,method,status)
        query = "INSERT INTO payment_history (U_ID,A_ID,PRICE,METHOD_OF_PAYMENT,STATUS) VALUES (%s, %s,%s, %s,%s)"
        values = (self.userid,self.a_id,price,method,status)
        cursor.execute(query,values)
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Booked","Appointment Booked Successfully!", parent=self.root)


    def get_price_from_database(self, doctor_id, num_hours):
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cursor = connection.cursor()
        query = "SELECT CalculateTotalPrice(%s, %s)"
        cursor.execute(query, (doctor_id, num_hours))

        #cursor.callfunc("CalculateTotalPrice", (doctor_id, num_hours))
        
        # Fetch the result of the stored function
        result = cursor.fetchone()
        price=result[0]
        connection.close()

        if result:
            #print("price",result[0])
            return price
        else:
            print("Price not found")

        
    def create_book_appointment_button(self, doctor):
        # Create a "Book Appointment" button for the given doctor
        book_appointment_button = tk.Button(self.tree, text="Book Appointment", command=lambda doctor=doctor: self.show_schedule(doctor))
        self.tree.window_create(doctor, window=book_appointment_button)

    def open_settings(self):
        # Create an instance of your userSettings class
        try:
            settings_window = tk.Toplevel()
            #username = "chaitra08"
            settings_window.title("User Settings")
            settings = UserSettingsPage(settings_window,U_NAME)
        except Exception as e:
            print(f"Error opening settings: {e}")

    
    def handle_tree_click(self, event):
        item_id = self.tree.identify_row(event.y)  # Get the item ID that was clicked
        if self.tree.tag_has("button", item_id):
                #print(item_id)
                self.show_schedule(item_id)

    """def redirect_window(self):
        username=self.uname_txt.get()
        self.window.destroy()
        subprocess.Popen(["python","s.py"])"""

   

if __name__ == '__main__':
    U_NAME=sys.argv[1]
    #print(U_NAME)
    if U_NAME is not None:
        U_NAME=str(U_NAME)
    #root = tk.Tk()
    #U_NAME="nirvan"
    app = MyGUI(U_NAME)
    #root.mainloop()
