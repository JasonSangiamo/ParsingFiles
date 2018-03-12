# Sangiamo, JJS6TX, CS 1111, Fall 2016
import threading
import urllib
import urllib.request
import time
import sqlite3
import datetime #for datastamp
import sys
import traceback

#DATABASE SETUP
conn = sqlite3.connect('wustlDatabaseURLs.db', check_same_thread=False)
c = conn.cursor()
#creates datatale for data to be stored in
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS data_entry(Datestamp TEXT, url TEXT)')
def dynamic_data_entry(website_id):
    unix = time.time()
    dateToAdd = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    c.execute('INSERT INTO data_entry(Datestamp, url) VALUES (?,?)',(dateToAdd, website_id))
    conn.commit()
create_table()



global hits
hits = 0
#This is the function that is called on a given URL to check if it is for a teacher w/ classes
def fetch_url(url):
    try:
        #opens URL and decodes, checks if it has a string in first 3000 characters that only not teachers or teachers w/o courses have
        stream = urllib.request.urlopen(url)
        stringStream = stream.read().decode()
        # this condition is to check if this page is for a teacher who actually teaches courses. If it is, we want to add it to the database
        if "<script src=\"https://acadinfo.wustl.edu/CourseListings/js/CourseList.js?v=1\" type=\"text/javascript\"></script>" not in stringStream[:3000]:

            dynamic_data_entry(url)
            print(str(url[-6:]) + " is a hit")
            global hits
            hits = hits + 1
        sys.stdout.flush()
        sys.stderr.flush()
    except Exception as exception:
        print("ERROR" + url)
        traceback.print_exc()
        error_file = open("errorLog.txt", "a")
        error_file.write(url)
        error_file.write(type(exception).__name__)
        error_file.close()
        sys.stdout.flush()
        sys.stderr.flush()

for j in range (0, 6000):
    # creating groups of 100 threads to be checked at synchronously
    startTime = time.time()
    urls = []
    checkIf100ItemList = []
    start = time.time()
    startIndex = 100*(j)
    endIndex = startIndex+100
    print(str(hits) + " hits so far!")
    print("Range: " + str(startIndex) + " to " + str(endIndex))
    for i in range (startIndex,endIndex):
        urls.append("https://acadinfo.wustl.edu/CourseListings/InstructorInfo.aspx?ID=" + str(i))
    threads = [threading.Thread(target=fetch_url, args=(url,)) for url in urls]
    # starting threads
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("Elapsed Time for 100 threads: %s" % (time.time() - start))
    averageTime = ((time.time()-startTime)/(j+1))
    print("Cumulative Average for 100 threads: " + str(averageTime) +  " seconds")
