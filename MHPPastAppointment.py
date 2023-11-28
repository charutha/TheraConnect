import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import mysql.connector
import credentials as cr
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage

class MHPPastAppointment(tk.Tk):
    def __init__(self, M_id):
        print(M_id)
        super().__init__()
        self.title("TheraConnect-MHP Past Appointments")
        self.geometry("900x600")
        self.bg_img = ImageTk.PhotoImage(file="mhp1.png")
        background = Label(self,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)
        #self.eval('tk::PlaceWindow . center')
        self.header_label = tk.Label(self, text="Past Appointments", font=("Verdana", 16))
        self.header_label.place(relx=0.5, rely=0.01, anchor="n")
        
        self.back_button = tk.Button(self, text="<- Back", font=("Verdana", 10),command=self.go_to_home)
        self.back_button.place(relx=0.1, rely=0.01, anchor="n")
        
        
        #FRAME FOR UPCOMING APPOINTMENTS
        self.frame1 = tk.Frame(self, bg="white", bd=4)
        self.frame1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        self.label1 = tk.Label(self.frame1, text="List of Completed Appointments", bg="white", anchor="w", font=("Verdana", 10))
        self.label1.grid(row=0, column=0, padx=5, pady=5, columnspan=3,sticky="nsew")
        
        #CANVAS FOR UPCOMING REQUESTS
        self.canvas1 = tk.Canvas(self.frame1,width=675,height=415)
        self.canvas1.grid(row=1, column=0)
        
        self.upcoming_appointments()
        
    def upcoming_appointments(self):
                 scrollbar = tk.Scrollbar(self.frame1, orient="vertical", command=self.canvas1.yview)
                 scrollbar.grid(row=1, column=1, sticky="ns")
                 self.inner_frame1 = tk.Frame(self.canvas1,height=160)
                 self.canvas1.create_window((0, 0), window=self.inner_frame1, anchor="nw")
                 connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                 cur = connection.cursor()
                 query= "SELECT * FROM Appointment WHERE M_id = %s AND (status = 'Completed' OR status = 'Cancelled')"
                 cur.execute(query, (str(M_id),))
                 result = cur.fetchall()
                 connection.close()
                 if result:
                     print(result)
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
                     no_appointments_label = tk.Label(self.inner_frame1, text="No Past appointments :(", font=("Verdana", 10))
                     no_appointments_label.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="w")
   
    def details(self,A_id):
        A_id=str(A_id)
        subprocess.Popen(["python", "MHPAppDetails.py", M_id,A_id])  
        self.destroy()
        
    def go_to_home(self):
        subprocess.Popen(["python", "MHPHomePage.py", M_id])  
        self.destroy()
                

if __name__=="__main__":
    M_id = sys.argv[1]
    if M_id is not None:
        M_id = str(M_id)
    #M_id="1"
    app=MHPPastAppointment(M_id)
    app.mainloop()
    

