
import os

#Importing Tkinter - Python GUI library
from tkinter import *
import tkinter.messagebox
from  tkinter import ttk

#Importing sqlite3
import sqlite3

#if 'ProteinSequence.db' already exist, delete it
if os.path.exists("ProteinSequence.db"):
    os.remove("ProteinSequence.db")

#Create the 'ProteinSequence.db' file
connect = sqlite3.connect('ProteinSequence.db')
if os.path.exists('ProteinSequence.db'):
    
    #create cursor to point in the database
    c = connect.cursor()

    #Create all tables
    #Create the Organism table
    c.execute("""
        CREATE TABLE Organism(
            SequenceOrganism TEXT NOT NULL PRIMARY KEY UNIQUE,
            GenusFamily TEXT NOT NULL,
            SequenceSource INGETER NOT NULL
        )""")
    #Create the LAB table
    c.execute("""
        CREATE TABLE LAB(
            LabID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            LabAddress TEXT NOT NULL,
            LabName TEXT NOT NULL,
            LabZipCode INGETER NOT NULL,
            LabState TEXT NOT NULL,
            LabCity TEXT NOT NULL,
            LabLockerLocation INGETER NOT NULL
        )""")
    #Create the Institution table
    c.execute("""
        CREATE TABLE Institution(
            InstitutionID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            InstitutionName TEXT NOT NULL,
            InstitutionAddress TEXT NOT NULL,
            InstitutionCity TEXT NOT NULL,
            InstitutionZipCode INTEGER NOT NULL,
            InstitutionState TEXT NOT NULL
        )""")
    #Create the Mission table
    c.execute("""
        CREATE TABLE Mission(
            MissionID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            MissionSponsor TEXT NOT NULL,
            MissionName TEXT NOT NULL
        )""")
    #Create the Researcher table
    c.execute("""
        CREATE TABLE Researcher(
            ResearcherNumber INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            ResearcherFirstname TEXT NOT NULL,
            ResearcherLastName TEXT NOT NULL,
            ResearcherReputation INTEGER NOT NULL,
            InstitutionID INTEGER NOT NULL,
            MIssionID INTEGER NOT NULL,
            FOREIGN KEY(InstitutionID) REFERENCES Institution(InstitutionID),
            FOREIGN KEY (MissionID) REFERENCES Mission(MissionID)
        )""")
    #Create the Sample table
    c.execute("""
        CREATE TABLE Sample(
            SampleID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            TimeSampled INTEGER NOT NULL,
            SampleSource TEXT NOT NULL,
            SequenceOrganism TEXT NOT NULL,
            LabID INTEGER NOT NULL,
            FOREIGN KEY (SequenceOrganism) REFERENCES Organism(SequenceOrganism),
            FOREIGN KEY (LabID) REFERENCES Lab(LabID)
        )""")
    #Create the Sequence table
    c.execute("""
        CREATE TABLE Sequence(
            SequenceID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            SequenceName TEXT NOT NULL,
            Sequence TEXT NOT NULL,
            ResearcherNumber INTEGER NOT NULL,
            SampleID INTEGER NOT NULL,
            FOREIGN KEY (ResearcherNumber) REFERENCES Researcher(ResearcherNumber),
            FOREIGN KEY (SampleID) REFERENCES Sample(SampleID)
        )""")
    
    #Insert all data into table
    #insert into the organism table
    c.execute("""INSERT INTO Organism VALUES 
            ('HELLO', 'HI', 1), 
            ('bruh', 'dam', 3)
            
            """)
    #insert into the Lab table
    c.execute("""INSERT INTO Lab VALUES 
            (1, 'HELLO', 'hello', 1, 'heloo', 'hellll', 3), 
            (2, 'bruh', 'hol', 3, 'dedw', 'dewdfew', 4)
            
            """)

    #commit the database
    connect.commit()


#Tkinter main window
#First window that the user will see
main = tkinter.Tk()

#Specifies basic aspects of the main window
main.title("Protein Sequence Database Query")
main.configure(background='black')
main.geometry('800x300')

#Label and text entry for the query
Label(main, text="Query the Sequence Database", font=('Calibri 15'), bg='black').place(x=10,y=60)
queryBox = Entry(main, width= 80)
queryBox.place(x=10,y=90)

#create the query window
def query():
    qw = tkinter.Tk()

    #Specifies basic aspects of the query window
    qw.title("Query Result")
    qw.configure(background='black')
    width = 400
    height = 300
    qw.geometry(f'{width}x{height}')

    #closes the query
    def Close():
        qw.destroy()

    #button to close the query window
    CloseButton = Button(qw, text="Close", command=Close, padx=20, pady=10)
    CloseButton.place(x=10,y=10)

    try:
        #execute any query from the queryBox
        c.execute(queryBox.get())
        des = [tuple[0] for tuple in c.description]
        outputs = c.fetchall()

        #create table to display query
        #code referenced from https://pythonguides.com/python-tkinter-table-tutorial/ 
        table_frame = Frame(qw)
        table_frame.pack()
        table_frame.place(x=10, y=60)
        query_table = ttk.Treeview(table_frame)
        query_table.pack()
    
        #output any query into output box
        query_table['columns'] = des
        query_table.column("#0", width=0,  stretch=NO)
        width = 20
        height = 150

        #add columns to table and define width
        #for every new column make window bigger
        for head in des:
            query_table.column(head,anchor=CENTER, width=100)
            width += 100

        #resize the window
        qw.geometry(f'{width}x{height}')

        #insert the column names into the table
        query_table.heading("#0",text="",anchor=CENTER)
        for head in des:
            query_table.heading(head,text=head,anchor=CENTER)
    
        #insert query into the table
        #for every item inserted, make window taller
        for x in range(len(outputs)):
            query_table.insert(parent='',index='end', iid=x, text='', values=outputs[x])
            height += 50

        #resize the window
        qw.geometry(f'{width}x{height}')
    except:
        Label(qw, text="Something wrong have occur", font=('Calibri 15'), bg='black').place(x=10,y=60)

    
    
    qw.mainloop()

#button to start the database query
querybutton = Button(main, text="Submit", command=query, padx=20, pady=10)
querybutton.place(x=10,y=140)

#closes the main program - destroys everything (database and the window)
def Exit():
    connect.close()
    main.destroy()

#Button to quit the program
ExitButton = Button(main, text="Exit", command=Exit, padx=20, pady=10)
ExitButton.place(x=10,y=10)

#runs the program
main.mainloop()