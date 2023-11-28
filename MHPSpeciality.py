import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import mysql.connector
import credentials as cr
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage
class MHPSpeciality(tk.Tk):
    def __init__(self, M_id):
        super().__init__()
        self.title("TheraConnect-MHP Speciality")
        self.geometry("900x600")
        #self.eval('tk::PlaceWindow . center')
        self.bg_img = ImageTk.PhotoImage(file="mhp1.png")
        background = Label(self,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)
        
        self.header_label1 = tk.Label(self, text="Before we get Started!", font=("Verdana", 20))
        self.header_label1.place(relx=0.5, rely=0.1, anchor="n")
        self.header_label2 = tk.Label(self, text="Which of the following do you specialize in?", font=("Times New Roman", 16))
        self.header_label2.place(relx=0.5, rely=0.2, anchor="n")
        
        self.frame_width = 0.3
        self.frame_height = 0.3
        self.relx = (1 - self.frame_width) / 2
        self.rely = (1 - self.frame_height) / 2
        self.frame = tk.Frame(self, bg="white", bd=4)
        self.frame.place(relx=self.relx, rely=self.rely, relwidth=self.frame_width, relheight=self.frame_height)
        
        #INITIALIZE ALL SPECIALITY PARAMETERS
        self.Trauma_Informed = tk.IntVar()
        self.Disability_Friendly = tk.IntVar()
        self.Queer_Friendly = tk.IntVar()
        self.Child_Specialist = tk.IntVar()        
        self.checkboxes = []
        options = ["Trauma Informed", "Disability Friendly", "Queer Friendly", "Child Specialist"]
        
        #CREATE CHECK BOXES
        for row, option in enumerate(options):
            checkbox = tk.Checkbutton(self.frame, text=option, variable=self.get_variable(option), bg="white", font=("Verdana", 12))
            self.checkboxes.append(checkbox)
            checkbox.grid(row=row + 2, column=0, sticky="w")

        submit_button = tk.Button(self.frame, text="Submit", command=self.collect_input, font=("Verdana", 12))
        submit_button.place(relx=0.1, rely=0.8, relwidth=0.8, relheight=0.18)

        self.M_id = M_id

    def get_variable(self, option):
        return {
            "Trauma Informed": self.Trauma_Informed,
            "Disability Friendly": self.Disability_Friendly,
            "Queer Friendly": self.Queer_Friendly,
            "Child Specialist": self.Child_Specialist
        }[option]

    def speciality_func(self):
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        try:
            query = "INSERT INTO Speciality (M_id, Trauma_Informed, Disability_Friendly, Queer_Friendly, Child_Specialist) VALUES (%s, %s, %s, %s, %s);"
            cur.execute(query, (self.M_id, self.Trauma_Informed.get(), self.Disability_Friendly.get(), self.Queer_Friendly.get(), self.Child_Specialist.get()))
            connection.commit()  # Commit the transaction
            messagebox.showinfo("Success", "Let's Get Started!")
            connection.close()
            self.destroy()
            subprocess.Popen(["python", "MHPHomePage.py", M_id])
        except Exception as e:
            connection.rollback() 
            messagebox.showerror("Error", f"Error due to {str(e)}")
        

    def collect_input(self):
        self.speciality_func()

if __name__ == "__main__":
    M_id = sys.argv[1] if len(sys.argv) > 1 else None
    if M_id is not None:
        M_id = str(M_id)
    #M_id=1
    app = MHPSpeciality(M_id)
    app.mainloop()

