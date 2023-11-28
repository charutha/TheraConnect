import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import sys
import mysql.connector
import credentials as cr
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage
class MHPAppDetails(tk.Tk):
    def __init__(self, M_id, A_id):
        super().__init__()
        self.title("TheraConnect-MHP Appointment Details")
        self.geometry("900x600")
        self.bg_img = ImageTk.PhotoImage(file="mhp1.png")
        background = Label(self,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)
        #self.eval('tk::PlaceWindow . center')
        self.header_label = tk.Label(self, text="Appointment Details", font=("Verdana", 16))
        self.header_label.place(relx=0.5, rely=0.01, anchor="n")
        self.back_button = tk.Button(self, text="<- Back", font=("Verdana", 10),command=self.go_to_past_page)
        self.back_button.place(relx=0.1, rely=0.02, anchor="n")
        
        
        #FRAMES
        self.frame1 = tk.Frame(self, bg="white", bd=4)
        self.frame1.place(relx=0.05, rely=0.1, relwidth=0.45, relheight=0.4)
        self.frame2 = tk.Frame(self, bg="white", bd=4)
        self.frame2.place(relx=0.55, rely=0.55, relwidth=0.4, relheight=0.4)
        self.frame3 = tk.Frame(self, bg="white", bd=4)
        self.frame3.place(relx=0.05, rely=0.55, relwidth=0.45, relheight=0.4)
        self.frame4 = tk.Frame(self, bg="white", bd=4)
        self.frame4.place(relx=0.55, rely=0.1, relwidth=0.4, relheight=0.4)
        
        self.subframe3 = tk.Frame(self.frame3, bg="white", bd=4)
        self.subframe3.place(relx=0.05, rely=0.55, relwidth=0.2, relheight=0.2)
        
        #LABELS
        self.label1 = tk.Label(self.frame1, text="Appointment Details", bg="white", anchor="w", font=("Verdana", 10))
        self.label1.grid(row=0, column=0, padx=5, pady=5, columnspan=3,sticky="nw")
        self.label2 = tk.Label(self.frame2, text="Add a new Medicine", bg="white", anchor="w", font=("Verdana", 10))
        self.label2.grid(row=0, column=0, padx=5, pady=5, columnspan=3,sticky="nw")
        self.label3 = tk.Label(self.frame3, text="Prescription", bg="white", anchor="w", font=("Verdana", 10))
        self.label3.grid(row=0, column=0, padx=5, pady=5, columnspan=3,sticky="nw")
        self.label4 = tk.Label(self.frame4, text="Payment Status", bg="white", anchor="w", font=("Verdana", 10))
        self.label4.grid(row=0, column=0, padx=5, pady=5, columnspan=3,sticky="nw")
        self.appointment_details()
        
    def appointment_details(self):
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        
        
        #FRAME 1: APPOINTMENT DETAILS
        query="CALL GetCustomAppointmentView(%s)"
        cur.execute(query,(str(A_id),))
        subquery="SELECT * FROM CustomAppointmentView"
        cur.execute(subquery)
        result=cur.fetchone()
        if result:
            #COLUMN 1
            label1 = tk.Label(self.frame1, text="Username\tFirst Name\tLast Name\t",font=("Verdana", 10))
            label1.grid(row=1, column=0, padx=2, pady=5, columnspan=3, sticky="w")
            label1_res = tk.Label(self.frame1, text = f"{result[0]}\t\t{result[1]}\t\t{result[2]}", bg="white",font=("Verdana", 10))
            label1_res.grid(row=2, column=0, padx=2, pady=5, columnspan=3, sticky="w")
            
            label2 = tk.Label(self.frame1, text="Age\tPhone\t\tEmail\t\tSex\t",font=("Verdana", 10))
            label2.grid(row=3, column=0, padx=2, pady=5, columnspan=3, sticky="w")
            label2_res = tk.Label(self.frame1, text = f"{result[3]}\t{result[4]}\t{result[5]}\t{result[6]}", bg="white",font=("Verdana", 10))
            label2_res.grid(row=4, column=0, padx=2, pady=5, columnspan=3, sticky="w")
            
            label3 = tk.Label(self.frame1, text="Date\t     From\t    To\t\tMode\tLocation  ",font=("Verdana", 10))
            label3.grid(row=5, column=0, padx=2, pady=5, columnspan=3, sticky="w")
            label3_res = tk.Label(self.frame1, text = f"{result[7]}  {result[8]}  {result[9]}\t{result[10]}\t{result[11]}", bg="white",font=("Verdana", 10))
            label3_res.grid(row=6, column=0, padx=2, pady=5, columnspan=3, sticky="w")
        else:
            no_appointments_label = tk.Label(self.frame1, text="This user/appointment does not exist :(", font=("Verdana", 10))
            no_appointments_label.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="w")
        
        
        #FRAME 2: FOLLOW UP
        query="SELECT Status FROM Appointment WHERE A_id=%s"
        cur.execute(query,(str(A_id),))
        result=cur.fetchone()
         
        #FRAME 2: ADD MEDICINE
        query = "SELECT Med_name FROM Medicine"
        cur.execute(query)
        med_names = cur.fetchall()
        connection.close()
        options = [med_name[0] for med_name in med_names]
        print(options)

        #FRAME 2: ADD A MED
        self.new_med_label = tk.Label(self.frame2,text="Medicine Name:",bg="white")
        self.new_med_label.grid(row=1, column=0)
        self.new_med_entry = tk.Entry(self.frame2,fg="black",width=20)
        self.new_med_entry.grid(row=1, column=1)
        add_button = tk.Button(self.frame2, text="Add", command=self.add_med, font=("Verdana", 10))
        add_button.place(relx=0.05, rely=0.85, relwidth=0.4, relheight=0.1)

        
        if result[0]=='Upcoming':
            #FRAME 3: PRESCRIPTION
            #options = ["Med1", "Med2", "Med3", "Med4","Med5"]
            label1 = tk.Label(self.frame3, text="Choose a Medicine",font=("Verdana", 10))
            label1.grid(row=1, column=0, padx=2, pady=5, columnspan=3, sticky="w")
            self.med_entry = [str(med) for med in options]
            self.med_entry= ttk.Combobox(self.frame3, values=self.med_entry, width=16,state="readonly")
            self.med_entry.set("Select a Medicine")
            self.med_entry.grid(row=2, column=0,sticky="w")
            self.start_label = tk.Label(self.frame3,text="Start Date",bg="white")
            self.start_label.grid(row=3, column=0)
            self.start_entry = tk.Entry(self.frame3,fg="black",width=20)
            self.start_entry.grid(row=3, column=1)
            self.end_label = tk.Label(self.frame3,text="End Date",bg="white")
            self.end_label.grid(row=4, column=0)
            self.end_entry = tk.Entry(self.frame3,fg="black",width=20)
            self.end_entry.grid(row=4, column=1)
            self.freq_label = tk.Label(self.frame3,text="Frequency",bg="white")
            self.freq_label.grid(row=5, column=0)
            self.freq_entry = tk.Entry(self.frame3,fg="black",width=20)
            self.freq_entry.grid(row=5, column=1)
            self.BF_label = tk.Label(self.frame3,text="Intake (BF=1,AF=0)",bg="white")
            self.BF_label.grid(row=6, column=0)
            self.BF_entry = tk.Entry(self.frame3,fg="black",width=20)
            self.BF_entry.grid(row=6, column=1)
          
            submit_button = tk.Button(self.frame3, text="Prescribe", command=self.collect_input, font=("Verdana", 10))
            submit_button.place(relx=0.05, rely=0.85, relwidth=0.4, relheight=0.1)
            
            #FRAME 4: PAYMENT
            label1 = tk.Label(self.frame4, text="Recieved Payment?",font=("Verdana", 10),bg="white")
            label1.grid(row=1, column=0, padx=2, pady=5, columnspan=3, sticky="w") 
            submit_button = tk.Button(self.frame4, text="Yes", command=self.update_payment_status, font=("Verdana", 10))
            submit_button.place(relx=0.05, rely=0.85, relwidth=0.4, relheight=0.1)

        else:
            label3 = tk.Label(self.frame3, text=f"Appointment Status: {result[0]}",font=("Verdana", 10),bg="white")
            label3.grid(row=2, column=0, padx=2, pady=5, columnspan=3, sticky="w") 
            label4 = tk.Label(self.frame4, text=f"Appointment Status: {result[0]}",font=("Verdana", 10),bg="white")
            label4.grid(row=1, column=0, padx=2, pady=5, columnspan=3, sticky="w") 
          
        
        
    def add_med(self):
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        query="INSERT INTO Medicine VALUES (%s)"
        cur.execute(query,(self.new_med_entry.get(),))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", "Medicine added successfully!")
        
        
    def update_payment_status(self):
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        query = "UPDATE Appointment SET Status='Completed' WHERE A_id=%s"
        cur.execute(query, (A_id,))
        query2 = "UPDATE Payment_History SET Status='Paid' WHERE A_id=%s"
        cur.execute(query2, (A_id,))
        connection.commit()
        messagebox.showinfo("Success", "Appointment Completed!")
        
    def prescribe_func(self):
        
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        if self.BF_entry.get()==1:
            intake_entry="BF"
        else:
            intake_entry="AF"
        query = "INSERT INTO Prescription_History VALUES (%s, %s, %s, %s, %s,%s,%s);"
        cur.execute(query, (A_id, self.med_entry.get(), self.start_entry.get(), self.end_entry.get(), self.freq_entry.get(),intake_entry,None))
        connection.commit()  # Commit the transaction
        messagebox.showinfo("Success", "Prescribed!")
        connection.close()
        

    def collect_input(self):
        self.prescribe_func()

    def get_variable(self, option):
            return {
                "Med1": self.Med1,
                "Med2": self.Med2,
                "Med3": self.Med3,
                "Med4": self.Med4,
                "Med5": self.Med5
            }[option]
    def get_variable2(self,opt):
        return {
            "BF":self.BF,
            "AF": self.AF
        }[opt]
        

    def go_to_past_page(self):
        subprocess.Popen(["python", "MHPHomePage.py", M_id])  
        self.destroy()
        
if __name__=="__main__":
    file = sys.argv[0]
    M_id = sys.argv[1]
    A_id = sys.argv[2]
    if M_id is not None and A_id is not None:
        M_id = str(M_id)
        A_id = str(A_id)
    #M_id="1"
    #A_id="1"
    app=MHPAppDetails(M_id,A_id)
    app.mainloop()
    

