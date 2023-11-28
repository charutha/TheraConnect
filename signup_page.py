
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import  os
import mysql.connector
import credentials as cr
from tkcalendar import Calendar
#from cal import getDate
from datetime import datetime
from datetime import date
#from settings import UserSettingsPage
import subprocess
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage
def process_selected_date(selected_date):
        print("Selected Date in main.py:", selected_date)
class SignUp:
    def __init__(self, root):
        #root1 = Tk()
        #root1.geometry("400x400")
        self.window = root
        #self.window1=root1
        #self.window1.geometry("1280x800+0+0")
        self.window.title("Sign Up")
        self.window.geometry("1280x800+0+0")
        self.window.config(bg = "white")
        self.bg_img = ImageTk.PhotoImage(file="mhp1.png")
        background = Label(self.window,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)

        #self.bg_img = ImageTk.PhotoImage(file="Images/photo1.jpeg")
        #background = Label(self.window).place(x=0,y=0,relwidth=1,relheight=1)


        frame = Frame(self.window, bg="white")
        frame.place(x=300,y=100,width=800,height=600)
        
        title1 = Label(frame, text="Sign Up", font=("times new roman",25,"bold"),bg="white").place(x=20, y=10)
        title2 = Label(frame, text="Join with us", font=("times new roman",13),bg="white", fg="gray").place(x=20, y=50)
        
        f_name = Label(frame, text="First name", font=("helvetica",15,"bold"),bg="white").place(x=20, y=100)
        self.fname_txt = Entry(frame,font=("arial"))
        self.fname_txt.place(x=20, y=130, width=200)

        l_name = Label(frame, text="Last name", font=("helvetica",15,"bold"),bg="white").place(x=240, y=100)
        self.lname_txt = Entry(frame,font=("arial"))
        self.lname_txt.place(x=240, y=130, width=200)

        address=Label(frame, text="Address", font=("helvetica",15,"bold"),bg="white").place(x=460, y=100)
        self.address_txt = Entry(frame,font=("arial"))
        self.address_txt.place(x=460, y=130, width=200)

        uname=Label(frame, text="Uname", font=("helvetica",15,"bold"),bg="white").place(x=20, y=180)
        self.uname_txt=Entry(frame,font=("arial"))
        self.uname_txt.place(x=20,y=210,width=200)

        password =  Label(frame, text="password", font=("helvetica",15,"bold"),bg="white").place(x=240, y=180)
        self.password_txt = Entry(frame,font=("arial"),show="*")
        self.password_txt.place(x=240, y=210, width=200)

        email = Label(frame, text="Email", font=("helvetica",15,"bold"),bg="white").place(x=460, y=180)
        self.email_txt = Entry(frame,font=("arial"))
        self.email_txt.place(x=460, y=210, width=200)
        
        phno=Label(frame, text="Phone Number", font=("helvetica",15,"bold"),bg="white").place(x=20, y=260)
        self.phno_txt = Entry(frame,font=("arial"))
        self.phno_txt.place(x=20, y=290, width=200)

        Sex = Label(frame, text="Sex(M,F,O)", font=("helvetica",15,"bold"),bg="white").place(x=460, y=260)
        self.sex_txt = Entry(frame,font=("arial"))
        self.sex_txt.place(x=460, y=290, width=200)
        Dob = Label(frame, text="Date of Birth", font=("helvetica",15,"bold"),bg="white").place(x=240, y=260)
        self.cal2 = Calendar(frame, selectmode='day', year=2000, month=5, day=22, date_pattern='y/mm/dd')
        self.cal2.place(x=240, y=290, width=200)
        def date_dob():
             self.selected_date1 =self.cal2.get_date()
             print(self.selected_date1)
             print(type(self.selected_date1))
        get_dob_button = Button(frame, text="Get Selected Date",command=date_dob)
        get_dob_button.place(x=240, y=500, width=200)
        self.signup = Button(frame,text="Sign Up",command=self.signup_func,font=("times new roman",18, "bold"),bd=0,cursor="hand2",bg="#71A6D2",fg="white").place(x=460,y=400,width=150)

    def signup_func(self):
        if self.fname_txt.get()=="" or self.lname_txt.get()=="" or self.email_txt.get()==""  or self.password_txt.get() == "":
            messagebox.showerror("Error!","Sorry!, All fields are required",parent=self.window)

        else:
            try:
                connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                cur = connection.cursor()
                cur.execute("select * from user where email=%s",(self.email_txt.get(),))
                print("hello")
                row=cur.fetchone()

                # Check if th entered email id is already exists or not.
                if row!=None:
                    messagebox.showerror("Error!","The email id is already exists, please try again with another email id",parent=self.window)
                else:           
                    print("dob",self.selected_date1)
                    date_of_birth = self.selected_date1 
                    dob_date = datetime.strptime(self.selected_date1, '%Y/%m/%d').date()  # Convert the string to a date object
                    print("Date of Birth:", dob_date)
                    current_date = date.today() 
                    age = current_date.year - dob_date.year - ((current_date.month, current_date.day) < (dob_date.month, dob_date.day))
                    print("Age:", age, "years")
                    self.username=self.uname_txt.get()
                    cur.execute("insert into user(Username,Password,First_name,Last_name,Date_Of_Birth,Age,Date_Of_Joining,Phone,Email,Address,Sex)values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                    (
                                        self.uname_txt.get(),
                                        self.password_txt.get(),
                                        self.fname_txt.get(),
                                        self.lname_txt.get(),
                                        self.selected_date1,
                                        age,
                                        current_date,
                                        self.phno_txt.get(),
                                        self.email_txt.get(),
                                        self.address_txt.get(),
                                        self.sex_txt.get()
                                    ))
                    cur.execute("select u_id from user where username=%s",(self.uname_txt.get(),))
                    row=cur.fetchone()
                    print(row)
                    connection.commit()
                    connection.close()
                    messagebox.showinfo("Congratulations!","Register Successful",parent=self.window)
                    self.reset_fields()
                    self.redirect_window()

            except Exception as es:
                print("hello")
                messagebox.showerror("Error!",f"Error due to {es}",parent=self.window)

   
    def process_selected_date(selected_date):
        print("Selected Date in main.py:", selected_date)

    def redirect_window(self):
        username=self.uname_txt.get()
        self.window.destroy()
        subprocess.Popen(["python","doctor_search.py",self.username])
    def reset_fields(self):
        self.fname_txt.delete(0, END)
        self.lname_txt.delete(0, END)
        self.email_txt.delete(0, END)
        self.password_txt.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    obj = SignUp(root)
    root.mainloop()
