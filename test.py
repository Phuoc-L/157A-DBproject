import os

#Importing Tkinter - Python GUI library
from tkinter import *
import tkinter.messagebox

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

#closes the program - destroys everything (database and the window)
def close():
    connect.close()
    main.destroy()

#Button to quit the program
ExitButton = Button(main, text="Exit", command=close, pady=10)
ExitButton.place(x=10,y=10)

#runs the program
main.mainloop()