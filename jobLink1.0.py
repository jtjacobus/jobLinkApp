from tkinter import *
import tkinter.messagebox as tm
import pymysql
from PIL import ImageTk
#import jL_Layout




class AppFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        root.geometry("480x800")
        root.configure(background="#34495E")
        root.title("Job Scheduler")

        self.label_username = Label(self, text="Username", font="candara 18", background="#d6dbdf")
        self.entry_username = Entry(self, font="candara 18", background="#aab7b8")

        self.label_username.grid(row=0, sticky=E, padx=2, pady=2)
        self.entry_username.grid(row=0, column=1, padx=2, pady=2)

        self.logbtn = Button(self, height=1, width=10, text="Login", font="candara 12 bold", command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=2)

        self.pack(padx=20,pady=320)


    def my_jobs_frame(root, username, u_type_ID, user_type):
        root = Tk()
        root.title(username + "'s Jobs:")  # text shown at top of window
        root.geometry("480x800")  # window size
        root.configure(background="#34495E")
        #photo_g = PhotoImage(file="green_house3.png")
        conn = pymysql.connect(host='localhost', user='root', password='########', db='#####')
        a = conn.cursor()
        sql = 'SELECT * FROM assigned_jobs;'
        a.execute(sql)
        data = a.fetchall()
        data_tuples = []
        if user_type == "technician":
            AppFrame._technician_jobs(data, data_tuples, u_type_ID)
            a.close()
            conn.close()
            user_label = Label(root,bg="#aab7b8",bd=0,width=40,font="helvetica 14 bold",fg="#34495E",text="Welcome "+username).grid(row=0,column=0,columnspan=4,sticky=E,padx=0,pady=0)
            my_jobs_label = Label(root, bg="#34495E", bd=0,font="helvetica 12 bold", fg="white",text="My Jobs: ").grid(row=1, column=0, sticky=W, padx=2, pady=8)
            my_stats_label = Label(root, bg="#34495E", bd=0, font="helvetica 12 bold", fg="white",text="My Stats: ").grid(row=1, column=2, sticky=W, padx=2, pady=8)
            for item in data_tuples:  # selects tuples and creates buttons with location.Street
                button_color = "#d4efdf"
                if item[1] == "In Progress":
                    button_color = "#f9e79f"
                elif item[1] == "Sheduled" or item[1] == "Unassigned":
                    button_color = "#cd6155"
                button = Button(root, bg=button_color, text=item[3],font="helvetica 12", command=lambda item=item: AppFrame._job_btn_clicked(root, item), compound="left", height=1, width=20)
                button.grid(padx=4, pady=4)  #something with the image is not working, and buttons need resized
        elif user_type == "admin":
            AppFrame._admin_jobs(data, data_tuples, u_type_ID)
            a.close()
            conn.close()
            for item in data_tuples:
                button_color = "#d4efdf"
                if item[1] == "In Progress":
                    button_color = "#f9e79f"
                elif item[1] == "Sheduled" or item[1] == "Unassigned":
                    button_color = "#cd6155"
                button = Button(root,bg=button_color, text=item[3],font="helvetica 12", command=lambda item=item: AppFrame._job_btn_clicked(root, item), compound="left", height=1, width=20)
                button.pack(padx=4, pady=4)  #something with the image is not working, and buttons need resized
        elif user_type == "client":
            AppFrame._client_jobs(data, data_tuples, u_type_ID)
            a.close()
            conn.close()
            for item in data_tuples:
                button_color = "#d4efdf"
                if item[1] == "In Progress":
                    button_color = "#f9e79f"
                elif item[1] == "Sheduled" or item[1] == "Unassigned":
                    button_color = "#cd6155"
                button = Button(root,bg=button_color,text=item[3],font="helvetica 12", command=lambda item=item: AppFrame._job_btn_clicked(root, item), compound="left", height=1, width=20)
                button.pack(padx=4, pady=4)  #something with the image is not working, and buttons need resized


    def _login_btn_clicked(self):
        """Submits username that is entered to the database and checks for a match,
        then returns the user_id that is found for that username. """
        username = self.entry_username.get()
        conn = pymysql.connect(host='localhost', user='root', password='######', db='#####')
        with conn:
            a = conn.cursor()
            a.execute('SELECT User_ID FROM user WHERE UserName = %s;',(username))
        user_data = a.fetchall()
        a.close()
        conn.close()
        if user_data == ():
            tm.showerror("Login error", "Incorrect username")
        else:
            found_user = AppFrame._format_data(user_data) #User_ID
            u_type_ID = (AppFrame._check_user_type(found_user)[0]) #(user_type)_ID
            user_type = (AppFrame._check_user_type(found_user)[1])
            AppFrame.my_jobs_frame(root,username, u_type_ID, user_type)


    def _job_btn_clicked(root, item):
        """Selects job tuple from database to populate specific job screen."""
        root = Tk()
        root.title(item[3])  # text shown at top of window
        root.geometry("480x800")  # window size
        root.configure(background="#34495E")
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1,weight=1)
        status_color = "#d4efdf"
        pay = "$"+str(item[6])
        start_date = str(item[5])
        if item[1] == "In Progress":
            status_color = "#f9e79f"
        elif item[1] == "Sheduled" or item[1] == "Unassigned":
            status_color = "#cd6155"
        start_color = "#cd6155"
        if item[1] == "In Progress" or item[1] == "Complete":
            start_color = "white"
        ins_text = "Remove existing cabinets and countertops. Dispose of. Install new cabinets and countertops to plan." #remove, only for testing
        job_id_label = Label(root, bg="#34495E", bd=0, font="helvetica 18 bold", fg=status_color, text=" "+str(item[0])).grid(row=0, column=0, sticky=W, padx=5, pady=20)
        company_label = Label(root, bg="#34495E", bd=0, font="helvetica 12 bold", fg="white", text=item[2]).grid(row=0, column=1, sticky=W, padx=20, pady=20)
        job_type_label = Label(root, bg="#34495E", bd=0, font="helvetica 12 bold", fg="white", text=item[4]).grid(row=0, column=2, sticky=W, padx=20, pady=20)
        job_name_label = Label(root, bg="#34495E", bd=0, font="helvetica 27 bold", fg=status_color, text=item[3]).grid(row=1, column=0, columnspan=3, sticky=W, padx=5, pady=5)
        job_status_label = Label(root, bg="#34495E", bd=0, font="helvetica 12 bold", fg= status_color, text="Status: "+item[1]).grid(row=2, column=1, sticky=W, padx=20, pady=5)
        status_button = Button(root, bg="#d4efdf", text="COMPLETE", font="helvetica 12",command=lambda item=item: AppFrame._status_btn_clicked(root,item),height=1,width=15)\
            .grid(row=2, column=2, sticky=W, padx=20, pady=5)
        start_date_label = Label(root, bg="#34495E", bd=0, font="helvetica 12 bold", fg= start_color, text="Start Date: "+start_date).grid(row=3, column=1, sticky=W, padx=20, pady=5)
        pay_label = Label(root, bg="#34495E", bd=0, font="helvetica 12 bold", fg="white",text="Pay: " + pay).grid(row=3, column=2, sticky=W, padx=20, pady=5)
        instructions = Label(root, bg="white", bd=5, font="helvetica 10", fg="black", text=ins_text, height=20, width=20, wraplength=450, justify=LEFT)\
            .grid(row=4, column=0, columnspan=3, padx=15, pady=30, sticky=W+E)


    def _status_btn_clicked(root, item):
        """Changes status on status button"""
        sql_status_update = 'UPDATE job SET Job_Status = "Complete" WHERE Job_ID = '+str(item[0])+';'
        print (sql_status_update)
        conn = pymysql.connect(host='localhost', user='root', password='#######', db='######')
        a = conn.cursor()
        a.execute(sql_status_update)
        conn.commit()
        a.close()
        conn.close()



    def _check_user_type(found_user):
        """Checks tech, admin, client tables for existence of username. If exists, returns specific id."""
        tech_check = 'SELECT Tech_ID FROM technician WHERE User_ID = ' + str(found_user) + ';'
        admin_check = 'SELECT Admin_ID FROM admin WHERE User_ID = ' + str(found_user) + ';'
        client_check = 'SELECT Client_ID FROM client WHERE User_ID = ' + str(found_user) + ';'
        conn = pymysql.connect(host='localhost', user='root', password='#######', db='######')
        a = conn.cursor()
        a.execute(tech_check)
        utype_data = a.fetchall()
        user_type = "technician"
        if utype_data ==():
            a.execute(admin_check)
            utype_data = a.fetchall()
            user_type = "admin"
            if utype_data ==():
                a.execute(client_check)
                utype_data = a.fetchall()
                user_type = "client"
        a.close()
        conn.close()
        return (AppFrame._format_data(utype_data), user_type)



    def _format_data(data):
        data_set = []
        for n in data:
            data_set.append(n[0])
        format_data = data_set[0]
        print(format_data)
        return(format_data)


    def _technician_jobs(data, data_tuples, u_type_ID):
        """ Selects jobs for tech with Tech_ID as variable """
        for n in data:
            if n[9] == u_type_ID:
                data_tuples.append(n)
            else:
                pass

    def _admin_jobs(data, data_tuples, u_type_ID):
        """ Selects jobs for tech with Admin_ID as variable """
        for n in data:
            if n[8] == u_type_ID:
                data_tuples.append(n)
            else:
                pass

    def _client_jobs(data, data_tuples, u_type_ID):
        """ Selects jobs for tech with Client_ID as variable """
        for n in data:
            if n[7] == u_type_ID:
                data_tuples.append(n)
            else:
                pass





root = Tk()
lf = AppFrame(root)
root.mainloop()
