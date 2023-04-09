#Student : Krish Parimal Patel
#Student ID : 8885555
#Author : Madiha Kazmi
#Date Created : April 8, 2023
#purpose : The purpose of this Python code is to create a GUI-based school management system that connects to a SQLite database and allows users to add, view, delete, and display student records.
import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry  # pip install tkcalendar
import sqlite3

# Creating the universal font variables
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

# Connecting to the Database where all information will be stored
connector = sqlite3.connect('SchoolManagement.db')
cursor = connector.cursor()

connector.execute(
"CREATE TABLE IF NOT EXISTS SCHOOL_MANAGEMENT (STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, EMAIL TEXT, PHONE_NO TEXT, GENDER TEXT, DOB TEXT, STREAM TEXT)"
)

# Creating the functions
def reset_fields():
    global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar

    for i in ['name_strvar', 'email_strvar', 'contact_strvar', 'gender_strvar', 'stream_strvar']:
        exec(f"{i}.set('')")
    dob.set_date(datetime.datetime.now().date())


def reset_form():                                                                          # This function clears the form and resets all fields to their default values
    global tree
    tree.delete(*tree.get_children())                                                      # Clear the data in the tree view
    reset_fields()                                                                         # Reset all form fields


def display_records():                                                                     # This function retrieves all records from the database and displays them in the tree view
    tree.delete(*tree.get_children())                                                      # Clear the data in the tree view
    curr = connector.execute('SELECT * FROM SCHOOL_MANAGEMENT')                            # Execute a SELECT query to retrieve all records from the table
    data = curr.fetchall()                                                                 # Fetch all the records
    for records in data:
        tree.insert('', END, values=records)                                               # Insert each record into the tree view as a new row


def add_record():                                                                          # This function retrieves the values entered in the form fields and adds a new record to the database
    global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar
    # Retrieve the values from the form fields
    name = name_strvar.get()                                                              
    email = email_strvar.get()
    contact = contact_strvar.get()
    gender = gender_strvar.get()
    DOB = dob.get_date()
    stream = stream_strvar.get()
    if not name or not email or not contact or not gender or not DOB or not stream:        # Check if any of the fields are empty
        mb.showerror('Error!', "Please fill all the missing fields!!")
    else:
        try:
            connector.execute(
            'INSERT INTO SCHOOL_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, DOB, STREAM) VALUES (?,?,?,?,?,?)', (name, email, contact, gender, DOB, stream)
            )
            connector.commit()                                                            # Commit the changes to the database
            mb.showinfo('Record added', f"Record of {name} was successfully added")
            reset_fields()
            display_records()
        except:                                                                           # If an exception is raised, show an error message to the user
            mb.showerror('Wrong type', 'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')


def remove_record():
    try:
        if not tree.selection():                                                          # Check if a row is selected in the Treeview
            mb.showerror('Error!', 'Please select an item from the database')
        else:
            current_item = tree.focus()                                                   # Get the selected row's values and delete the row from the Treeview
            values = tree.item(current_item)
            selection = values["values"]
            tree.delete(current_item)
            connector.execute('DELETE FROM SCHOOL_MANAGEMENT WHERE STUDENT_ID=%d' % selection[0])          # Delete the record from the database
            connector.commit()
            mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')                 # Show success message and refresh the Treeview
            display_records()
    except Exception as e:
        mb.showerror('Error!', f'An error occurred while removing the record: {str(e)}')                    # Show error message if any error occurs



def view_record():
    global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar
     # Get currently selected record in the treeview widget
    current_item = tree.focus()
    values = tree.item(current_item)
    selection = values["values"]
    
    try:                                                                                                     # Extract date from the record selection and convert to date object
        date = datetime.date(int(selection[5][:4]), int(selection[5][5:7]), int(selection[5][8:]))
    except ValueError:                                                                                       # Show error message if the date format in record is invalid
        messagebox.showerror(title='Invalid Date', message='Invalid date format in record')
        return
    
    try:                                                                                                     # Set the values of tkinter StringVars based on the selected record
        name_strvar.set(selection[1]); email_strvar.set(selection[2])
        contact_strvar.set(selection[3]); gender_strvar.set(selection[4])
        dob.set_date(date); stream_strvar.set(selection[6])
    except IndexError:                                                                                       # Show error message if the selected record has missing data
        messagebox.showerror(title='Missing Data', message='Selected record has missing data')
        return

import tkinter.messagebox as messagebox

import os
import tkinter.messagebox as messagebox

def print_record():
    try:                                                                                                     # Select all records from the database
        curr = connector.execute('SELECT * FROM SCHOOL_MANAGEMENT')
        data = curr.fetchall()

        file_path = 'school_records.txt'                                                                      # Define the file path to store the records

        with open(file_path, 'w') as f:                                                                       # Open the file and write each record to it
            for record in data:
                f.write(str(record) + '\n')

        file_location = os.path.abspath(file_path)                                                             # Get the absolute path of the file and display a message box showing the file path
        messagebox.showinfo(title='File Saved', message=f"Records written to file: {file_path}\n\nFile location: {file_location}")
    except Exception as e:                                                                                     # If any exception occurs during the file writing process, show an error message
        messagebox.showerror(title='Error', message=f'An error occurred while writing to file: {str(e)}')



# Initializing the GUI window
main = Tk()
main.title('DataFlair School Management System')
main.geometry('1000x600')
main.resizable(0, 0)

# Creating the background and foreground color variables
lf_bg = 'MediumSpringGreen' # bg color for the left_frame
cf_bg = 'PaleGreen' # bg color for the center_frame

# Creating the StringVar or IntVar variables
name_strvar = StringVar()
email_strvar = StringVar()
contact_strvar = StringVar()
gender_strvar = StringVar()
stream_strvar = StringVar()

# Placing the components in the main window
Label(main, text="STUDENT RECORD MANAGEMENT SYSTEM", font=headlabelfont, bg='SpringGreen').pack(side=TOP, fill=X)

left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)

center_frame = Frame(main, bg=cf_bg)
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)

right_frame = Frame(main, bg="Gray35")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)

# Placing components in the left frame
Label(left_frame, text="Name", font=labelfont, bg=lf_bg).place(relx=0.375, rely=0.05)
Label(left_frame, text="Contact Number", font=labelfont, bg=lf_bg).place(relx=0.175, rely=0.18)
Label(left_frame, text="Email Address", font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.31)
Label(left_frame, text="Gender", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.44)
Label(left_frame, text="Date of Birth (DOB)", font=labelfont, bg=lf_bg).place(relx=0.1, rely=0.57)
Label(left_frame, text="Stream", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.7)

Entry(left_frame, width=19, textvariable=name_strvar, font=entryfont).place(x=20, rely=0.1)
Entry(left_frame, width=19, textvariable=contact_strvar, font=entryfont).place(x=20, rely=0.23)
Entry(left_frame, width=19, textvariable=email_strvar, font=entryfont).place(x=20, rely=0.36)
Entry(left_frame, width=19, textvariable=stream_strvar, font=entryfont).place(x=20, rely=0.75)

OptionMenu(left_frame, gender_strvar, 'Male', "Female").place(x=45, rely=0.49, relwidth=0.5)

dob = DateEntry(left_frame, font=("Arial", 12), width=15)
dob.place(x=20, rely=0.62)

Button(left_frame, text='Submit and Add Record', font=labelfont, command=add_record, width=18).place(relx=0.025, rely=0.85)

# Placing components in the center frame
Button(center_frame, text='Delete Record', font=labelfont, command=remove_record, width=15).place(relx=0.1, rely=0.25)
Button(center_frame, text='View Record', font=labelfont, command=view_record, width=15).place(relx=0.1, rely=0.35)
Button(center_frame, text='Reset Fields', font=labelfont, command=reset_fields, width=15).place(relx=0.1, rely=0.45)
Button(center_frame, text='Delete database', font=labelfont, command=reset_form, width=15).place(relx=0.1, rely=0.55)
Button(center_frame, text='Print to File', font=labelfont, command=print_record, width=15).place(relx=0.1, rely=0.65)

# Placing components in the right frame
Label(right_frame, text='Students Records', font=headlabelfont, bg='DarkGreen', fg='LightCyan').pack(side=TOP, fill=X)

tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                    columns=('Student ID', "Name", "Email Address", "Contact Number", "Gender", "Date of Birth", "Stream"))

X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)

X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)

tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

tree.heading('Student ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Email Address', text='Email ID', anchor=CENTER)
tree.heading('Contact Number', text='Phone No', anchor=CENTER)
tree.heading('Gender', text='Gender', anchor=CENTER)
tree.heading('Date of Birth', text='DOB', anchor=CENTER)
tree.heading('Stream', text='Stream', anchor=CENTER)

tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=140, stretch=NO)
tree.column('#3', width=200, stretch=NO)
tree.column('#4', width=80, stretch=NO)
tree.column('#5', width=80, stretch=NO)
tree.column('#6', width=80, stretch=NO)
tree.column('#7', width=150, stretch=NO)

tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

display_records()

# Finalizing the GUI window
main.update()
main.mainloop()
