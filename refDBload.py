#Importing Tkinter - Python GUI library

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox
import os

# Importing sqlite3
import sqlite3

# if 'ProteinSequence.db' already exist, delete it
if os.path.exists("ProteinSequence.db"):
    os.remove("ProteinSequence.db")

# Create the 'ProteinSequence.db' file
connect = sqlite3.connect('ProteinSequence.db')
if os.path.exists('ProteinSequence.db'):
    # create cursor to point in the database
    c = connect.cursor()

    # Create all tables
    # Create the Organism table
    c.execute("""
        CREATE TABLE Organism(
            SequenceOrganism TEXT NOT NULL PRIMARY KEY UNIQUE,
            GenusFamily TEXT NOT NULL,
            SequenceSource INTEGER NOT NULL
        )""")
    # Create the LAB table
    c.execute("""
        CREATE TABLE LAB(
            LabID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            LabAddress TEXT NOT NULL,
            LabName TEXT NOT NULL,
            LabZipCode INTEGER NOT NULL,
            LabState TEXT NOT NULL,
            LabCity TEXT NOT NULL,
            LabLockerLocation INTEGER NOT NULL
        )""")
    # Create the Institution table
    c.execute("""
        CREATE TABLE Institution(
            InstitutionID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            InstitutionName TEXT NOT NULL,
            InstitutionAddress TEXT NOT NULL,
            InstitutionCity TEXT NOT NULL,
            InstitutionZipCode INTEGER NOT NULL,
            InstitutionState TEXT NOT NULL
        )""")
    # Create the Mission table
    c.execute("""
        CREATE TABLE Mission(
            MissionID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            MissionSponsor TEXT NOT NULL,
            MissionName TEXT NOT NULL
        )""")
    # Create the Researcher table
    c.execute("""
        CREATE TABLE Researcher(
            ResearcherNumber INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            ResearcherFirstname TEXT NOT NULL,
            ResearcherLastName TEXT NOT NULL,
            ResearcherReputation INTEGER NOT NULL,
            InstitutionID INTEGER NOT NULL,
            MissionID INTEGER NOT NULL,
            FOREIGN KEY(InstitutionID) REFERENCES Institution(InstitutionID),
            FOREIGN KEY (MissionID) REFERENCES Mission(MissionID)
        )""")
    # Create the Sample table
    c.execute("""
        CREATE TABLE Sample(
            SampleID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            DateSampled INTEGER NOT NULL,
            TimeSampled INTEGER NOT NULL,
            SampleSource TEXT NOT NULL,
            SequenceOrganism TEXT NOT NULL,
            LabID INTEGER NOT NULL,
            FOREIGN KEY (SequenceOrganism) REFERENCES Organism(SequenceOrganism),
            FOREIGN KEY (LabID) REFERENCES Lab(LabID)
        )""")
    # Create the Sequence table
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
    
    # commit the database
    connect.commit()

#the Tkinter root window
#First window that the user will see
root = tkinter.Tk()

#Specifies basic aspects of the main window
root.title("Alignment Selector")
root.geometry('500x300')

#closes the program - destroys everything
def close():
    root.destroy()

#this function takes the input file and processes it
def submissionAl():
    #opens the file dialog and gets the filepath of the input file
    filePath = filedialog.askopenfilename()

    #Checks if the file is existent and in the correct format
    if not filePath:
        tkinter.messagebox.showerror("Canceled","operation canceled")
        return
    elif filePath.lower().endswith(('.fasta', '.fa', '.txt')):
        tkinter.messagebox.showinfo("File accepted","File to be submitted")
    else:
        tkinter.messagebox.showerror("File error", "Improper file type")
        return

    #reads the inputted file and stores all the strings in a list
    with open(filePath, 'r') as reader:
        linesFile = []
        seqLine = ""
        numSeqs = 0

        for lineRed in reader:
            if (lineRed.count(">") != 0):
                linesFile.append(seqLine)
                linesFile.append(lineRed)
                seqLine = ""
                numSeqs += 1
            else:
                seqLine += lineRed
    #takes care of certain edge case issues in the loop
    if(seqLine != ""):
        linesFile.append(seqLine)

    if (linesFile[0].count(">") == 0):
        linesFile.pop(0)

    def_line=""
    sequence = ""
    mission = 1
    lab_store = 1
    insert_stmt = ("INSERT INTO Sequence(SequenceName, Sequence, ResearcherNumber, SampleID)"
                   "VALUES (?, ?, ?, ?)"
                   )

    #Creates the new output testing and training files
    for evLine in linesFile:
        if (evLine.count(">") != 0):
            record = (def_line, sequence, mission, lab_store)
            c.execute(insert_stmt, record)

            def_line = evLine[1:-1]
            sequence = ""
        elif (evLine.count("!") != 0):
            mission = evLine
        elif  (evLine.count("*") != 0):
            lab_store= evLine
        else:
            sequence = evLine

    #Insert all data into table
    #insert into the organism table
    c.execute("""INSERT INTO Organism (SequenceOrganism, GenusFamily, SequenceSource) VALUES
            ('Rhinocerotidae', 'Equus', 1), 
            ('Culex pipiens', 'Culex', 2),
            ('Panthera leo', 'Panthera', 3)
            """)
    #insert into the Lab table
    c.execute("""INSERT INTO Lab(LabAddress, LabName, LabZipCode, LabState, LabCity, LabLockerLocation) VALUES
            ('60 Foster Lane Evanston', 'Research Center Of The Organizing Of Zoogenics', 2580135826,'Alabama', 'Huntsville', 34),
            ('38 Second Drive Charleston', 'Test Center Of The Enhancement Of Synecology', 9420394209,'California', 'Sacramento', 78),
            ('8720 Big Rock Cove Drive Bartlett', 'Research Lab Of The Reinforcement Of Physiology', 8020180239,'Colorado','Denver', 59)
            """)
    #insert into the Institution table
    c.execute("""INSERT INTO Institution(InstitutionName, InstitutionAddress, InstitutionCity, InstitutionZipCode, InstitutionState) VALUES
            ('9733 St Paul Ave. North Wales', 'Beacon Biotechnology', 'Los Angeles', 9420382731, 'California'),
            ('3 Brickyard Street Phillipsburg', 'Sega Future Industries', 'Sacramento', 8988236517, 'California'),
            ('759 Mill Avenue Leominster', 'ReAgent Technologies', 'Houston', 1937284981, 'Texas')
            """)
    #insert into the Mission table
    c.execute("""INSERT INTO Mission (MissionSponsor, MissionName) VALUES
            ('ActiveGrant Coporation', 'Organism/Organic Exposure to Radiation'), 
            ('Future Animals Foundation', 'Animal adaptation Coevolution'), 
            ('Nature Future Technology', 'Animal Living Pattern - Behavioral Study')
            """)
    #insert into the Researcher table
    c.execute("""INSERT INTO Researcher (ResearcherFirstname, ResearcherLastName, ResearcherReputation, InstitutionID, MissionID) VALUES
            ('Tasneem', 'Richard', 89, 1, 2),
            ('Niyah', 'Caldwell', 74, 2, 1),
            ('Sadiyah', 'Carr', 95, 3, 2)
            """)
    #insert into the Sample table
    c.execute("""INSERT INTO Sample (DateSampled, TimeSampled, SampleSource, SequenceOrganism, LabID) VALUES
            (date('2013-04-23'), time('15:05:12'), 'Lab Sample', 'Culex pipiens', 2), 
            (date('2016-12-10'), time('13:20:22'), 'Field Sample', 'Rhinocerotidae', 1), 
            (date('2018-07-03'), time('09:32:04'), 'Field Sample', 'Panthera leo', 3) 
            """)

    # commit the database
    connect.commit()

#submission button
submitButton = Button(root, text="Begin Trimming", command=submissionAl, pady=10)
submitButton.place(x=150, y=225)

#Button to quite the program
ExitButton = Button(root, text="Exit", command=close, pady=10)
ExitButton.place(x=0,y=0)

#runs the program
root.mainloop()