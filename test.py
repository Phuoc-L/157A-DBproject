import os

#Importing Tkinter - Python GUI library
from tkinter import *
import tkinter.messagebox

#Importing sqlite3
import sqlite3

#if 'DNASequence.db' already exist, delete it
if os.path.exists("DNASequence.db"):
    os.remove("DNASequence.db")

#Create the 'DNASequence.db' file
connect = sqlite3.connect('DNASequence.db')
if os.path.exists('DNASequence.db'):
    
    #create cursor to point in database
    c = connect.cursor()

    #Create the table_name table
    c.execute("""
        CREATE TABLE table_name(
            data1 TEXT,
            dta2 INGETER
        )""")


#Tkinter main window
#First window that the user will see
main = tkinter.Tk()

#Specifies basic aspects of the main window
main.title("Sequence Database")
main.configure(background='black')
main.geometry('800x300')

#Label and text entry for the query
Label(main, text="Query the Sequence Database", font=('Calibri 15'), bg='black').place(x=10,y=60)
queryBox = Entry(main, width= 80)
queryBox.place(x=10,y=90)

#closes the program - destroys everything
def close():
    main.destroy()

#Button to quit the program
ExitButton = Button(main, text="Exit", command=close, pady=10)
ExitButton.place(x=10,y=10)

#runs the program
main.mainloop()