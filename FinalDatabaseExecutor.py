from FinalParser import parse
import sqlite3
import time
import datetime
import threading
import traceback
import sys
import requests
from bs4 import BeautifulSoup
conn = sqlite3.connect('wustlDatabaseURLs.db', check_same_thread=False)
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS CoursesFinal(Datestamp TEXT, Name TEXT, Instructor TEXT,  Department TEXT, Abbreviation TEXT, Number TEXT, Description TEXT, Units TEXT, Lab TEXT, Location TEXT, StartTime TEXT, EndTime TEXT, Days TEXT, Final TEXT, Semester TEXT, Section TEXT)')
create_table()

def dataEntry(courseObject):
    c1 = courseObject
    unix = time.time()
    dateToAdd = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    c.execute('INSERT INTO CoursesFinal(Datestamp, Name, Instructor, Department, Abbreviation, Number, Description, Units, Lab, Location, '
              'StartTime, EndTime, Days, Final, Semester, Section) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
              (dateToAdd, c1[0],c1[1],c1[2],c1[3],c1[4],c1[5],c1[6],c1[7],c1[8],c1[9],c1[10],c1[11],c1[12],c1[13],c1[14]))
    conn.commit()

global courses
courses = 0
def fetchCourses(url):
    #change this to alter which semester are used for class addition
    semesters = ["FL2017"]
    allCourses = parse(url, semesters)
    for course in allCourses:
        dataEntry(course)


def dataEntryThreading():
    try:
        iterations = 0
        counter =0
        c.execute('SELECT url FROM data_entry')
        data = c.fetchall()
        print(len(data))
        for url in data:
            startTime = time.time()
            print(counter)
            counter += 1
            url = str(url).strip("('").strip("',)")
            print(url)
            fetchCourses(url)
            print("Elapsed Time for 1 threads: %s" % (time.time() - startTime))
    except Exception as exception:
        traceback.print_exc()
        print("ERROR" + str(url))
        error_file = open("errorLogClasses.txt", "a")
        error_file.write(str(url) + '\n')
        error_file.write(type(exception).__name__)
        error_file.close()


#dataEntryThreading()
    c.execute('ALTER TABLE CoursesFinal ADD COLUMN NameID INT')
conn.commit()