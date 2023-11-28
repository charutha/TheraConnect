import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess
import sys
import mysql.connector
import credentials as cr
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage
class MHPReview(tk.Tk):
    def __init__(self, M_id):
        super().__init__()
        self.title("TheraConnect-MHP Reviews")
        #self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.geometry("900x600")
        self.bg_img = ImageTk.PhotoImage(file="mhp1.png")
        background = Label(self,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)
        #self.eval('tk::PlaceWindow . center')
        self.header_label = tk.Label(self, text="Reviews", font=("Verdana", 16))
        self.header_label.place(relx=0.5, rely=0.01, anchor="n")
        
        self.back_button = tk.Button(self, text="<- Back", font=("Verdana", 10),command=self.go_to_home)
        self.back_button.place(relx=0.1, rely=0.01, anchor="n")
        
        self.frame = tk.Frame(self, bg="white", bd=4)
        self.frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        self.label = tk.Label(self.frame, text="Patient Reviews", bg="white", font=("Verdana", 10))
        self.label.grid(row=0, column=0, padx=(5, 0), pady=5, sticky="w")
        

        #BY RATING
        self.rating_button=tk.Button(self.frame,text="Filter Rating: Descending",font=("Verdana", 10),command=self.on_rating_click)
        self.rating_button.grid(row=1, column=0, padx=(0,99), pady=5, sticky="w")
        
        #BY NO. OF SESSIONS
        self.session_button=tk.Button(self.frame,text="Filter By No. of Sessions",font=("Verdana", 10),command=self.on_session_click)
        self.session_button.place(relx=0.26, rely=0.08)
        #self.session_button.grid(row=1, column=1, padx=(0,99), pady=5, sticky="w")
                
        #BY TIME
        self.time_button=tk.Button(self.frame,text="Filter By Time",font=("Verdana", 10),command=self.on_time_click)
        self.time_button.place(relx=0.51, rely=0.08)
        #self.time_button.grid(row=1, column=2, padx=(0,99), pady=5, sticky="w")
        
        #BY AGE
        self.age_button=tk.Button(self.frame,text="Filter By Age",font=("Verdana", 10),command=self.on_age_click)
        self.age_button.place(relx=0.66, rely=0.08)
        #self.age_button.grid(row=1, column=3, padx=(0,99), pady=5, sticky="w")

        #BY SEX
        self.sex_button=tk.Button(self.frame,text="Filter By Sex",font=("Verdana", 10),command=self.on_sex_click)
        self.sex_button.place(relx=0.81, rely=0.08)
        #self.sex_button.grid(row=1, column=, padx=(0,99), pady=5, sticky="w")
        
        
        #CANVAS FOR UPCOMING REQUESTS
        self.canvas = tk.Canvas(self.frame,width=675,height=340)
        self.canvas.grid(row=4, column=0,columnspan=2)
        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=4, column=3, sticky="ns")
        scrollbar2 = tk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        scrollbar2.grid(row=17, column=0,columnspan=9, sticky="ew")
        self.inner_frame = tk.Frame(self.canvas,height=160)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.display_reviews()
        
    def display_reviews(self):
            connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cur = connection.cursor()
            query= """SELECT U.Username,R.* 
                FROM Review R INNER JOIN User U ON R.U_id = U.U_id 
                WHERE R.M_id=%s 
                ORDER BY Rating ASC"""
            cur.execute(query, (str(M_id),))
            result=cur.fetchall()
            connection.close()
            self.display_result(result)
    
    def sort_by_rating_desc(self):
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        query= """SELECT U.Username,R.* 
            FROM Review R INNER JOIN User U ON R.U_id = U.U_id 
            WHERE R.M_id=%s 
            ORDER BY Rating DESC"""
        cur.execute(query, (str(M_id),))
        result=cur.fetchall()
        connection.close()
        self.display_result(result)
        
    def sort_by_session(self):
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        query= """SELECT U.Username, R.*, COUNT(A.U_id) AS session_count
                FROM Review R
                INNER JOIN User U ON R.U_id = U.U_id
                LEFT JOIN Appointment A ON R.U_id = A.U_id AND A.M_id = %s
                WHERE R.M_id = %s
                GROUP BY R.U_id,R.M_id
                ORDER BY session_count DESC, R.Date"""
        cur.execute(query, (str(M_id),str(M_id),))
        result=cur.fetchall()
        print(result)
        connection.close()
        if result:
                header_label1 = tk.Label(self.inner_frame, text="Username",font=("Verdana", 10))
                header_label1.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="w")
                header_label2 = tk.Label(self.inner_frame, text="Date",font=("Verdana", 10))
                header_label2.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky="w")
                header_label3 = tk.Label(self.inner_frame, text="Title",font=("Verdana", 10))
                header_label3.grid(row=1, column=2, padx=5, pady=5, columnspan=3, sticky="w")
                header_label4 = tk.Label(self.inner_frame, text="Comment",font=("Verdana", 10))
                header_label4.grid(row=1, column=3, padx=5, pady=5, columnspan=3, sticky="w")
                header_label5 = tk.Label(self.inner_frame, text="Rating",font=("Verdana", 10))
                header_label5.grid(row=1, column=4, padx=(5,20), pady=5, columnspan=3, sticky="w")
                header_label6 = tk.Label(self.inner_frame, text="No. of Sessions",font=("Verdana", 10))
                header_label6.grid(row=1, column=5, padx=(20,0), pady=5, columnspan=3, sticky="w")
                row_no=2
                for row in result:
                    label1 = tk.Label(self.inner_frame, text=f"{row[0]}", bg="white",font=("Verdana", 10))
                    label1.grid(row=row_no, column=0, padx=5, pady=5, rowspan=2, sticky="w")
                    label2 = tk.Label(self.inner_frame, text=f"{row[3]}", bg="white",font=("Verdana", 10))
                    label2.grid(row=row_no, column=1, padx=5, pady=5, rowspan=2, sticky="w")
                    label3 = tk.Label(self.inner_frame, text=f"{row[4]}", bg="white",font=("Verdana", 10))
                    label3.grid(row=row_no, column=2, padx=5, pady=5, rowspan=2, sticky="w")
                    label4 = tk.Label(self.inner_frame, text=f"{row[5]}", bg="white",font=("Verdana", 10))
                    label4.grid(row=row_no, column=3, padx=5, pady=5, rowspan=2, sticky="w")
                    label5 = tk.Label(self.inner_frame, text=f"{row[6]}", bg="white",font=("Verdana", 10))
                    label5.grid(row=row_no, column=4, padx=(5,20), pady=5, rowspan=2, sticky="e")
                    label6 = tk.Label(self.inner_frame, text=f"{row[7]}", bg="white",font=("Verdana", 10))
                    label6.grid(row=row_no, column=5, padx=(20,0), pady=5, rowspan=2, sticky="w")
                    row_no+=2   
        else:
                no_appointments_label = tk.Label(self.inner_frame, text="No Reviews yet :(", font=("Verdana", 10))
                no_appointments_label.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="w") 
        
    def sort_by_time(self):
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        query= "CALL GetReviewsByTime(%s)"
        cur.execute(query, (str(M_id),))
        result=cur.fetchall()
        connection.close()
        if result:
                header_label1 = tk.Label(self.inner_frame, text="Username",font=("Verdana", 10))
                header_label1.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="w")
                header_label2 = tk.Label(self.inner_frame, text="Date",font=("Verdana", 10))
                header_label2.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky="w")
                header_label3 = tk.Label(self.inner_frame, text="Title",font=("Verdana", 10))
                header_label3.grid(row=1, column=2, padx=5, pady=5, columnspan=3, sticky="w")
                header_label4 = tk.Label(self.inner_frame, text="Comment",font=("Verdana", 10))
                header_label4.grid(row=1, column=3, padx=5, pady=5, columnspan=3, sticky="w")
                header_label5 = tk.Label(self.inner_frame, text="Rating",font=("Verdana", 10))
                header_label5.grid(row=1, column=4, padx=(5,20), pady=5, columnspan=3, sticky="w")
                header_label6 = tk.Label(self.inner_frame, text="Time Interval",font=("Verdana", 10))
                header_label6.grid(row=1, column=5, padx=(20,0), pady=5, columnspan=3, sticky="w")
                row_no=2
                for row in result:
                    label1 = tk.Label(self.inner_frame, text=f"{row[0]}", bg="white",font=("Verdana", 10))
                    label1.grid(row=row_no, column=0, padx=5, pady=5, rowspan=2, sticky="w")
                    label2 = tk.Label(self.inner_frame, text=f"{row[3]}", bg="white",font=("Verdana", 10))
                    label2.grid(row=row_no, column=1, padx=5, pady=5, rowspan=2, sticky="w")
                    label3 = tk.Label(self.inner_frame, text=f"{row[4]}", bg="white",font=("Verdana", 10))
                    label3.grid(row=row_no, column=2, padx=5, pady=5, rowspan=2, sticky="w")
                    label4 = tk.Label(self.inner_frame, text=f"{row[5]}", bg="white",font=("Verdana", 10))
                    label4.grid(row=row_no, column=3, padx=5, pady=5, rowspan=2, sticky="w")
                    label5 = tk.Label(self.inner_frame, text=f"{row[6]}", bg="white",font=("Verdana", 10))
                    label5.grid(row=row_no, column=4, padx=(5,20), pady=5, rowspan=2, sticky="e")
                    label6 = tk.Label(self.inner_frame, text=f"{row[7]}", bg="white",font=("Verdana", 10))
                    label6.grid(row=row_no, column=5, padx=(20,0), pady=5, rowspan=2, sticky="w")
                    row_no+=2   
        else:
                no_appointments_label = tk.Label(self.inner_frame, text="No Reviews yet :(", font=("Verdana", 10))
                no_appointments_label.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="w")
        
    def sort_by_age(self):
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        query= """SELECT U.Username, R.*, U.Age,
                    CASE
                        WHEN U.Age < 18 THEN 'Below 18'
                        WHEN U.Age >= 18 AND U.Age <= 30 THEN '18 to 30'
                        WHEN U.Age > 30 AND U.Age <= 50 THEN '30 to 50'
                        ELSE 'Above 50'
                    END AS age_category
                FROM (
                    SELECT R.*
                    FROM Review R
                    WHERE M_id = %s
                ) R
                INNER JOIN User U ON R.U_id = U.U_id
                ORDER BY
                    CASE
                        WHEN U.Age < 18 THEN 1
                        WHEN U.Age >= 18 AND U.Age <= 30 THEN 2
                        WHEN U.Age > 30 AND U.Age <= 50 THEN 3
                        ELSE 4
                    END
                """
        cur.execute(query, (str(M_id),))
        result=cur.fetchall()
        connection.close()
        if result:
                header_label1 = tk.Label(self.inner_frame, text="Username",font=("Verdana", 10))
                header_label1.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="w")
                header_label2 = tk.Label(self.inner_frame, text="Date",font=("Verdana", 10))
                header_label2.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky="w")
                header_label3 = tk.Label(self.inner_frame, text="Title",font=("Verdana", 10))
                header_label3.grid(row=1, column=2, padx=5, pady=5, columnspan=3, sticky="w")
                header_label4 = tk.Label(self.inner_frame, text="Comment",font=("Verdana", 10))
                header_label4.grid(row=1, column=3, padx=5, pady=5, columnspan=3, sticky="w")
                header_label5 = tk.Label(self.inner_frame, text="Rating",font=("Verdana", 10))
                header_label5.grid(row=1, column=4, padx=(5,20), pady=5, columnspan=3, sticky="w")
                header_label6 = tk.Label(self.inner_frame, text="Age",font=("Verdana", 10))
                header_label6.grid(row=1, column=5, padx=(20,10), pady=5, columnspan=3, sticky="w")
                header_label7 = tk.Label(self.inner_frame, text="Age Category",font=("Verdana", 10))
                header_label7.grid(row=1, column=6, padx=(10,0), pady=5, columnspan=3, sticky="w")
                row_no=2
                for row in result:
                    label1 = tk.Label(self.inner_frame, text=f"{row[0]}", bg="white",font=("Verdana", 10))
                    label1.grid(row=row_no, column=0, padx=5, pady=5, rowspan=2, sticky="w")
                    label2 = tk.Label(self.inner_frame, text=f"{row[3]}", bg="white",font=("Verdana", 10))
                    label2.grid(row=row_no, column=1, padx=5, pady=5, rowspan=2, sticky="w")
                    label3 = tk.Label(self.inner_frame, text=f"{row[4]}", bg="white",font=("Verdana", 10))
                    label3.grid(row=row_no, column=2, padx=5, pady=5, rowspan=2, sticky="w")
                    label4 = tk.Label(self.inner_frame, text=f"{row[5]}", bg="white",font=("Verdana", 10))
                    label4.grid(row=row_no, column=3, padx=5, pady=5, rowspan=2, sticky="w")
                    label5 = tk.Label(self.inner_frame, text=f"{row[6]}", bg="white",font=("Verdana", 10))
                    label5.grid(row=row_no, column=4, padx=(5,20), pady=5, rowspan=2, sticky="e")
                    label6 = tk.Label(self.inner_frame, text=f"{row[7]}", bg="white",font=("Verdana", 10))
                    label6.grid(row=row_no, column=5, padx=(20,10), pady=5, rowspan=2, sticky="w")
                    label7 = tk.Label(self.inner_frame, text=f"{row[8]}", bg="white",font=("Verdana", 10))
                    label7.grid(row=row_no, column=6, padx=(10,0), pady=5, rowspan=2, sticky="w")
                    row_no+=2   
        else:
                no_appointments_label = tk.Label(self.inner_frame, text="No Reviews yet :(", font=("Verdana", 10))
                no_appointments_label.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="w")                  
    def sort_by_sex(self):
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        query= """SELECT U.Username, R.*, U.Sex
                   FROM Review R
                   INNER JOIN User U ON R.U_id = U.U_id
                   WHERE R.M_id = %s
                   ORDER BY U.Sex
                """
        cur.execute(query, (str(M_id),))
        result=cur.fetchall()
        connection.close()
        if result:
                header_label1 = tk.Label(self.inner_frame, text="Username",font=("Verdana", 10))
                header_label1.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="w")
                header_label2 = tk.Label(self.inner_frame, text="Date",font=("Verdana", 10))
                header_label2.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky="w")
                header_label3 = tk.Label(self.inner_frame, text="Title",font=("Verdana", 10))
                header_label3.grid(row=1, column=2, padx=5, pady=5, columnspan=3, sticky="w")
                header_label4 = tk.Label(self.inner_frame, text="Comment",font=("Verdana", 10))
                header_label4.grid(row=1, column=3, padx=5, pady=5, columnspan=3, sticky="w")
                header_label5 = tk.Label(self.inner_frame, text="Rating",font=("Verdana", 10))
                header_label5.grid(row=1, column=4, padx=(5,20), pady=5, columnspan=3, sticky="w")
                header_label6 = tk.Label(self.inner_frame, text="Sex",font=("Verdana", 10))
                header_label6.grid(row=1, column=5, padx=(20,10), pady=5, columnspan=3, sticky="w")
                row_no=2
                for row in result:
                    label1 = tk.Label(self.inner_frame, text=f"{row[0]}", bg="white",font=("Verdana", 10))
                    label1.grid(row=row_no, column=0, padx=5, pady=5, rowspan=2, sticky="w")
                    label2 = tk.Label(self.inner_frame, text=f"{row[3]}", bg="white",font=("Verdana", 10))
                    label2.grid(row=row_no, column=1, padx=5, pady=5, rowspan=2, sticky="w")
                    label3 = tk.Label(self.inner_frame, text=f"{row[4]}", bg="white",font=("Verdana", 10))
                    label3.grid(row=row_no, column=2, padx=5, pady=5, rowspan=2, sticky="w")
                    label4 = tk.Label(self.inner_frame, text=f"{row[5]}", bg="white",font=("Verdana", 10))
                    label4.grid(row=row_no, column=3, padx=5, pady=5, rowspan=2, sticky="w")
                    label5 = tk.Label(self.inner_frame, text=f"{row[6]}", bg="white",font=("Verdana", 10))
                    label5.grid(row=row_no, column=4, padx=(5,20), pady=5, rowspan=2, sticky="e")
                    label6 = tk.Label(self.inner_frame, text=f"{row[7]}", bg="white",font=("Verdana", 10))
                    label6.grid(row=row_no, column=5, padx=(20,0), pady=5, rowspan=2, sticky="w")
                    row_no+=2   
        else:
                no_appointments_label = tk.Label(self.inner_frame, text="No Reviews yet :(", font=("Verdana", 10))
                no_appointments_label.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="w")   
      
    def display_result(self,result):
        if result:
                header_label1 = tk.Label(self.inner_frame, text="Username",font=("Verdana", 10))
                header_label1.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="w")
                header_label2 = tk.Label(self.inner_frame, text="Date",font=("Verdana", 10))
                header_label2.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky="w")
                header_label3 = tk.Label(self.inner_frame, text="Title",font=("Verdana", 10))
                header_label3.grid(row=1, column=2, padx=5, pady=5, columnspan=3, sticky="w")
                header_label4 = tk.Label(self.inner_frame, text="Comment",font=("Verdana", 10))
                header_label4.grid(row=1, column=3, padx=5, pady=5, columnspan=3, sticky="w")
                header_label5 = tk.Label(self.inner_frame, text="Rating",font=("Verdana", 10))
                header_label5.grid(row=1, column=4, padx=5, pady=5, columnspan=3, sticky="w")
                row_no=2
                for row in result:
                    label1 = tk.Label(self.inner_frame, text=f"{row[0]}", bg="white",font=("Verdana", 10))
                    label1.grid(row=row_no, column=0, padx=5, pady=5, rowspan=2, sticky="w")
                    label2 = tk.Label(self.inner_frame, text=f"{row[3]}", bg="white",font=("Verdana", 10))
                    label2.grid(row=row_no, column=1, padx=5, pady=5, rowspan=2, sticky="w")
                    label3 = tk.Label(self.inner_frame, text=f"{row[4]}", bg="white",font=("Verdana", 10))
                    label3.grid(row=row_no, column=2, padx=5, pady=5, rowspan=2, sticky="w")
                    label4 = tk.Label(self.inner_frame, text=f"{row[5]}", bg="white",font=("Verdana", 10))
                    label4.grid(row=row_no, column=3, padx=5, pady=5, rowspan=2, sticky="w")
                    label5 = tk.Label(self.inner_frame, text=f"{row[6]}", bg="white",font=("Verdana", 10))
                    label5.grid(row=row_no, column=4, padx=5, pady=5, rowspan=2, sticky="w")
                    row_no+=2   
        else:
                no_appointments_label = tk.Label(self.inner_frame, text="No Reviews yet :(", font=("Verdana", 10))
                no_appointments_label.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="w") 
        
        
                
    def on_click(self):
        self.canvas.delete("all")
        self.canvas = tk.Canvas(self.frame,width=675,height=350)
        self.canvas.grid(row=2, column=0,columnspan=2)
        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=2, column=3, sticky="ns")
        scrollbar2 = tk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        scrollbar2.grid(row=15, column=0,columnspan=9, sticky="ew")
        self.inner_frame = tk.Frame(self.canvas,height=160)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        
        
    def on_rating_click(self):
        self.on_click()
        self.sort_by_rating_desc()
        
    def on_session_click(self):
        self.on_click()
        self.sort_by_session()
        
    def on_time_click(self):
        self.on_click()
        self.sort_by_time()
        
    def on_age_click(self):
        self.on_click()
        self.sort_by_age()
        
    def on_sex_click(self):
        self.on_click()
        self.sort_by_sex()
        
    def go_to_home(self):
        subprocess.Popen(["python", "MHPHomePage.py", M_id])  
        self.destroy()
            

if __name__=="__main__":
    M_id = sys.argv[1]
    if M_id is not None:
      M_id = str(M_id)
    #M_id="1"
    app=MHPReview(M_id)
    app.mainloop()
    


