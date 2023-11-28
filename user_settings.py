import tkinter as tk
from tkinter import ttk
import mysql.connector
import credentials as cr
import sys
import threading
from datetime import datetime
import datetime
import time
from tkinter import ttk, messagebox,Scrollbar
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage
class UserSettingsPage():
    def __init__(self, username):
        #root=
        #self.root = root
        self.username = username
        print("inside practice.py username init",self.username)
        self.display_user_data()
        #self.userid=1
        self.entry_widgets = None
        self.values = None

    def edit_selected_review(self, review_tree):
        selected_item = review_tree.selection()

        if selected_item:
            item = review_tree.item(selected_item, 'values')

            if item:
                p = item[0]
                #print(p)
                edit_window = tk.Toplevel()
                edit_window.title("Edit Review")

                column_names = ["Doctor Name","Date", "Title", "Comment", "Rating"]
                self.entry_widgets = []

                for i, column_name in enumerate(column_names):
                    label = tk.Label(edit_window, text=column_name)
                    label.grid(row=i, column=0)

                    initial_value = item[i] if i < len(item) else ""  # Handle missing values
                    entry = tk.Entry(edit_window)
                    entry.insert(0, initial_value)
                    entry.grid(row=i, column=1)

                    self.entry_widgets.append(entry)

                def update_review():
                    new_values = [entry.get() for entry in self.entry_widgets]

                    #print(new_values)
                    connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                    cursor = connection.cursor()
                    mhp_name = p 
                    cursor.execute("SELECT m_id FROM mhp WHERE first_name = %s", (mhp_name,))
                    result = cursor.fetchone()
                    print("mid is",result[0])
                    new_values =[entry.get() for entry in self.entry_widgets]
                    for i in new_values:
                        print(i)
                    #new_values = new_values[:2] + new_values[3:]
                    print(new_values)

                    if result:
                        m_id = result[0]
                        column_names = ["Doctor Name", "Date", "Title", "Comment", "Rating"]

                        for i, column_name in enumerate(column_names):
                            if column_name == "Doctor Name":
                                #messagebox.showinfo("Cannot Update this field")
                                # In this case, we don't update the "Doctor Name" because it's in the 'mhp' table.
                                continue

                            query = f"UPDATE review SET {column_name} = %s WHERE M_id = %s"
                            cursor.execute(query, (new_values[i], m_id))

                    connection.commit()
                    connection.close()
                    self.update_review_tree(review_tree)
                    edit_window.destroy()
                update_button = tk.Button(edit_window, text="Update", command=update_review)
                update_button.grid(row=len(column_names), columnspan=2)
#############################################################################################################################################################
    def add_review(self,review_tree):
   
        add_window = tk.Toplevel()
        add_window.title("Add Review")

        column_names = ["Doctor Name","Title", "Comment", "Rating(1-5)"]
        self.entry_widgets = []

        for i, column_name in enumerate(column_names):
            label = tk.Label(add_window, text=column_name)
            label.grid(row=i, column=0)

            entry = tk.Entry(add_window)
            entry.grid(row=i, column=1)

            self.entry_widgets.append(entry)

        def insert_review():
            current_datetime = datetime.datetime.now()
            current_date = current_datetime.date()
            new_values = [self.userid] + [current_date] + [entry.get() for entry in self.entry_widgets]
            print(new_values)
            print("user_id is",self.userid)
            connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cursor = connection.cursor()
            mhp_name = new_values[2]
            print(mhp_name)
            cursor.execute("SELECT m_id FROM mhp WHERE first_name = %s", (mhp_name,))
            result = cursor.fetchone()
            if result:
                self.mhp_id = result[0]
                new_values =[self.mhp_id] + [self.userid] + [current_date] + [entry.get() for entry in self.entry_widgets]
                new_values = new_values[:3] + new_values[4:]
                print(new_values)
            query = "INSERT INTO review (M_ID,U_ID,Date, Title, Comment, Rating) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, tuple(new_values))
            connection.commit()
            connection.close()
            self.update_review_tree(review_tree)
            add_window.destroy()

        add_button = tk.Button(add_window, text="Add Review", command=insert_review)
        add_button.grid(row=len(column_names), columnspan=2)
##############################################################################################################################################################33
    def delete_review(self,review_tree):
        selected_item = review_tree.selection()
        if selected_item:
            item = review_tree.item(selected_item, 'values')
            if item:
                mhp_name = item[0]
                #print(p)
                connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                cursor = connection.cursor()
                cursor.execute("SELECT m_id FROM mhp WHERE first_name = %s", (mhp_name,))
                result = cursor.fetchone()
                print("doctor id",result)
                if result:
                    mhp_id = result[0]
                    query = "DELETE FROM review WHERE M_ID = %s AND U_ID = %s"
                    cursor.execute(query, (mhp_id, self.userid))
                    connection.commit()
                    connection.close()
                    self.update_review_tree(review_tree)
####################################################################################################################################################3
    def delete_payment(self, a_id,u_id):
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cursor = connection.cursor()
        print("entered into payment deletion")
        print("pau", a_id, u_id)
        
        try:
            # Delete the payment from payment_history with the corresponding A_ID
            payment_delete_query ="UPDATE payment_history set status=%s where u_id=%s and a_id=%s"
            cursor.execute(payment_delete_query, ("cancelled",u_id, a_id))
            print("payment deleted")
            
            # Commit the transaction
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error deleting payment: {err}")
        finally:
            cursor.close()
            connection.close()

    def get_aid(self, u_id,date):
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cursor = connection.cursor()
        print("entered into aid")
        print("a_id u_id is", u_id)
        
        try:
            # Get the A_ID from the appointment table based on U_ID
            payment_delete_query = "SELECT a_id FROM appointment WHERE U_ID = %s and date=%s and status=%s"
            cursor.execute(payment_delete_query, (u_id,date,"cancelled"))
            a_id = cursor.fetchone()[0]
            print("aid is", a_id)
            
            # Call the delete_payment function
            #self.delete_payment(u_id, a_id)
        except mysql.connector.Error as err:
            print(f"Error getting A_ID: {err}")
        finally:
            cursor.close()
            connection.close()
            self.delete_payment(a_id, u_id)
    
    def cancel_appointment(self, appt_tree1):
        selected_item = appt_tree1.selection()
        if selected_item:
            item = appt_tree1.item(selected_item, 'values')
            print("item is", item)
            #u_id = item[0] 
            date=item[1] 
            print("u_id is", self.userid)
            self.start_time_user=item[2]
            end_time_user=item[3]
            start_time = datetime.datetime.strptime(self.start_time_user, '%H:%M:%S')
            end_time = datetime.datetime.strptime(end_time_user, '%H:%M:%S')
            time_difference = end_time - start_time
            self.num_hours, remainder = divmod(time_difference.seconds, 3600)
            print("st and et is:",self.start_time_user,end_time_user,self.num_hours)
            #self.delete_payment(u_id)
            print("entered update")
            connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cursor = connection.cursor()

            try:
                # Delete the appointment where the date matches and status is 'upcoming'
                appt_delete_query = "update appointment set status=%s WHERE date = %s AND status = %s and u_id=%s"
                cursor.execute(appt_delete_query, ("cancelled",item[1], "upcoming",self.userid))
                print("appointment cancelled")
                # Commit the transaction
                connection.commit()
                query="SELECT m_id from mhp where first_name=%s"
                cursor.execute(query,(item[0],))
                m_id = cursor.fetchone()[0]
                #query="update schedule where m_id=%s and date=%s
                slots_to_update = []
                time_slot_mapping = {
                "9_10AM": {"start_time": "9:00:00", "end_time": "10:00:00"},
                "10_11AM": {"start_time": "10:00:00", "end_time": "11:00:00"},
                "11_12AM": {"start_time": "11:00:00", "end_time": "12:00:00"},
                "12_1PM": {"start_time": "12:00:00", "end_time": "13:00:00"},
                "1_2PM": {"start_time": "13:00:00", "end_time": "14:00:00"},
                "2_3PM": {"start_time": "14:00:00", "end_time": "15:00:00"},
                "3_4PM": {"start_time": "15:00:00", "end_time": "16:00:00"},
                "4_5PM": {"start_time": "16:00:00", "end_time": "17:00:00"},
                }
                """for slot, slot_times in time_slot_mapping.items():
                    slot_start_time = slot_times["start_time"]
                    slot_end_time = slot_times["end_time"]
                    print("start_time",slot_start_time)
                    print("end_time",slot_end_time)
                    #if start_time_user <= slot_start_time and end_time_user >= slot_end_time:
                    if start_time <= slot_start_time < end_time or start_time < slot_end_time <= end_time:
                        print("st and et of user is:",self.start_time_user,end_time_user)
                        print("slots",slot)
                        slots_to_update.append(slot)
                print(slots_to_update)"""
                #WORKING TILL HERE
                result_time_slots1 = []
                result_time_slots1 =self.calculate_time_slots()
                print("resultant:",result_time_slots1)
                for slot in result_time_slots1:
                    #update_query="UPDATE Schedule AS s SET"+ f"s.{slot}=0 WHERE s.M_id=%s AND s.Date=%s"
                    update_query = f"UPDATE Schedule AS s SET s.{slot} = 0 WHERE s.M_id = %s AND s.Date = %s"
                    cursor.execute(update_query, (m_id, date))
                    connection.commit()
            except mysql.connector.Error as err:
                print(f"Error deleting appointment: {err}")
            finally:
                cursor.close()
                connection.close()
                self.get_aid(self.userid,date)

            self.update_appt_tree1(appt_tree1)

   

    def calculate_time_slots(self):
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

        start_time = datetime.datetime.strptime(self.start_time_user, '%H:%M:%S')
        end_time = start_time + datetime.timedelta(hours=self.num_hours)

        time_slots = []

        for slot, slot_times in time_slot_mapping.items():
            slot_start_time = datetime.datetime.strptime(slot_times["start_time"], '%H:%M:%S')
            slot_end_time = datetime.datetime.strptime(slot_times["end_time"], '%H:%M:%S')

            if start_time <= slot_start_time < end_time or start_time < slot_end_time <= end_time:
                time_slots.append(slot)

        return time_slots



   
###########################################################################################################################################################
    def edit_selected_user(self,user_tree):
        # Get the selected item from the Treeview
        selected_item = user_tree.selection()

        if selected_item:
            # Retrieve the data of the selected user
            item = user_tree.item(selected_item)
            self.values = item['values']
            p=self.values[1]
            print(self.values[1])
            if self.values[1]=="Date of Joining" or self.values[1]=="User ID" or self.values[1]=="Username":
                 messagebox.showinfo("Cannot Update this field")
            print(self.values[0])
            # Create a new window for editing
            edit_window = tk.Toplevel()
            edit_window.title("Edit User")
            labels=self.values[0]
            self.entry_widgets = []
            label = tk.Label(edit_window, text=labels)
            label.grid(row=1, column=0)

            entry = tk.Entry(edit_window)
            entry.insert(0, p) 
            entry.grid(row=1, column=1)
     
            self.entry_widgets.append(entry)
            # Create an "Update" button
            def update_user():
                # Get the new values from the Entry widgets
                new_values = [entry.get() for entry in self.entry_widgets]
                print(new_values)
                # Update the user data in the database
                connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                cursor = connection.cursor()

                # Construct and execute the SQL query to update the user data
                if labels=="User Id":
                   messagebox.showinfo("Cannot Change User ID", "You cannot change the User ID.")
                if labels=="First Name":
                    cursor.execute("update user set first_name=%s where first_name=%s", (new_values[0], p))
                if labels=="Last Name":
                    cursor.execute("update user set last_name=%s where last_name=%s", (new_values[0], p))
                if labels=="Date of Birth":
                    cursor.execute("update user set Date_of_Birth=%s where Date_of_Birth=%s", (new_values[0], p))
                if labels=="Date of Joining":
                    messagebox.showinfo("Cannot Change Date of Joining", "You cannot change the Date of Joining.")
                if labels=="Password":
                    cursor.execute("update user set Password=%s where Password=%s", (new_values[0], p))
                if labels=="Username":
                    messagebox.showinfo("Cannot Change Username", "You cannot change the Username.")
                if labels=="Phone Number":
                    cursor.execute("update user set phone=%s where phone=%s", (new_values[0], p))
                if labels=="Age":
                    cursor.execute("update user set age=%s where age=%s", (new_values[0], p))
                if labels=="Email":
                    cursor.execute("update user set email=%s where email=%s", (new_values[0], p))
                if labels=="Address":
                    cursor.execute("update user set address=%s where address=%s", (new_values[0], p))
                if labels=="Sex":
                    cursor.execute("update user set sex=%s where sex=%s", (new_values[0], p))
                connection.commit()
                connection.close()
                self.update_user_tree(user_tree)
                edit_window.destroy()

            update_button = tk.Button(edit_window, text="Update", command=update_user)
            update_button.grid(row=len(labels), columnspan=2)
#############################################################################################################################################

    def display_user_data(self):
        if self.username is not None:
            # Connect to the MySQL database
            connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cursor = connection.cursor()
            # Retrieve user data using the current_user variable
            cursor.execute("SELECT * FROM user WHERE username = %s", (self.username,))
            print("username is",self.username)
            user_data = cursor.fetchone()
            self.userid=user_data[0]
            print(self.userid)

            if user_data:
                def delete():
                    try:
                        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                        cursor = connection.cursor()

                        # Delete the user from the database
                        #cursor.execute("DELETE FROM user WHERE Username = %s", (self.username,))
                        """query=START TRANSACTION;

                        DELETE FROM prescription_history WHERE U_id=%s;
                        DELETE FROM review WHERE U_id = %s;
                        DELETE FROM payment_history WHERE U_id = %s;
                        DELETE FROM appointment WHERE U_id = %s;
                        DELETE FROM user WHERE U_id = %s;
                        COMMIT;

                        ROLLBACK;"""
                        # START TRANSACTION
                        cursor.execute("START TRANSACTION;")
                        connection.commit()

                        # DELETE FROM prescription_history
                        query = "DELETE FROM prescription_history WHERE a_id IN (SELECT a_id FROM appointment WHERE U_id = %s);"
                        cursor.execute(query, (self.userid,))
                        connection.commit()

                        # DELETE FROM review
                        query = "DELETE FROM review WHERE U_id = %s"
                        cursor.execute(query, (self.userid,))
                        connection.commit()

                        # DELETE FROM payment_history
                        query = "DELETE FROM payment_history WHERE U_id = %s"
                        cursor.execute(query, (self.userid,))
                        connection.commit()

                        # DELETE FROM appointment
                        query = "DELETE FROM appointment WHERE U_id = %s"
                        cursor.execute(query, (self.userid,))
                        connection.commit()

                        # DELETE FROM user
                        query = "DELETE FROM user WHERE U_id = %s"
                        cursor.execute(query, (self.userid,))
                        connection.commit()

                        # COMMIT
                        cursor.execute("COMMIT;")
                        connection.commit()

                        #cursor.execute(query, (self.userid,self.userid,self.userid,self.userid,self.userid))
                        print(self.username)
                        connection.commit()
                        connection.close()
                        self.settings_window.destroy()
                        messagebox.showinfo("DELETED", "Your Account Has Been Successfully Deleted!")
                        print("user successfully deleted")
                    except Exception as e:
                      print("Error:", str(e))


                # Create a tkinter window for the user settings
                self.settings_window = tk.Toplevel()
                self.settings_window.title("User Settings")
                self.bg_img = ImageTk.PhotoImage(file="mhp1.png")
                background = Label(self.settings_window,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)
                self.settings_window.geometry("{0}x{1}+0+0".format(self.settings_window.winfo_screenwidth(), self.settings_window.winfo_screenheight()))
                user_tree = ttk.Treeview(self.settings_window, columns=("Labels", "Details"), show="headings")
                label = tk.Label(self.settings_window, text="Your Details")
                label.place(x=50,y=50)
                delete_button = tk.Button(self.settings_window, text="Delete Your Account", command=delete)
                delete_button.place(x=200,y=50)
                pending_prescriptions_button = tk.Button(self.settings_window, text="Pending Prescriptions", command=self.show_pending_prescriptions)
                pending_prescriptions_button.place(x=100, y=650)
                all_prescriptions_button = tk.Button(self.settings_window, text="All Prescriptions", command=self.show_all_prescriptions)
                all_prescriptions_button.place(x=300, y=650)
                # Set the headings for the columns
                user_tree.heading("Labels", text="Labels")
                user_tree.heading("Details", text="Details")
                user_tree.column("Labels", width=100)
                user_tree.column("Details", width=150)
                self.userid=user_data[0]
                # Display the user's data
                labels = [
                    ("Username", user_data[1]),
                    ("Password", user_data[2]),
                    ("First Name", user_data[3]),
                    ("Last Name", user_data[4]),
                    ("Date of Birth", user_data[5]),
                    ("Age", user_data[6]),
                    ("Date of Joining", user_data[7]),
                    ("Phone Number", user_data[8]),
                    ("Email", user_data[9]),
                    ("Address", user_data[10]),
                    ("Sex", user_data[11])
                ]
                for label, value in labels:
                    user_tree.insert("", "end", values=(label, value))

                user_tree.place(x=50,y=100)
                user_tree.tag_configure("button", foreground="blue")
                user_tree.tag_bind("button", "<Button-1>", lambda event, tree=user_tree: self.edit_selected_user(user_tree))
                for item_id in user_tree.get_children():
                    user_tree.insert(item_id, "end", values=("Edit",), tags=("button",))
                ####################################################################################################3
                label1 = tk.Label(self.settings_window, text="Your Payment History")
                label1.place(x=400,y=50)
                # Create a table to display past payment information
                # Create a table to display past payment information
                self.payment_tree = ttk.Treeview(self.settings_window, columns=("U_ID", "A_ID", "Price", "Method_Of_Payment", "Status"), show="headings")

                # Set the headings to match the column names
                self.payment_tree.heading("U_ID", text="U_ID")
                self.payment_tree.heading("A_ID", text="A_ID")
                self.payment_tree.heading("Price", text="Price")
                self.payment_tree.heading("Method_Of_Payment", text="Method of Payment")
                self.payment_tree.heading("Status", text="Status")
                self.payment_tree.column("U_ID",width=50)
                self.payment_tree.column("A_ID",width=50)
                self.payment_tree.column("Price",width=50)
                self.payment_tree.column("Method_Of_Payment",width=50)
                self.payment_tree.column("Status",width=50)

                # Pack the Treeview widget
                self.payment_tree.place(x=450,y=100)

                #connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                #cursor = connection.cursor()
                cursor.execute("SELECT * FROM payment_history WHERE U_ID = %s", (user_data[0],))
                payments = cursor.fetchall()
                for payment in payments:
                    self.payment_tree.insert("", "end", values=payment)
                #connection.commit()
                #connection.close()
                ##########################################################################################################
                label2 = tk.Label(self.settings_window, text="Your Past Appointments")
                label2.place(x=50,y=350)
                # Create a table to display past payment information
                # Create a table to display past payment information
                self.appt_tree = ttk.Treeview(self.settings_window, columns=("Doctor Name","Date", "Start_time", "End_time","Mode","Location","Status"), show="headings")
                self.appt_tree["height"]=10
                # Set the headings to match the column names
                self.appt_tree.heading("Doctor Name", text="Doctor Name")
                self.appt_tree.heading("Date", text="Date")
                self.appt_tree.heading("Start_time", text="Start_time")
                self.appt_tree.heading("End_time", text="End_time")
                self.appt_tree.heading("Mode", text="Mode")
                self.appt_tree.heading("Location", text="Location")
                self.appt_tree.heading("Status", text="Status")
                self.appt_tree.column("Doctor Name", width=50)
                self.appt_tree.column("Date", width=100)
                self.appt_tree.column("Start_time", width=100)
                self.appt_tree.column("End_time", width=100)
                self.appt_tree.column("Mode", width=100)
                self.appt_tree.column("Location", width=100)
                self.appt_tree.column("Status", width=100)
                self.appt_tree.place(x=50,y=400)
                #connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                #cursor = connection.cursor()
                cursor.execute("SELECT m.first_name, A.Date, A.Start_time, A.End_time, A.Mode, A.Location, A.Status FROM appointment A JOIN mhp M ON A.M_ID = M.m_id WHERE (A.Status = 'completed' OR A.Status = 'cancelled') AND A.U_ID = %s",
                                (user_data[0],))

                appts= cursor.fetchall()
                for a in appts:
                    self.appt_tree.insert("", "end", values=a)
               
                ###############################################################################################################33
                label3 = tk.Label(self.settings_window, text="Your Upcoming Appointments")
                label3.place(x=800,y=350)
                appt_tree1 = ttk.Treeview(self.settings_window, columns=("Doctor Name", "Date", "Start_time", "End_time","Mode","Location","Status"), show="headings",height=10)
                appt_tree1["height"]=10
                appt_tree1.heading("Doctor Name", text="Doctor Name")
                appt_tree1.heading("Date", text="Date")
                appt_tree1.heading("Start_time", text="Start_time")
                appt_tree1.heading("End_time", text="End_time")
                appt_tree1.heading("Mode", text="Mode")
                appt_tree1.heading("Location", text="Location")
                appt_tree1.heading("Status", text="Status")
                appt_tree1.column("Doctor Name", width=50)
                appt_tree1.column("Date", width=100)
                appt_tree1.column("Start_time", width=100)
                appt_tree1.column("End_time", width=100)
                appt_tree1.column("Mode", width=100)
                appt_tree1.column("Location", width=100)
                appt_tree1.column("Status", width=100)
                appt_tree1.place(x=800,y=400)
                cursor.execute("SELECT m.first_name, A.Date, A.Start_time, A.End_time, A.Mode, A.Location, A.Status FROM appointment A JOIN mhp M ON A.M_ID = M.m_id WHERE A.Status = 'upcoming' AND A.U_ID = %s", (user_data[0],))
                appts= cursor.fetchall()
                def check_appointments(appointment_date):
                        print("inside func")
                        while True:  # Adjust this loop to check periodically
                            current_date = datetime.date.today()
                            days_until_appointment = (appointment_date - current_date).days
                            print("days_until_appointment",days_until_appointment)
                            if days_until_appointment <= 1:
                                print("helllo,less than a day")
                                messagebox.showinfo("Upcoming Appointment", "Your appointment is less than 1 day away!")
                            time.sleep(1000)
                for a in appts:
                    appt_tree1.insert("", "end", values=a)
                    appointment_date_str = a[1].strftime("%Y-%m-%d")
                    appointment_date = datetime.datetime.strptime(appointment_date_str, "%Y-%m-%d").date()
                    appointment_thread = threading.Thread(target=check_appointments, args=(appointment_date,))
                    appointment_thread.daemon = True
                    appointment_thread.start()

                

                
                """appointment_thread = threading.Thread(target=check_appointments)
                appointment_thread.daemon = True 
                appointment_thread.start()"""
                tk.Button(self.settings_window,
                    text='Cancel Appointment', 
                    command=lambda: self.cancel_appointment(appt_tree1), 
                    ).place(x=900,y=500)
                
                ####################################################################################################################################################33
                label4 = tk.Label(self.settings_window, text="Your Reviews")
                label4.place(x=800, y=50)
                cursor.execute("SELECT m.first_name,r.Date,r.Title,r.Comment,r.Rating from review r join mhp m on r.m_id=m.m_id WHERE r.U_ID = %s order by r.date", (user_data[0],))
                reviews = cursor.fetchall()
                review_tree = ttk.Treeview(self.settings_window, columns=("Doctor Name", "Date","Title","Comment","Rating"), show="headings")
                review_tree.heading("Doctor Name", text="Doctor Name")
                review_tree.heading("Date", text="Date")
                review_tree.heading("Title", text="Title")
                review_tree.heading("Comment", text="Comment")
                review_tree.heading("Rating", text="Rating")
                review_tree.column("Doctor Name", width=100)
                review_tree.column("Date", width=100)
                review_tree.column("Title", width=100)
                review_tree.column("Comment", width=150)
                review_tree.column("Rating", width=100)
                review_tree.place(x=800, y=100)
                style = ttk.Style()
                #sb = Scrollbar(frame, orient=VERTICAL)
                #sb.pack(side=RIGHT, fill=Y)
                #review_tree.config(yscrollcommand=sb.set)
                #sb.config(command=tv.yview)
                #scrollbar = Scrollbar(self.settings_window, orient="vertical", command=review_tree.yview)
                #scrollbar.place(x=950, y=100, height=200)  
                #review_tree.configure(yscrollcommand=scrollbar.set)
                for review in reviews:
                        #print(reviews)
                        #print("doctor_id",reviews[0][0])
                        review_tree.insert("", "end", values=review)
                    
                tk.Button(self.settings_window,text='Update Review', command=lambda: self.edit_selected_review(review_tree),).place(x=900,y=200)
                tk.Button(self.settings_window,text='Add Review', command=lambda: self.add_review(review_tree),).place(x=1000,y=200)
                tk.Button(self.settings_window,text='Delete Review', command=lambda: self.delete_review(review_tree),).place(x=1100,y=200)
                style.theme_use("default")
                style.map("Treeview")
                connection.commit()
                connection.close()
              
                ####################################################################################################################################################33
                """label5 = tk.Label(self.settings_window, text="Your Pending Prescriptions")
                label5.place(x=50,y=800)
                # Create a table to display past payment information
                # Create a table to display past payment information
                pres = ttk.Treeview(self.settings_window, columns=("A_ID", "Medication Name", "Start Date", "End Date", "Intake time","Frequency","Additional Comments"), show="headings")

                # Set the headings to match the column names
                pres.heading("A_ID", text="A_ID")
                pres.heading("Medication Name", text="Medication Name")
                pres.heading("Start Date", text="Start Date")
                pres.heading("End Date", text="End Date")
                pres.heading("Intake time", text="Intake time")
                pres.heading("Frequency", text="Frequency")
                pres.heading("Additional Comments", text="Additional Comments")
                pres.column("A_ID", width=50)
                pres.column("Medication Name", width=50)
                pres.column("Start Date", width=100)
                pres.column("End Date", width=100)
                pres.column("Intake time", width=100)
                pres.column("Frequency", width=100)
                pres.column("Additional Comments", width=200)
                pres.place(x=800,y=600)
# Fetch and display past payment data from the database
                #connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                #cursor = connection.cursor()
                current_datetime = datetime.datetime.now()
                current_date = current_datetime.date()

                query = WITH UserAppointment AS (
                    SELECT ap.A_ID
                    FROM appointment ap
                    WHERE ap.U_ID = %s
                )
                SELECT ph.A_ID, m.med_name, ph.start_date, ph.end_date, ph.intake_time, ph.frequency, ph.additional_instructions
                FROM prescription_history ph
                JOIN UserAppointment ua ON ph.A_ID = ua.A_ID
                JOIN medicine m ON ph.med_id = m.med_id
                WHERE %s BETWEEN ph.start_date AND ph.end_date;
                
                #cursor.execute(query, (user_data[0],))
                cursor.execute(query, (user_data[0], current_date))
                appts= cursor.fetchall()
                for a in appts:
                    pres.insert("", "end", values=a)
                connection.commit()
                connection.close()
            else:
                print("User not found")
        else:
            print("No user is logged in")"""
    def show_pending_prescriptions(self):
        # Create a new window to display pending prescriptions
        #prescription_window = tk.Toplevel(self.settings_window)  # Use 'self.settings_window' as the parent
        #prescription_window.title("Prescriptions")
        prescription_window = tk.Toplevel(self.settings_window)
        prescription_window.title("Pending Prescriptions")

        # Create a Treeview widget to display prescription details
        pres = ttk.Treeview(prescription_window, columns=("A_ID", "Medication Name", "Start Date", "End Date", "Intake time", "Frequency", "Additional Comments"), show="headings")

        # Set the headings to match the column names
        pres.heading("A_ID", text="A_ID")
        pres.heading("Medication Name", text="Medication Name")
        pres.heading("Start Date", text="Start Date")
        pres.heading("End Date", text="End Date")
        pres.heading("Intake time", text="Intake time")
        pres.heading("Frequency", text="Frequency")
        pres.heading("Additional Comments", text="Additional Comments")

        # Set column widths
        pres.column("A_ID", width=50)
        pres.column("Medication Name", width=100)
        pres.column("Start Date", width=100)
        pres.column("End Date", width=100)
        pres.column("Intake time", width=100)
        pres.column("Frequency", width=100)
        pres.column("Additional Comments", width=200)

        pres.pack()

        # Fetch and display pending prescription data
        current_datetime = datetime.datetime.now()
        current_date = current_datetime.date()

        query = """WITH UserAppointment AS (
            SELECT ap.A_ID
            FROM appointment ap
            WHERE ap.U_ID = %s
        )
        SELECT ph.A_ID, ph.med_name, ph.start_date, ph.end_date, ph.intake_time, ph.frequency, ph.additional_instructions
        FROM prescription_history ph
        JOIN UserAppointment ua ON ph.A_ID = ua.A_ID
        WHERE %s BETWEEN ph.start_date AND ph.end_date;
        """
        #JOIN medicine m ON ph.med_name = m.med_name
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cursor = connection.cursor()
        cursor.execute(query, (self.userid, current_date))
        appts = cursor.fetchall()

        for a in appts:
            pres.insert("", "end", values=a)
        connection.commit()
        connection.close()

    def show_all_prescriptions(self):
        # Create a new window to display pending prescriptions
        #prescription_window = tk.Toplevel(self.settings_window)  # Use 'self.settings_window' as the parent
        #prescription_window.title("Prescriptions")
        prescription_window1 = tk.Toplevel(self.settings_window)
        prescription_window1.title("Pending Prescriptions")

        # Create a Treeview widget to display prescription details
        pres1 = ttk.Treeview(prescription_window1, columns=("A_ID", "Medication Name", "Start Date", "End Date", "Intake time", "Frequency", "Additional Comments"), show="headings")

        # Set the headings to match the column names
        pres1.heading("A_ID", text="A_ID")
        pres1.heading("Medication Name", text="Medication Name")
        pres1.heading("Start Date", text="Start Date")
        pres1.heading("End Date", text="End Date")
        pres1.heading("Intake time", text="Intake time")
        pres1.heading("Frequency", text="Frequency")
        pres1.heading("Additional Comments", text="Additional Comments")

        # Set column widths
        pres1.column("A_ID", width=50)
        pres1.column("Medication Name", width=100)
        pres1.column("Start Date", width=100)
        pres1.column("End Date", width=100)
        pres1.column("Intake time", width=100)
        pres1.column("Frequency", width=100)
        pres1.column("Additional Comments", width=200)

        pres1.pack()

        # Fetch and display pending prescription data
        #current_datetime = datetime.datetime.now()
        #current_date = current_datetime.date()

        query = """WITH UserAppointment AS (
            SELECT ap.A_ID
            FROM appointment ap
            WHERE ap.U_ID = %s
        )
        SELECT ph.A_ID, ph.med_name, ph.start_date, ph.end_date, ph.intake_time, ph.frequency, ph.additional_instructions
        FROM prescription_history ph
        JOIN UserAppointment ua ON ph.A_ID = ua.A_ID
        """
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cursor = connection.cursor()
        cursor.execute(query, (self.userid,))
        appts = cursor.fetchall()

        for a in appts:
            pres1.insert("", "end", values=a)
        connection.commit()
        connection.close()

    # Create a button to open the Pending Prescriptions window
    


    def update_review_tree(self, review_tree):
        review_tree.delete(*review_tree.get_children())
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cursor = connection.cursor()
        cursor.execute("SELECT m.first_name,r.Date,r.Title,r.Comment,r.Rating from review r join mhp m on r.m_id=m.m_id WHERE r.U_ID = %s order by r.date", (self.userid,))
        reviews = cursor.fetchall()
        print(reviews)
        review_tree = ttk.Treeview(self.settings_window, columns=("Doctor Name", "Date","Title","Comment","Rating"), show="headings")
        review_tree.heading("Doctor Name", text="Doctor Name")
        review_tree.heading("Date", text="Date")
        review_tree.heading("Title", text="Title")
        review_tree.heading("Comment", text="Comment")
        review_tree.heading("Rating", text="Rating")
        review_tree.column("Doctor Name", width=100)
        review_tree.column("Date", width=100)
        review_tree.column("Title", width=100)
        review_tree.column("Comment", width=100)
        review_tree.column("Rating", width=150)
        review_tree.place(x=800, y=100)
        for review in reviews:
                        review_tree.insert("", "end", values=review)
        tk.Button(self.settings_window,text='Update Review', command=lambda: self.edit_selected_review(review_tree),).place(x=900,y=200)
        tk.Button(self.settings_window,text='Add Review', command=lambda: self.add_review(review_tree),).place(x=1000,y=200)
        tk.Button(self.settings_window,text='Delete Review', command=lambda: self.delete_review(review_tree),).place(x=1100,y=200)
               
        style = ttk.Style()
        style.theme_use("default")
        style.map("Treeview")

    def update_appt_tree1(self, appt_tree1):
        print("entered appt_tree")
        appt_tree1.delete(*appt_tree1.get_children())
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cursor = connection.cursor()
        appt_tree1 = ttk.Treeview(self.settings_window, columns=("Doctor Name", "Date", "Start_time", "End_time","Mode","Location","Status"), show="headings",height=10)
        appt_tree1["height"]=10
        appt_tree1.heading("Doctor Name", text="Doctor Name")
        appt_tree1.heading("Date", text="Date")
        appt_tree1.heading("Start_time", text="Start_time")
        appt_tree1.heading("End_time", text="End_time")
        appt_tree1.heading("Mode", text="Mode")
        appt_tree1.heading("Location", text="Location")
        appt_tree1.heading("Status", text="Status")
        appt_tree1.column("Doctor Name", width=50)
        appt_tree1.column("Date", width=100)
        appt_tree1.column("Start_time", width=100)
        appt_tree1.column("End_time", width=100)
        appt_tree1.column("Mode", width=100)
        appt_tree1.column("Location", width=100)
        appt_tree1.column("Status", width=100)
        appt_tree1.place(x=800,y=400)
        cursor.execute("SELECT m.first_name, A.Date, A.Start_time, A.End_time, A.Mode, A.Location, A.Status FROM appointment A JOIN mhp M ON A.M_ID = M.m_id WHERE A.Status = 'upcoming' AND A.U_ID = %s", (self.userid,))
        appts= cursor.fetchall()
        for a in appts:
            appt_tree1.insert("", "end", values=a)
        tk.Button(self.settings_window,
            text='Cancel Appointment', 
            command=lambda: self.cancel_appointment(appt_tree1), 
            ).place(x=900,y=500)

        connection.commit()
        connection.close()
        self.update_appt_tree()
        self.update_payment()

    def update_appt_tree(self):
        print("entered appt_tree")
        self.appt_tree.delete(*self.appt_tree.get_children())
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cursor = connection.cursor()
        self.appt_tree = ttk.Treeview(self.settings_window, columns=("Doctor Name","Date", "Start_time", "End_time","Mode","Location","Status"), show="headings")
        self.appt_tree["height"]=10
        # Set the headings to match the column names
        self.appt_tree.heading("Doctor Name", text="Doctor Name")
        self.appt_tree.heading("Date", text="Date")
        self.appt_tree.heading("Start_time", text="Start_time")
        self.appt_tree.heading("End_time", text="End_time")
        self.appt_tree.heading("Mode", text="Mode")
        self.appt_tree.heading("Location", text="Location")
        self.appt_tree.heading("Status", text="Status")
        self.appt_tree.column("Doctor Name", width=50)
        self.appt_tree.column("Date", width=100)
        self.appt_tree.column("Start_time", width=100)
        self.appt_tree.column("End_time", width=100)
        self.appt_tree.column("Mode", width=100)
        self.appt_tree.column("Location", width=100)
        self.appt_tree.column("Status", width=100)
        self.appt_tree.place(x=50,y=400)
        cursor.execute("SELECT m.first_name, A.Date, A.Start_time, A.End_time, A.Mode, A.Location, A.Status FROM appointment A JOIN mhp M ON A.M_ID = M.m_id WHERE (A.Status = 'completed' OR A.Status = 'cancelled') AND A.U_ID = %s",
                        (self.userid,))

        appts= cursor.fetchall()
        for a in appts:
            self.appt_tree.insert("", "end", values=a)
        connection.commit()
        connection.close()
        
    def update_payment(self):
        print("entered payment")
        self.payment_tree.delete(*self.payment_tree.get_children())
        self.payment_tree = ttk.Treeview(self.settings_window, columns=("U_ID", "A_ID", "Price", "Method_Of_Payment", "Status"), show="headings")
        self.payment_tree.heading("U_ID", text="U_ID")
        self.payment_tree.heading("A_ID", text="A_ID")
        self.payment_tree.heading("Price", text="Price")
        self.payment_tree.heading("Method_Of_Payment", text="Method of Payment")
        self.payment_tree.heading("Status", text="Status")
        self.payment_tree.column("U_ID",width=50)
        self.payment_tree.column("A_ID",width=50)
        self.payment_tree.column("Price",width=50)
        self.payment_tree.column("Method_Of_Payment",width=50)
        self.payment_tree.column("Status",width=50)

        # Pack the Treeview widget
        self.payment_tree.place(x=450,y=100)

        #connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        #cursor = connection.cursor()
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM payment_history WHERE U_ID = %s", (self.userid,))
        payments = cursor.fetchall()
        for payment in payments:
            self.payment_tree.insert("", "end", values=payment)
    
        connection.commit()
        connection.close()
    def update_user_tree(self, user_tree):
        user_tree.delete(*user_tree.get_children())
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE Username = %s", (self.username,))
        user_data = cursor.fetchone()

        labels = [
            ("User ID", user_data[0]),
            ("Username", user_data[1]),
            ("Password", user_data[2]),
            ("First Name", user_data[3]),
            ("Last Name", user_data[4]),
            ("Date of Birth", user_data[5]),
            ("Age", user_data[6]),
            ("Date of Joining", user_data[7]),
            ("Phone Number", user_data[8]),
            ("Email", user_data[9]),
            ("Address", user_data[10]),
            ("Sex", user_data[11])
        ]

        for label, value in labels:
            user_tree.insert("", "end", values=(label, value))

        connection.commit()
        connection.close()

        # Tag and bind the "Edit" button
        user_tree.tag_configure("button", foreground="blue",)
        user_tree.tag_bind("button", "<Button-1>", lambda event, tree=user_tree: self.edit_selected_user(user_tree))
        for item_id in user_tree.get_children():
            user_tree.insert(item_id, "end", values=("Edit",), tags=("button",))
        """ Add this code after the "Edit" button code
        user_tree.tag_configure("delete_button", foreground="red")  # Configure the tag for the delete button
        user_tree.tag_bind("delete_button", "<Button-1>", lambda event, tree=user_tree: self.delete_selected_user(user_tree))

        for item_id in user_tree.get_children():
            user_tree.insert(item_id, "end", values=("Edit", "Delete"), tags=("button", "delete_button"))"""
#self.root.mainloop()

if __name__ == "__main__":
    # Create the main tkinter window
    root = tk.Tk()
    #root.geometry("400x400")
    U_NAME=sys.argv[1]
    #U_NAME="user10"
    #print("practice.py",U_NAME)
    if U_NAME is not None:
        U_NAME=str(U_NAME)
        print("str practice.py",U_NAME)
    #U_NAME="chaitra"
    # Create a "Settings" button to display user details
    user_settings = UserSettingsPage(U_NAME)
    #user_settings.mainloop()
    #settings_button = tk.Button(root, text="Settings", command=user_settings.display_user_data)
    #settings_button.pack()

    # Run the tkinter main loop
    root.mainloop()
   
