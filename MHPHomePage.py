import tkinter as tk
import subprocess
import sys
import mysql.connector
import datetime
from tkinter import messagebox
import inspect
import credentials as cr
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage
#CORRELATED/NESTED FUNCTION FRO UPCOMING APPOINTMNENTS MODE
#from PIL import Image, ImageTk

class MHPHomePage(tk.Tk):
    def __init__(self,M_id,file):
        super().__init__()
        self.title("TheraConnect-MHP Home Page!")
        self.geometry("900x600")
        #self.geometry("1700x800")
        #self.eval('tk::PlaceWindow . center')
        self.bg_img = ImageTk.PhotoImage(file="mhp1.png")
        background = Label(self,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)
        
        self.header_label = tk.Label(self, text="Home Page", font=("Verdana", 16))
        self.header_label.place(relx=0.5, rely=0.01, anchor="n",)
        
        #SETTINGS BUTTON
        self.settings_button = tk.Button(self, text="Settings", font=("Verdana", 12),command=self.go_to_settings)
        self.settings_button.place(relx=0.9, rely=0.01, anchor="n")

        #Reset Schedule every time you login
        if file in ["MHPLogin.py"]:
            self.reset_schedule() 
        else:
            print(file)

        #FRAME FOR UPCOMING APPOINTMENTS
        self.frame1 = tk.Frame(self, bg="white", bd=4)
        self.frame1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.35)
        self.label1 = tk.Label(self.frame1, text="Upcoming Appointments", bg="white", anchor="w", font=("Verdana", 10))
        self.label1.grid(row=0, column=0, padx=5, pady=5, columnspan=3,sticky="nw")
        
        #CANVAS FOR UPCOMING REQUESTS
        self.canvas1 = tk.Canvas(self.frame1,width=660,height=160)
        self.canvas1.grid(row=1, column=0)

        self.upcoming_appointments()
        
        
        #FRAME FOR PENDING REQUESTS
        self.frame2 = tk.Frame(self, bg="white", bd=4)
        self.frame2.place(relx=0.1, rely=0.47, relwidth=0.8, relheight=0.35)
        self.label2 = tk.Label(self.frame2, text="Pending Appointment Requests", bg="white", font=("Verdana", 10))
        self.label2.grid(row=0, column=0, padx=5, pady=5, columnspan=3,sticky="nw")
        
        #CANVAS FOR PENDING REQUESTS
        self.canvas2 = tk.Canvas(self.frame2,width=660,height=160)
        self.canvas2.grid(row=1, column=0)
  
        self.pending_appointments()
        
        
        #FRAME FOR VIEWING APPOINTMENTS, SCHEDULE AND REVIEWS
        self.frame3 = tk.Frame(self, bg="white", bd=4)
        self.frame3.place(relx=0.1, rely=0.84, relwidth=0.8, relheight=0.1)
        
        self.past_button = tk.Button(self.frame3, text="View Past Appointments", font=("Verdana", 12),command=self.past_appointments)
        self.past_button.grid(row=0, column=0, padx=20, pady=5, sticky="w")
        
        self.schedule_button = tk.Button(self.frame3, text="Manage your Schedule", font=("Verdana", 12),command=self.schedule)
        self.schedule_button.grid(row=0, column=1, padx=(45,20), pady=5)
        
        self.review_button = tk.Button(self.frame3, text="View Reviews", font=("Verdana", 12),command=self.reviews)
        self.review_button.grid(row=0, column=2, padx=(50,20), pady=5, sticky="e")
        
    def reset_schedule(self):
        print("yes")
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        
        #CHECK CURRENT DATE
        start_date = datetime.date.today()
        start_day = start_date.strftime("%A")
        print("Start:",start_date,start_day)
        
        #DELETE FROM SCHEDULE WHERE DATE IS BEFORE CURRENT DATE
        query1="""DELETE FROM schedule
                    WHERE M_id = %s
                      AND Date < %s
                    """
        cur.execute(query1,(str(M_id),str(start_date)))
        connection.commit()
        connection.close()
        
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        
        #COUNT NO. OF ENTRIES THAT EXIST
        query2="SELECT COUNT(DISTINCT DATE) FROM Schedule WHERE M_id = %s"
        cur.execute(query2,(str(M_id),))
        result=cur.fetchone()
        no_of_entries=result[0]
        print(no_of_entries)
        
        if no_of_entries<5:
            new_start_date = start_date + datetime.timedelta(days=no_of_entries)
            new_start_day = new_start_date.strftime("%A")
            print("New Start: ",new_start_date,new_start_day)       
            i=no_of_entries
            while (i<5):
                if new_start_day not in ["Sunday","Saturday"]:
                    query3 = "INSERT INTO Schedule VALUES (%s,%s,%s,0,0,0,0,0,0,0,0)"
                    cur.execute(query3, (str(M_id),str(new_start_day), str(new_start_date)))
                    print("Added values:", new_start_date,new_start_day)
                    i+=1
                new_start_date += datetime.timedelta(days=1)
                new_start_day = new_start_date.strftime("%A")
            
        connection.commit()
        connection.close()
        
        
    def upcoming_appointments(self):
            scrollbar = tk.Scrollbar(self.frame1, orient="vertical", command=self.canvas1.yview)
            scrollbar.grid(row=1, column=1, sticky="ns")
            self.inner_frame1 = tk.Frame(self.canvas1,height=160)
            self.canvas1.create_window((0, 0), window=self.inner_frame1, anchor="nw")
            connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cur = connection.cursor()
            query= "SELECT * FROM Appointment WHERE M_id = %s AND status = 'Upcoming'"
            cur.execute(query, (str(M_id),))
            result = cur.fetchall()
            connection.commit()
            connection.close()
            if result:
                label = tk.Label(self.inner_frame1, text="Date\t\tStart Time\tEnd Time\t\tMode\tLocation",font=("Verdana", 10))
                label.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="w")
                row_no=2
                for row in result:
                    label = tk.Label(self.inner_frame1, text=f"{row[3]}\t{row[4]}\t\t{row[5]}\t\t{row[6]}\t{row[7]}", bg="white",font=("Verdana", 10))
                    label.grid(row=row_no, column=0, padx=5, pady=5, columnspan=3, sticky="w")
                    button = tk.Button(self.inner_frame1,text="Details",font=("Verdana",10),command=lambda A_id=row[0]: self.details(A_id))
                    button.grid(row=row_no, column=10, padx=5, pady=5, columnspan=3, sticky="w")
                    row_no+=1    
            else:
                no_appointments_label = tk.Label(self.inner_frame1, text="No upcoming appointments!", font=("Verdana", 10))
                no_appointments_label.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="w")
            
                 
    def pending_appointments(self):
            scrollbar = tk.Scrollbar(self.frame2, orient="vertical", command=self.canvas2.yview)
            scrollbar.grid(row=1, column=1, sticky="ns")
            self.inner_frame2 = tk.Frame(self.canvas2,height=160)
            self.canvas2.create_window((0, 0), window=self.inner_frame2, anchor="nw")
            connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cur = connection.cursor()
            query= "SELECT * FROM Appointment WHERE M_id = %s AND status = 'Pending'"
            cur.execute(query, (str(M_id),))
            result = cur.fetchall()
            connection.close()
            if result:
                label = tk.Label(self.inner_frame2, text="Date\t\tStart Time\tEnd Time\t\tMode\tLocation",font=("Verdana", 10))
                label.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="w")
                row_no=2
                for row in result:
                    label = tk.Label(self.inner_frame2, text=f"{row[3]}\t{row[4]}\t\t{row[5]}\t\t{row[6]}\t{row[7]}", bg="white",font=("Verdana", 10))
                    label.grid(row=row_no, column=0, padx=5, pady=5, columnspan=3, sticky="w")
                    button = tk.Button(self.inner_frame2,text="Approve",font=("Verdana",10),command=lambda A_id=row[0]: self.approve(A_id))
                    button.grid(row=row_no, column=10, padx=5, pady=5, columnspan=3, sticky="w")
                    row_no+=1           
            else:
                no_appointments_label = tk.Label(self.inner_frame2, text="No pending appointments!", font=("Verdana", 10))
                no_appointments_label.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="w")
            

    
                 
    def approve(self,A_id):
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        query1= "UPDATE Appointment SET status = 'Upcoming' WHERE A_id = %s"
        cur.execute(query1, (str(A_id),))
        # Fetch Date, start_time, and end_time from the database
        query2 = "SELECT Date, Start_Time, End_Time FROM Appointment WHERE A_id = %s"
        cur.execute(query2, (str(A_id),))
        result = cur.fetchone()
        Date = result[0]
        start_time = result[1]
        end_time = result[2]
        
        # Define the time slot names and the mapping between time slots and their corresponding time ranges
        time_slot_names = ["9_10AM", "10_11AM", "11_12AM", "12_1PM", "1_2PM", "2_3PM", "3_4PM", "4_5PM"]
        
        slot_to_time_range = {
            "9_10AM": (datetime.time(9, 0), datetime.time(10, 0)),
            "10_11AM": (datetime.time(10, 0), datetime.time(11, 0)),
            "11_12AM": (datetime.time(11, 0), datetime.time(12, 0)),
            "12_1PM": (datetime.time(12, 0), datetime.time(13, 0)),
            "1_2PM": (datetime.time(13, 0), datetime.time(14, 0)),
            "2_3PM": (datetime.time(14, 0), datetime.time(15, 0)),
            "3_4PM": (datetime.time(15, 0), datetime.time(16, 0)),
            "4_5PM": (datetime.time(16, 0), datetime.time(17, 0)),
        }
        
        # Convert start_time and end_time to datetime.timedelta objects
        start_time_timedelta = start_time.total_seconds() // 3600  # Convert to hours
        end_time_timedelta = end_time.total_seconds() // 3600  # Convert to hours
        
        
        # Iterate through time slots and update the Schedule table
        for slot_name, (slot_start, slot_end) in slot_to_time_range.items():
            slot_start_timedelta = slot_start.hour + slot_start.minute // 60
            slot_end_timedelta = slot_end.hour + slot_end.minute // 60
        
            if start_time_timedelta <= slot_start_timedelta and end_time_timedelta >= slot_end_timedelta:
                query = f"UPDATE Schedule SET {slot_name} = 1 WHERE M_id = %s AND Date = %s"
                cur.execute(query, (M_id, Date))
        
        connection.commit()
        connection.close()

        self.canvas1.delete("all")
        self.canvas2.delete("all")
        
        self.pending_appointments()
        self.upcoming_appointments()

    def details(self,A_id):
        A_id=str(A_id)
        subprocess.Popen(["python", "MHPAppDetails.py", M_id,A_id])  
        self.destroy()    
    
    def schedule(self):
        subprocess.Popen(["python", "MHPSchedule.py", M_id])  
        self.destroy()
    
    def reviews(self):
        subprocess.Popen(["python", "MHPReviews.py", M_id])  
        self.destroy()
    
    def past_appointments(self):
        subprocess.Popen(["python", "MHPPastAppointment.py", M_id])  
        self.destroy()
        
    def go_to_settings(self):
        subprocess.Popen(["python", "MHPSettings.py", M_id])  
        self.destroy()
        
if __name__=="__main__":
    file=sys.argv[0] if len(sys.argv) > 1 else None
    M_id = sys.argv[1] if len(sys.argv) > 1 else None
    print(sys.argv[0],sys.argv[1])
    if M_id is not None:
        M_id = str(M_id)
    file=str(file)
    # M_id="1"
    # file="MHPSpeciality.py"
    app=MHPHomePage(M_id,file)
    app.mainloop()
    