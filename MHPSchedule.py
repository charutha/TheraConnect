import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess
import sys
import mysql.connector
import credentials as cr
from PIL import Image, ImageTk
from tkinter import Label, PhotoImage
class MHPSchedule(tk.Tk):
    def __init__(self, M_id):
        super().__init__()
        self.title("TheraConnect-MHP Schedule")
        self.geometry("950x600")
        self.bg_img = ImageTk.PhotoImage(file="mhp1.png")
        background = Label(self,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)
        #self.eval('tk::PlaceWindow . center')
        self.header_label = tk.Label(self, text="Your Schedule for the next 5 days!", font=("Verdana", 14))
        self.header_label.place(relx=0.5, rely=0.01, anchor="n")
        
        self.back_button = tk.Button(self, text="<- Back", font=("Verdana", 10),command=self.go_to_home)
        self.back_button.place(relx=0.1, rely=0.01, anchor="n")
        
        self.frame1 = tk.Frame(self, bg="white", bd=4)
        self.frame1.place(relx=0.05, rely=0.1, relwidth=0.85, relheight=0.55)
        
        self.frame2 = tk.Frame(self, bg="white", bd=4)
        self.frame2.place(relx=0.05, rely=0.66, relwidth=0.85, relheight=0.33)
          
        self.date_label = tk.Label(self.frame2,text="Choose Date",bg="white")
        self.date_label.grid(row=0, column=0, sticky="w")
  
     
        self.slot_label = tk.Label(self.frame2,text="Choose Slot",bg="white")
        self.slot_label.grid(row=0, column=2, padx=10, sticky="w")

        self.action_label = tk.Label(self.frame2,text="Choose Action",bg="white")
        self.action_label.grid(row=0, column=4, padx=10, sticky="w")
        
        self.apply_button = tk.Button(self.frame2, text="Apply", font=("Verdana", 10),command=self.apply_effect)
        self.apply_button.grid(row=4, column=4 ,sticky="w")
        
        self.canvas = tk.Canvas(self.frame1, width=800, height=800)
        self.canvas.pack()
        self.viewschedule()
        
        self.action_entry = [str(action) for action in ["Make Slot Available","Make Slot Unavailable"]]
        self.action_entry= ttk.Combobox(self.frame2, values=self.action_entry, width=15,state="readonly")
        self.action_entry.set("Select an Action")
        self.action_entry.grid(row=2, column=4,sticky="w")
        
        self.all_slot_button = tk.Button(self.frame2, text="All slots", font=("Verdana", 10),command=self.check_all_slots)
        self.all_slot_button.grid(row=4, column=0,sticky="w")
        
        self.date_entry = [str(date) for date in self.Dates]
        self.date_entry= ttk.Combobox(self.frame2, values=self.date_entry, width=15,state="readonly")
        self.date_entry.set("Select a Date")
        self.date_entry.grid(row=2, column=0,sticky="w")
        
        self.slot1 = tk.IntVar()
        self.slot2 = tk.IntVar()
        self.slot3 = tk.IntVar()
        self.slot4 = tk.IntVar()
        self.slot5 = tk.IntVar()
        self.slot6 = tk.IntVar()
        self.slot7 = tk.IntVar()
        self.slot8 = tk.IntVar()
        
        self.checkboxes = []
        options = ["9_10AM", "10_11AM", "11_12AM", "12_1PM", "1_2PM", "2_3PM", "3_4PM", "4_5PM"]
        row=2
        #CREATE CHECK BOXES
        for row, option in enumerate(options):
            checkbox = tk.Checkbutton(self.frame2, text=option, variable=self.get_variable(option), bg="white", font=("Verdana", 7))
            self.checkboxes.append(checkbox)
            checkbox.grid(row=row + 1, column=2, padx=10, sticky="w")
        
    
    def apply_effect(self):
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        
        
        selected_date = self.date_entry.get()
        selected_action = self.action_entry.get()
        selected_slots = [self.slot1.get(),self.slot2.get(),self.slot3.get(),self.slot4.get(),self.slot5.get(),self.slot6.get(),self.slot7.get(),self.slot8.get()]
        final_selected_slots=[]
        options = ["9_10AM", "10_11AM", "11_12AM", "12_1PM", "1_2PM", "2_3PM", "3_4PM", "4_5PM"]
        for i in range (len(selected_slots)):
            if selected_slots[i]==1:
                final_selected_slots.append(options[i])
        final_selected_slots = ','.join([x for x in final_selected_slots])
    
        if selected_action=="Make Slot Unavailable":
            query1=""" UPDATE Schedule AS s
                        SET 
                            s.9_10AM = CASE WHEN FIND_IN_SET('9_10AM', %s) > 0 THEN 1 ELSE s.9_10AM END,
                            s.10_11AM = CASE WHEN FIND_IN_SET('10_11AM',%s) > 0 THEN 1 ELSE s.10_11AM END,
                            s.11_12AM = CASE WHEN FIND_IN_SET('11_12AM', %s) > 0 THEN 1 ELSE s.11_12AM END,
                            s.12_1PM = CASE WHEN FIND_IN_SET('12_1PM', %s) > 0 THEN 1 ELSE s.12_1PM END,
                            s.1_2PM = CASE WHEN FIND_IN_SET('1_2PM', %s) > 0 THEN 1 ELSE s.1_2PM END,
                            s.2_3PM = CASE WHEN FIND_IN_SET('2_3PM', %s) > 0 THEN 1 ELSE s.2_3PM END,
                            s.3_4PM = CASE WHEN FIND_IN_SET('3_4PM', %s) > 0 THEN 1 ELSE s.3_4PM END,
                            s.4_5PM = CASE WHEN FIND_IN_SET('4_5PM', %s) > 0 THEN 1 ELSE s.4_5PM END
                        WHERE
                            s.M_id = %s AND s.Date = %s"""
            cur.execute(query1, (final_selected_slots,final_selected_slots,final_selected_slots,final_selected_slots,final_selected_slots,final_selected_slots,final_selected_slots,final_selected_slots, M_id, selected_date))
            connection.commit()
                        
            query2="""UPDATE Appointment AS a
                        SET a.Status = 'Cancelled'
                        WHERE
                            a.M_id = %s 
                            AND a.Date = %s
                            AND TIME(a.Start_time) IN (
                                SELECT 
                                    CASE 
                                        WHEN s.9_10AM = 1 THEN '09:00:00' 
                                        WHEN s.10_11AM = 1 THEN '10:00:00' 
                                        WHEN s.11_12AM = 1 THEN '11:00:00' 
                                        WHEN s.12_1PM = 1 THEN '12:00:00' 
                                        WHEN s.1_2PM = 1 THEN '13:00:00' 
                                        WHEN s.2_3PM = 1 THEN '14:00:00' 
                                        WHEN s.3_4PM = 1 THEN '15:00:00' 
                                        WHEN s.4_5PM = 1 THEN '16:00:00' 
                                    END AS slot_time
                                FROM Schedule AS s
                                WHERE
                                    s.M_id = a.M_id
                                    AND s.Date = a.Date
                                    AND (s.9_10AM = 1 OR s.10_11AM = 1 OR s.11_12AM = 1 OR s.12_1PM = 1 OR s.1_2PM = 1 OR s.2_3PM = 1 OR s.3_4PM = 1 OR s.4_5PM = 1)
                            )"""
                            
            cur.execute(query2, (M_id, selected_date))
            connection.commit()
            connection.close()
        else:
            query1=""" UPDATE Schedule AS s
                        SET 
                            s.9_10AM = CASE WHEN FIND_IN_SET('9_10AM', %s) > 0 THEN 0 ELSE s.9_10AM END,
                            s.10_11AM = CASE WHEN FIND_IN_SET('10_11AM',%s) > 0 THEN 0 ELSE s.10_11AM END,
                            s.11_12AM = CASE WHEN FIND_IN_SET('11_12AM', %s) > 0 THEN 0 ELSE s.11_12AM END,
                            s.12_1PM = CASE WHEN FIND_IN_SET('12_1PM', %s) > 0 THEN 0 ELSE s.12_1PM END,
                            s.1_2PM = CASE WHEN FIND_IN_SET('1_2PM', %s) > 0 THEN 0 ELSE s.1_2PM END,
                            s.2_3PM = CASE WHEN FIND_IN_SET('2_3PM', %s) > 0 THEN 0 ELSE s.2_3PM END,
                            s.3_4PM = CASE WHEN FIND_IN_SET('3_4PM', %s) > 0 THEN 0 ELSE s.3_4PM END,
                            s.4_5PM = CASE WHEN FIND_IN_SET('4_5PM', %s) > 0 THEN 0 ELSE s.4_5PM END
                        WHERE
                            s.M_id = %s AND s.Date = %s"""
            cur.execute(query1, (final_selected_slots,final_selected_slots,final_selected_slots,final_selected_slots,final_selected_slots,final_selected_slots,final_selected_slots,final_selected_slots, M_id, selected_date))
            connection.commit()
                        
            query2="""UPDATE Appointment AS a
                    SET a.Status = 'Pending'
                    WHERE
                        a.M_id = %s 
                        AND a.Date = %s
                        AND a.Status = 'Upcoming' or a.Status= 'Cancelled'
                        AND TIME(a.Start_time) IN (
                            SELECT 
                                CASE 
                                    WHEN s.9_10AM = 1 THEN '09:00:00' 
                                    WHEN s.10_11AM = 1 THEN '10:00:00' 
                                    WHEN s.11_12AM = 1 THEN '11:00:00' 
                                    WHEN s.12_1PM = 1 THEN '12:00:00' 
                                    WHEN s.1_2PM = 1 THEN '13:00:00' 
                                    WHEN s.2_3PM = 1 THEN '14:00:00' 
                                    WHEN s.3_4PM = 1 THEN '15:00:00' 
                                    WHEN s.4_5PM = 1 THEN '16:00:00' 
                                END AS slot_time
                            FROM Schedule AS s
                            WHERE
                                s.M_id = a.M_id
                                AND s.Date = a.Date
                                AND (s.9_10AM = 1 OR s.10_11AM = 1 OR s.11_12AM = 1 OR s.12_1PM = 1 OR s.1_2PM = 1 OR s.2_3PM = 1 OR s.3_4PM = 1 OR s.4_5PM = 1)
                        )
                        AND TIME(a.Start_time) IN (
                            SELECT slot_time
                            FROM (
                                SELECT 
                                    CASE 
                                        WHEN s.9_10AM = 1 THEN '09:00:00' 
                                        WHEN s.10_11AM = 1 THEN '10:00:00' 
                                        WHEN s.11_12AM = 1 THEN '11:00:00' 
                                        WHEN s.12_1PM = 1 THEN '12:00:00' 
                                        WHEN s.1_2PM = 1 THEN '13:00:00' 
                                        WHEN s.2_3PM = 1 THEN '14:00:00' 
                                        WHEN s.3_4PM = 1 THEN '15:00:00' 
                                        WHEN s.4_5PM = 1 THEN '16:00:00' 
                                    END AS slot_time
                                FROM Schedule AS s
                                WHERE
                                    s.M_id = a.M_id
                                    AND s.Date = a.Date
                                    AND (s.9_10AM = 1 OR s.10_11AM = 1 OR s.11_12AM = 1 OR s.12_1PM = 1 OR s.1_2PM = 1 OR s.2_3PM = 1 OR s.3_4PM = 1 OR s.4_5PM = 1)
                            ) AS slot_times
                            WHERE slot_time = TIME(a.Start_time) AND slot_times.slot_time = '09:00:00'
                        );"""
            cur.execute(query2, (M_id, selected_date))
            connection.commit()
            connection.close()
            
        #RENEW CHECKBOXES AND DROP DOWN LIST
        self.date_entry.set("Select Date")
        self.action_entry.set("Select an Action")
        for checkbox in self.checkboxes:
            checkbox.deselect()
        self.canvas.delete("all")
        self.viewschedule()

        
    
    def check_all_slots(self):
        for checkbox in self.checkboxes:
            checkbox.select()

            
    def get_variable(self, option):
        return {
            "9_10AM": self.slot1,
            "10_11AM": self.slot2,
            "11_12AM": self.slot3,
            "12_1PM": self.slot4,
            "1_2PM": self.slot5,
            "2_3PM": self.slot6,
            "3_4PM": self.slot7,
            "4_5PM": self.slot8
        }[option]
        
    def viewschedule(self):
        connection = mysql.connector.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()
        query= "SELECT * FROM Schedule WHERE M_id = %s"
        cur.execute(query, (str(M_id),))
        result = cur.fetchall()
        connection.close()
        
        for i in range (len(result)):
            result[i]=list(result[i][1:])
        self.availability_data=list(result)

        #dates list
        self.Dates=[]
        for i in range (len(result)):
            self.Dates.append(self.availability_data[i][1])
        self.Dates=tuple(self.Dates)

        self.cell_objects = []
       
        header_row = ["Day", "Date", "9_10AM", "10_11AM", "11_12AM", "12_1PM", "1_2PM", "2_3PM", "3_4PM", "4_5PM"]
        for col, header in enumerate(header_row):
            x1 = col * 75
            y1 = 0
            x2 = x1 + 75
            y2 = y1 + 50
            cell_rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray")
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=header)

        # Create the table rows and cells
        for row, data_row in enumerate(self.availability_data):
            self.cell_objects.append([])
            for col, cell_data in enumerate(data_row):
                x1 = col * 75
                y1 = (row + 1) * 50
                x2 = x1 + 75
                y2 = y1 + 50
                cell_rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
                self.cell_objects[row].append(cell_rect)  # Store the cell object
                self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(cell_data))
        self.update_colours()

    
            
    def update_colours(self):
            for row in range(len(self.availability_data)):
                for col in range(len(self.availability_data[0])):
                    if col >= 2:  # Skip the first two columns (Date and Day)
                        if self.availability_data[row][col] == 1:
                            #cell_color = "#b48080"
                            cell_color = "#71A6D2"  # Not available
                        else:
                            cell_color = "white"  # Available
                        self.canvas.itemconfig(self.cell_objects[row][col], fill=cell_color)
    
    def go_to_home(self):
             subprocess.Popen(["python", "MHPHomePage.py", M_id])  
             self.destroy()             
                        

if __name__=="__main__":
    M_id = sys.argv[1]
    if M_id is not None:
      M_id = str(M_id)
    #M_id="1"
    app=MHPSchedule(M_id)
    app.mainloop()