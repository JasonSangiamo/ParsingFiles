#This is the new and improved course parser
#This functions takes a url string and a list of semesters
import urllib.request
import requests
from operator import itemgetter

def parse(url, semestersRaw):
    htmlText = requests.get(url).text
    #print(htmlText)

    classes = []
    sections = 0
    semesters = []
    #taking the raw list of semsters and generating the string to search for
    # This string indicates the start of a new term
    startOfTermString = "<td style='width:43px;'><a style='color:DarkRed;'>"



    for semester in semestersRaw:
        semesters.append(startOfTermString+semester)

    print(semesters)

    #(htmlText)

    #if startOfTermString not in the text, there is only one term and we need to parse it a differnet way
    if startOfTermString not in htmlText:
        startOfTermString = "<td style='width:43px;'></td>"
        semesters[0] = startOfTermString







    for semester in semesters:
        print("running semester in semesters")
        if semester in htmlText:
            print("semester in htmltext")
            #this loop is used to keep track of which semester to store the data currently parsed under
            semesterStartIndex = htmlText.index(startOfTermString)
            htmlTextWithoutStartingSemester =htmlText[semesterStartIndex+1:]

            #we must check if there is a new term in the remainder of the HTML
            if startOfTermString in htmlTextWithoutStartingSemester:
                semesterEndIndex = htmlTextWithoutStartingSemester.index(startOfTermString) + semesterStartIndex+35
            else:
                print("end not in here")
                semesterEndIndex = len(htmlTextWithoutStartingSemester)
            running = True
            classStartString = "<td style='width:14%;vertical-align:top;'>" #this string marks the start of a new
            #class because it marks the start of the department piece of info which is the first part of a class
            # , if its index is before that of a new semester string, that means there is another class left in the
            #current semester
            semesterString = htmlText[semesterStartIndex + 1:] #need to add one to be able to later identify when the next
            #term starts, if the 1 isn't added, it will think a new term starts at index 0

            #parsing strings:
            # Dept, dept abv, numb: <td style="width:14%;vertical-align:top;">
            parseDeptAbvNumb = "<td style='width:14%;vertical-align:top;'>"
            parseCourseTitle = "<td style='width:57%;vertical-align:top;'>"
            parseUnits = "<td style='width:18%;vertical-align:top;'>"
            parseDescription = "<td style='width:91%;'"
            parseLab = "<td style='width:11%;vertical-align:top;'>"

            #print(semesterString.index(classStartString))
            #30 so it doesn't just count itself
            #print(semesterString[30:].index(startOfTermString))
            while(semesterString.index(classStartString) < semesterString.index(startOfTermString)):


#CLASS FIELDS
########################################################################################################################
                #makes semeseter string now start at the start of this info because anything before this is now useless
                semesterString = semesterString[semesterString.index(parseDeptAbvNumb) : ]
                #strips the start of the info we're looking for from the start of semesterstirng
                semesterString = semesterString.strip("<td style='width:14%;vertical-align:top;'><a style='font-weight: bold; text-align:left;'>")
                #the info we're looking for is now at the start of semesterString and ends at the start of the first HTML tag

                deptAbvNumb = semesterString[:semesterString.index("<")]
                deptAbvNumb = deptAbvNumb.split("&nbsp")
                abv = deptAbvNumb[0]
                dept = deptAbvNumb[1]
                numb = deptAbvNumb[2]

                semesterString = semesterString[semesterString.index(parseCourseTitle) : ]
                semesterString = semesterString.strip("<td style='width:57%;vertical-align:top;'><a style='font-weight: bold; text-align:left;' >")
                courseTitle = semesterString[ : semesterString.index("<")]
                #print(courseTitle)

                semesterString = semesterString[semesterString.index(parseUnits) : ]
                semesterString = semesterString.strip("<td style='width:18%;vertical-align:top;'><a style='text-align:left;'>")
                units = semesterString[ : semesterString.index("<")]
                #print(units)

                semesterString = semesterString[semesterString.index(parseLab) : ]
                semesterString = semesterString.strip("<td style='width:11%;vertical-align:top;'><a style='text-align:left;'>")
                #print(semesterString[0])
                if semesterString[0] == "/":
                    lab = "No lab required"
                else:
                    lab = semesterString[ : semesterString.index("</")]
                #print(lab)

                semesterString = semesterString[semesterString.index(parseDescription) : ]
                semesterString = semesterString.strip("<td style='width:91%;'><a style='text-align:left;' >")
                description = semesterString[ : semesterString.index("<")]
                #print(description)

#SECTION FIELDS
########################################################################################################################
                classString = semesterString[ : semesterString.index(classStartString)]
                sectionInfoMarker = "<td class='ItemRow'>"
                tagCounter = 0
                while(sectionInfoMarker in classString):
                    classString = classString[classString.index(sectionInfoMarker) : ]
                    if tagCounter % 6 == 0:
                        #this means it is section
                        classString = classString[classString.index(sectionInfoMarker) : ]
                        classString = classString.strip(sectionInfoMarker)
                        section = classString[ : classString.index("<")]
                        #print(section)
                    if tagCounter % 6 == 1:
                        #this means it is the days string
                        classString = classString[classString.index(sectionInfoMarker) : ]
                        classString = classString.strip(sectionInfoMarker)
                        days= classString[ : classString.index("</")]
                        #print(days)
                    tagCounter += 1
                    if tagCounter % 6 == 2:
                        # this means it is the time string
                        classString = classString[classString.index(sectionInfoMarker):]
                        classString = classString.strip(sectionInfoMarker)
                        time = classString[: classString.index("</")]
                        if "-" in time:
                            time = time.split("-")
                            startTime = time[0]
                            endTime = time[1]
                        else:
                            startTime = "Not given"
                            endTime = "Not given"
                            print("error parsing time!")
                        #print(time)
                    if tagCounter % 6 == 3:
                        # this means it is the building and room string
                        classString = classString[classString.index(sectionInfoMarker):]
                        classString = classString.strip(sectionInfoMarker)
                        #doing the ">" + 1 to get rid of link
                        roomAndBuilding = classString[classString.index(">") + 1: classString.index("</")]
                        roomAndBuilding = roomAndBuilding.strip()
                        if roomAndBuilding == '':
                            roomAndBuilding = "TBA"
                        #print(roomAndBuilding)
                    if tagCounter % 6 == 4:
                        # this means it is the instructor string
                        classString = classString[classString.index(sectionInfoMarker):]
                        classString = classString.strip(sectionInfoMarker)
                        instructor = classString[classString.index(">") + 1 : classString.index("</")]
                        #the > gets rid of the link
                        #print(instructor)
                    if tagCounter % 6 == 5:
                        # this means it is the final exam string
                        classString = classString[classString.index(sectionInfoMarker):]
                        classString = classString.strip(sectionInfoMarker)
                        finalExam = classString[: classString.index("</")]
                        #print(finalExam)
                        #append here
                        courseObject = [courseTitle, instructor, dept, abv, numb, description, units, lab, roomAndBuilding, startTime, endTime, days, finalExam, semester.strip("<td style='width:43px;'><a style='color:DarkRed;'>"), section]
                        classes.append(courseObject)


    return classes


coursees = parse("https://acadinfo.wustl.edu/CourseListings/InstructorInfo.aspx?ID=449385", ["FL2017"])
# for course in coursees:
#     print(course)