from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import os
from signup_page import SignUp
import credentials as cr
from tkcalendar import Calendar
import subprocess
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage
class login_page:
    def __init__(self, root):
        self.window = root
        self.window.title("Log In Theraconnect")
        # Set the window size
        # Here 0,0 represents the starting point of the window 
        self.window.geometry("1280x800+0+0")
        self.window.config(bg = "white")
        self.bg_img = ImageTk.PhotoImage(file="mhp1.png")
        background = Label(self.window,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)

        self.frame1 = Frame(self.window, bg="#7DC5E7")
        self.frame1.place(x=0, y=0, width=450, relheight = 1)

        #label1 = Label(self.frame1, text= "Py", font=("times new roman", 40, "bold"), bg="yellow", fg="red").place(x=100,y=300)
        #label2 = Label(self.frame1, text= "Seek", font=("times new roman", 40, "bold"), bg="yellow", fg="RoyalBlue1").place(x=162,y=300)
        #label3 = Label(self.frame1, text= "It's all about Python", font=("times new roman", 13, "bold"), bg="yellow", fg="brown4").place(x=100,y=360)


        self.frame2 = Frame(self.window, bg = "#F0F8FF")
        self.frame2.place(x=450,y=0,relwidth=1, relheight=1)

        self.frame3 = Frame(self.frame2, bg="white")
        self.frame3.place(x=140,y=150,width=500,height=450)

        self.uname_label = Label(self.frame3,text="Username", font=("helvetica",20,"bold"),bg="white", fg="gray").place(x=50,y=40)
        self.uname_entry = Entry(self.frame3,font=("times new roman",15,"bold"),bg="white",fg="gray")
        self.uname_entry.place(x=50, y=80, width=300)

        self.password_label = Label(self.frame3,text="Password", font=("helvetica",20,"bold"),bg="white", fg="gray").place(x=50,y=120)
        self.password_entry = Entry(self.frame3,font=("times new roman",15,"bold"),bg="white",fg="gray",show="*")
        self.password_entry.place(x=50, y=160, width=300)

        #================Buttons===================
        self.login_button = Button(self.frame3,text="Log In",command=self.login_func,font=("times new roman",15, "bold"),bd=0,cursor="hand2",bg="#AED4F1",fg="white").place(x=50,y=200,width=300)

        self.forgotten_pass = Button(self.frame3,text="Forgotten password?",command=self.forgot_func,font=("times new roman",10, "bold"),bd=0,cursor="hand2",bg="white",fg="blue").place(x=125,y=260,width=150)

        self.create_button = Button(self.frame3,text="Create New Account",command=self.redirect_window,font=("times new roman",18, "bold"),bd=0,cursor="hand2",bg="#71A6D2",fg="white").place(x=80,y=320,width=250)


    def login_func(self):
        if self.uname_entry.get()=="" or self.password_entry.get()=="":
            messagebox.showerror("Error!","All fields are required",parent=self.window)
        else:
            try:
                connection = mysql.connector.connect(host="localhost", user="root", passwd="chaitra08", charset="utf8", database="theraconnect_patronus")
                cur = connection.cursor()
                #connection=pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                #cur = connection.cursor()
                cur.execute("select * from User where Username=%s and Password=%s",(self.uname_entry.get(),self.password_entry.get()))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error!","Invalid USERNAME & PASSWORD",parent=self.window)
                else:
                    messagebox.showinfo("Success","Wellcome to Theraconnect!",parent=self.window)
                    self.username=self.uname_entry.get()
                    self.reset_fields()
                    self.redirect()
                    
                    connection.close()

            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)

    def forgot_func(self):
        if self.uname_entry.get()=="":
            messagebox.showerror("Error!", "Please enter your Username",parent=self.window)
        else:
            try:
                connection = mysql.connector.connect(host="localhost", user="root", passwd="chaitra08", charset="utf8", database="theraconnect_patronus")
                #mysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                cur = connection.cursor()
                cur.execute("SELECT * FROM user WHERE username=%s", (self.uname_entry.get(),))
                #cur.execute("select * from user where username=%s", self.uname_entry.get())
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error!", "Username doesn't exists")
                else:
                    self.username=self.uname_entry.get()
                    connection.close()
                    
                  

                    self.root=Toplevel()
                    self.root.title("Forget Password?")
                    self.root.geometry("400x440+450+200")
                    self.root.config(bg="white")
                    self.root.focus_force()
                    self.root.grab_set()

                    title3 = Label(self.root,text="Change your password",font=("times new roman",20,"bold"),bg="white").place(x=10,y=10)

                    title4 = Label(self.root,text="It's quick and easy",font=("times new roman",12),bg="white").place(x=10,y=45)

                    title5 = Label(self.root, text="New Password", font=("times new roman", 15, "bold"), bg="white").place(x=10,y=100)
                    title6 = Label(self.root, text="Re- Enter New Password", font=("times new roman", 15, "bold"), bg="white").place(x=10,y=200)
                    #self.password_entry = Entry(self.frame3,font=("times new roman",15,"bold"),bg="white",fg="gray",show="*")
                    self.new_pass = Entry(self.root,font=("arial"),show="*")
                    self.new_pass.place(x=10,y=150,width=270)
                    self.new_pass1 = Entry(self.root,font=("arial"),show="*")
                    self.new_pass1.place(x=10,y=250,width=270)

                    self.create_button = Button(self.root,text="Submit",command=self.change_pass,font=("times new roman",18, "bold"),bd=0,cursor="hand2",bg="green2",fg="white").place(x=95,y=340,width=200)
                    #=========================================================================

            except Exception as e:
                messagebox.showerror("Error", f"{e}")
                
      
    def change_pass(self):
        if self.uname_entry.get() == ""  or self.new_pass.get() == "" or self.new_pass1.get() == "" :
            messagebox.showerror("Error!", "Please fill the all entry field correctly")
        elif self.new_pass1.get()!=self.new_pass.get():
            messagebox.showerror("Error!","Passwords are not Matching")
        else:
            try:
                connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                cur = connection.cursor()
                cur.execute("select * from user where username=%s", (self.uname_entry.get(),))
                row=cur.fetchone()
                print(row)
                if row == None:
                    messagebox.showerror("Error!", "Please fill the all entry field correctly")
                else:
                    try:
                        cur.execute("update user set password=%s where username=%s", (self.new_pass.get(),self.uname_entry.get()))
                        connection.commit()

                        messagebox.showinfo("Successful", "Password has changed successfully")
                        self.username=self.uname_entry.get()
                        connection.close()
                        self.reset_fields()
                        self.root.destroy()
                        self.redirect()

                    except Exception as er:
                        messagebox.showerror("Error!", f"{er}")
                        
            except Exception as er:
                        messagebox.showerror("Error!", f"{er}")
            
    def redirect_window(self):
        subprocess.Popen(["python","signup_page.py"])
        self.window.destroy()
       

    def redirect(self):
        #username=self.uname_txt.get()
        self.window.destroy()
        subprocess.Popen(["python","doctor_search.py",self.username])

    def reset_fields(self):
        self.uname_entry.delete(0,END)
        self.password_entry.delete(0,END)
# The main function
if __name__ == "__main__":
    root = Tk()
    obj = login_page(root)
    root.mainloop()
