import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import datetime
import mysql.connector
import subprocess
import credentials as cr
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage
class MHPRegistrationPage(tk.Tk):
    def __init__(self):
        #self.sex = "Male"
        super().__init__()
        self.title("TheraConnect- MHP Registration Page")
        self.geometry("900x600")
        self.bg_img = ImageTk.PhotoImage(file="mhp1.png")
        background = Label(self,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)
        #self.eval('tk::PlaceWindow . center')

        self.frame = tk.Frame(self, bg="white", bd=4)
        self.frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        self.label = tk.Label(self.frame, text="Register", bg="white", anchor="w", font=("Verdana", 16))
        self.label.grid(row=0, column=0, padx=5, pady=5, columnspan=3)
        #self.bg_img = ImageTk.PhotoImage(file="mhp1.png")
        #background = Label(self,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)

        #CREATE ENTRY FIELDS
        self.entry_dict = {}
        self.entries1 = ["Username", "Password", "First Name", "Last Name"]
        self.entries2 = ["Sex", "Date of Birth","Phone", "Email"]
        self.entries3 = ["Address","Qualification", "Experience", "Rate per hour"]
        self.create_entry_fields(self.entries1, column=0)
        self.create_entry_fields(self.entries2, column=1)
        self.create_entry_fields(self.entries3, column=2)
        for col in range(3):
            self.frame.grid_columnconfigure(col, weight=1)

        #SIGN UP BUTTON
        signup_button = tk.Button(self.frame, text="Sign Up", font=("Verdana", 12), fg="white", width=20, bg="Grey", command=self.signup_func)
        signup_button.grid(row=len(self.entries1) + 20, column=0, padx=10, pady=25, columnspan=3)
        
        #GO TO LOGIN PAGE
        log_link = tk.Label(self.frame, text="Already have an account? Login", bg="white", font=("Verdana", 8, "underline"), fg="blue")
        log_link.grid(row=len(self.entries1) + 22, column=0, padx=10, pady=10, columnspan=3)
        log_link.bind("<Button-1>", self.mhplogin_window)
    def create_entry_fields(self, entries, column):
        for i, entry_text in enumerate(entries):
            label_row = i * 2 + 2  
            entry_row = label_row + 1
    
            label = tk.Label(self.frame, text=entry_text, bg="white")
            label.grid(row=label_row, column=column, padx=10, pady=5, sticky="w")
            
            if entry_text == "Date of Birth":
                days = [str(day) for day in range(1, 32)]
                months = [str(month) for month in ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")]
                years = [str(year) for year in range(1948, 2006)]

                day_combo = ttk.Combobox(self.frame, values=days, width=4,state="readonly")
                month_combo = ttk.Combobox(self.frame, values=months, width=6,state="readonly")
                year_combo = ttk.Combobox(self.frame, values=years, width=4,state="readonly")

                day_combo.set("Day")
                month_combo.set("Month")
                year_combo.set("Year")

                day_combo.grid(row=entry_row, column=column, padx=(5, 0), pady=5, sticky="w")
                month_combo.grid(row=entry_row, column=column, padx=0, pady=5)
                year_combo.grid(row=entry_row, column=column, padx=(0, 5), pady=5, sticky="e")
                entry = (day_combo, month_combo, year_combo)
                self.entry_dict[entry] = f"Enter {entry_text}"
                
            elif entry_text == "Sex":
                sex = [str(sex) for sex in ("Male", "Female", "Other")]
                entry= ttk.Combobox(self.frame, values=sex, width=7,state="readonly")
                entry.set("Male")
                entry.grid(row=entry_row, column=column, padx=5, pady=5, sticky="w")
                entry=(entry,entry,entry)
                self.entry_dict[entry] = f"Enter {entry_text}"
              
                
            elif entry_text == "Address" or entry_text =="Qualification" :
                entry = tk.Text(self.frame, wrap=tk.WORD, width=30, height=3, fg="grey")
                entry.grid(row=entry_row, column=column, padx=5, pady=5, sticky="w")
                entry.insert("1.0",f"Enter {entry_text}")
                self.setup_placeholder(entry, f"Enter {entry_text}")
                
            else:
                entry = tk.Entry(self.frame, fg="grey", width=30)
                entry.grid(row=entry_row, column=column, padx=10, pady=5, sticky="w")
                entry.insert(0,f"Enter {entry_text}")
                self.setup_placeholder(entry, f"Enter {entry_text}")
            

    def setup_placeholder(self, entry, placeholder):
        self.entry_dict[entry] = placeholder
        if isinstance(entry, tk.Entry):
            entry.bind("<FocusIn>", self.on_entry_click)
            entry.bind("<FocusOut>", self.on_entry_leave)
        elif isinstance(entry, tk.Text):
            entry.bind("<FocusIn>", self.on_text_click)
            entry.bind("<FocusOut>", self.on_text_leave)
            
    def on_entry_click(self, event):
        entry = event.widget
        if entry.get() == self.entry_dict[entry]:
            entry.delete(0,"end")
            entry.config(fg="black")

    def on_entry_leave(self, event):
        entry = event.widget
        if entry.get().strip() == "":    
            entry.delete(0, "end")
            entry.insert(0, self.entry_dict[entry])
            entry.config(fg="grey")
          
    def on_text_click(self, event):
        text = event.widget
        if text.get("1.0", "end-1c") == self.entry_dict[text]:
            text.delete("1.0", "end-1c")
            text.config(fg="black")

    def on_text_leave(self, event):
        text = event.widget
        if text.get("1.0", "end-1c").strip() == "":
            text.delete("1.0", "end-1c")
            text.insert("1.0", self.entry_dict[text])
            text.config(fg="grey")
    def mhplogin_window(self,event):
        self.destroy()
        subprocess.Popen(["python","MHPLogin.py"])
   
        
    def signup_func(self):
            #CHECK IF ALL FIELDS ARE FILLED
            validation_result = self.validate_entries()
            
            #GET THE INPUT FROM ALL FIELDS
            if validation_result:
                connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                cur = connection.cursor()
                for entry, placeholder in self.entry_dict.items():
                    if isinstance(entry, tk.Entry):
                        if placeholder == "Enter Username":
                            username = entry.get()
                        elif placeholder == "Enter Password":
                                password = entry.get()
                        elif placeholder == "Enter First Name":
                                fname = entry.get()
                        elif placeholder == "Enter Last Name":
                                lname = entry.get()
                        elif placeholder == "Enter Phone":
                                phone = entry.get()
                        elif placeholder == "Enter Email":
                                email = entry.get()
                        elif placeholder == "Enter Experience":
                                exp = entry.get()
                        elif placeholder == "Enter Rate per hour":
                                rate = entry.get()
                    elif isinstance(entry, tk.Text):
                        if placeholder == "Enter Address":
                                addr = entry.get("1.0", "end-1c")
                                if addr.strip() == "" or addr=="Enter Address":
                                    addr = None
                        elif placeholder == "Enter Qualification":
                                qualification = entry.get("1.0", "end-1c")
                    elif isinstance(entry,tuple):
                        if placeholder == "Enter Date of Birth":
                            day, month, year = [item.get() for item in entry]
                            day = int(day)
                            month = datetime.datetime.strptime(month, '%b').month
                            year = int(year)
                            DOB = datetime.date(year, month, day)
                        if placeholder == "Enter Sex":
                                sex, arbitary1, arbitary2 = [item.get() for item in entry]
                
                #CHECK IF INPUTS ARE VALID
                validation_errors = [] 
                validation_errors = self.validation_error(validation_errors,username,password,fname,lname,phone,email,rate)
                if validation_errors:
                    try:
                        curr_date=datetime.date.today()
                        curr_year=curr_date.strftime("%Y")
                        DOB=str(DOB)
                        age=str(int(curr_year)-year)
                        DOJ= str(datetime.date.today().strftime('%Y-%m-%d'))
                        rate=str(rate)
                        rating=str(0)
                        sex=sex[0]
                        
                        #PERFORM INSERTION
                        query1 = "INSERT INTO MHP (Username, Password, First_Name, Last_Name, Date_Of_Birth, Age, Date_Of_Joining, Phone, Email, Address, Sex, Qualification, Experience, Rating, Rate_per_hour) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                        cur.execute(query1, (username, password, fname, lname, DOB, age, DOJ, phone, email, addr, sex, qualification, exp, rating, rate))
                
                        #PASS M_ID TO NEXT PAGE
                        query2 = "SELECT M_id FROM MHP WHERE Username = %s"
                        cur.execute(query2, (username,))
                        result = cur.fetchone()
                        M_id=str(result[0])
                        
                        connection.commit() 
                        #INSERT INTO SCHEDULE TABLE
                        start_date = datetime.date.today()
                        print("start date",start_date)
                        start_day = start_date.strftime("%A")
                        print("start day",start_day)
                        i=1
                        while (i<6):
                            if start_day not in ["Sunday","Saturday"]:
                                query3 = "INSERT INTO Schedule VALUES (%s,%s,%s,0,0,0,0,0,0,0,0)"
                                cur.execute(query3, (M_id,str(start_day), str(start_date)))
                                i+=1
                            start_date += datetime.timedelta(days=1)
                            start_day = start_date.strftime("%A")
                            
                        connection.commit() 

                        connection.close()
                        self.destroy()
                        subprocess.Popen(["python", "MHPSpeciality.py", M_id])
                    except Exception as e:
                        connection.rollback()  
                        messagebox.showerror("Error", f"Error due to {str(e)}")
                    
                        
                        
                        
    def validation_error(self,validation_errors,username,password,fname,lname,phone,email,rate):
         if len(username) < 3:
              messagebox.showerror("Error!", "Username is too short. It must have a length of at least 3.")
              return False
         connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
         cur = connection.cursor()
         query1= "SELECT * FROM MHP WHERE Username = %s"
         cur.execute(query1,(username,))
         result = cur.fetchall()
         if result:
                  messagebox.showerror("Error!", "Username already exists.")
                  connection.close()
                  return False
         if len(password) < 5:
              messagebox.showerror("Error!", "Password is too short. It must have a length of at least 5.")
              return False
         if not fname.isalpha():
              messagebox.showerror("Error!", "First Name should contain only alphabets.")
              return False
         if not lname.isalpha():
              messagebox.showerror("Error!", "Last Name should contain only alphabets.")
              return False
         if not phone.isnumeric():
              messagebox.showerror("Error!","Phone number should contain only numerals.")
              return False
         if len(phone)!=10:
             messagebox.showerror("Error!","Please enter a valid Phone.")
             return False
         email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
         if not re.match(email_pattern, email):
              messagebox.showerror("Error!", "Please enter a valid email address.")
              return False
         try:
              rate = float(rate)
              if not (0 <= rate <= 9999999.99):
                  messagebox.showerror("Error!", "Rate has exceeded the limit.")
                  return False
         except ValueError:
                 messagebox.showerror("Error!", "Please enter a valid rate per hour.")
                 return False
         return True
              
    def validate_entries(self):
        mandatory_fields = ["Enter Username",
                            "Enter Password", 
                            "Enter First Name", 
                            "Enter Last Name",
                            "Enter Date of Birth",
                            "Enter Phone", 
                            "Enter Email", 
                            "Enter Qualification", 
                            "Enter Experience(in years)", 
                            "Rate per hour"]   
        for entry, placeholder in self.entry_dict.items():
            if isinstance(entry, tk.Entry):
                if entry.get().strip() == placeholder and placeholder in mandatory_fields:
                    messagebox.showerror("Error!", f"{placeholder}")
                    return False 
            elif isinstance(entry, tk.Text):
                if entry.get("1.0", "end-1c").strip() == placeholder and placeholder in mandatory_fields:
                    messagebox.showerror("Error!", f"{placeholder}")
                    return False
            elif isinstance(entry,tuple):
                if all(item.get() in ("Day","Month","Year") for item in entry) and "Enter Date of Birth" in mandatory_fields:
                    messagebox.showerror("Error!", "Enter valid Date of Birth")
                    return False
        return True

    
if __name__ == "__main__":
     app = MHPRegistrationPage()
     app.mainloop()    
     
