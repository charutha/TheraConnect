import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess
import sys
import mysql.connector
import credentials as cr
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage
class MHPSettings(tk.Tk):
    def __init__(self, M_id):
        super().__init__()
        self.title("TheraConnect-MHP Settings Page")
        self.geometry("900x600")
        self.bg_img = ImageTk.PhotoImage(file="mhp1.png")
        background = Label(self,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)
        #self.eval('tk::PlaceWindow . center')
        self.header_label = tk.Label(self, text="Settings Page", font=("Verdana", 14))
        self.header_label.place(relx=0.5, rely=0.01, anchor="n")
        
        self.back_button = tk.Button(self, text="<- Back", font=("Verdana", 10),command=self.go_to_home)
        self.back_button.place(relx=0.1, rely=0.01, anchor="n")

        self.frame1 = tk.Frame(self, bg="white", bd=4)
        self.frame1.place(relx=0.35, rely=0.1, relwidth=0.4, relheight=0.65)
        self.label1 = tk.Label(self.frame1, text="Edit your Details", bg="white", anchor="w", font=("Verdana", 12))
        #self.label1.place(relx=0.5, rely=0.1)
        self.label1.grid(row=0, column=0, padx=5, pady=5, columnspan=3,sticky="nw")
        
        # CREATE LABELS AND ENTRY FIELDS
        self.first_name_label = tk.Label(self.frame1, text="First Name:", font=("Verdana", 10),bg="white")
        self.first_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.first_name_entry = tk.Entry(self.frame1, font=("Verdana", 10))
        self.first_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.last_name_label = tk.Label(self.frame1, text="Last Name:", font=("Verdana", 10),bg="white")
        self.last_name_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.last_name_entry = tk.Entry(self.frame1, font=("Verdana", 10))
        self.last_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.phone_label = tk.Label(self.frame1, text="Phone:", font=("Verdana", 10),bg="white")
        self.phone_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.phone_entry = tk.Entry(self.frame1, font=("Verdana", 10))
        self.phone_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.email_label = tk.Label(self.frame1, text="Email:", font=("Verdana", 10),bg="white")
        self.email_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.email_entry = tk.Entry(self.frame1, font=("Verdana", 10))
        self.email_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        self.address_label = tk.Label(self.frame1, text="Address:", font=("Verdana", 10),bg="white")
        self.address_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.address_entry = tk.Entry(self.frame1, font=("Verdana", 10))
        self.address_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        self.sex_label = tk.Label(self.frame1, text="Sex:", font=("Verdana", 10),bg="white")
        self.sex_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.sex_entry = ttk.Combobox(self.frame1, values=["M", "F", "O"], font=("Verdana", 10),width=17)
        self.sex_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        
        #POPULATE FIELDS WITH EXISTING DATA
        self.populate_data()
        
        #UPDATE BUTTON
        self.update_button = tk.Button(self.frame1, text="Update Details",width=25, font=("Verdana", 10), command=self.update_details)
        self.update_button.grid(row=7, column=0, columnspan=2,padx=5,pady=10,sticky="w")
        
        #DELETE BUTTON
        self.delete_button = tk.Button(self.frame1, text="Delete Account", width=25, font=("Verdana", 10), command=self.confirm_delete)
        self.delete_button.grid(row=12, column=0, columnspan=2,padx=5, pady=20,sticky="w")
        
    def populate_data(self):
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        query = "SELECT First_Name, Last_Name, Phone, Email, Address, Sex FROM MHP WHERE M_id = %s"
        cur.execute(query, (str(M_id),))
        result = cur.fetchone()
        connection.close()

        if result:
            first_name, last_name, phone, email, address, sex = result
            self.first_name_entry.insert(0, first_name)
            self.last_name_entry.insert(0, last_name)
            self.phone_entry.insert(0, phone)
            self.email_entry.insert(0, email)
            self.address_entry.insert(0, address)
            self.sex_entry.set(sex)
            
    def update_details(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()
        sex = self.sex_entry.get()

        # Update the details in the database
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        query = "UPDATE MHP SET First_Name = %s, Last_Name = %s, Phone = %s, Email = %s, Address = %s, Sex = %s WHERE M_id = %s"
        cur.execute(query, (first_name, last_name, phone, email, address, sex, str(M_id)))
        connection.commit()
        connection.close()

        messagebox.showinfo("Success", "Details updated successfully!")
        
    
    def confirm_delete(self):
        result = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete your account?\nThis action is irreversible.")
        if result:
            self.delete_account()
        else:
            messagebox.showinfo("Account Deletion Canceled", "Your account was not deleted.")

        
    def delete_account(self):
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        try:
            """
            query =
                DELETE FROM Speciality WHERE M_id=%s;
                DELETE FROM Schedule WHERE M_id=%s;
                DELETE FROM Review WHERE M_id=%s;
                DELETE FROM Appointment WHERE M_id=%s AND (Status="Upcoming" OR Status="Pending");
                DELETE FROM Payment_history WHERE M_id=%s AND Status="Pending";
                DELETE FROM mhp WHERE M_id=%s;
            
            cur.execute(query, (M_id, M_id, M_id, M_id, M_id, M_id))
            connection.commit()
            """
            cur.execute("START TRANSACTION;")
            connection.commit()

            query = "DELETE FROM review WHERE M_id = %s;"
            cur.execute(query, (M_id,))
            connection.commit()
           
            query = "DELETE FROM payment_history WHERE A_id IN (SELECT A_id FROM Appointment WHERE M_id=%s);"
            cur.execute(query, (M_id,))
            connection.commit()

            query = "DELETE FROM prescription_history WHERE A_id IN (SELECT A_id FROM Appointment WHERE M_id=%s);"
            cur.execute(query, (M_id,))
            connection.commit()
       
            query =  "DELETE FROM appointment WHERE M_id = %s;"
            cur.execute(query, (M_id,))
            connection.commit()
            
            query = "DELETE FROM schedule WHERE M_id=%s;"
            cur.execute(query, (M_id,))
            connection.commit()

            query = "DELETE FROM speciality WHERE M_id=%s;"
            cur.execute(query, (M_id,))
            connection.commit()

            query = " DELETE FROM mhp WHERE M_id = %s;"
            cur.execute(query, (M_id,))
            connection.commit()
            

            cur.execute("COMMIT;")
            connection.commit()

            cur.execute("ROLLBACK;")
            connection.commit()

            connection.commit()
            connection.close()
            self.destroy()

        except Exception as e:
            connection.rollback()
            print("Error:", str(e))
        #except mysql.connector.Error as e:
            #connection.rollback()
            #print(f"Error: {e}")
            print(e)
        finally:
            connection.close()
            messagebox.showinfo("Account Deleted", "Your account has been deleted.")
            
    def go_to_home(self):
            subprocess.Popen(["python", "MHPHomePage.py", M_id])  
            self.destroy()
            

if __name__=="__main__":
    M_id = sys.argv[1]
    if M_id is not None:
      M_id = str(M_id)
    # M_id="1"
    app=MHPSettings(M_id)
    app.mainloop()