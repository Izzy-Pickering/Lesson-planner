import cs50
import csv

# Select the database
db = cs50.SQL("sqlite:///Database/resources.db")

# Set up the global variables
topiclist = []
topicFlashcardString = {}
topicBookString = {}
topicGameString = {}
topicLessonString = {}

def main():
    # Empty the database
    open("Database/resources.db", "w").close()
    
    # REFRESH THE TABLES:
    # Set up the books, games and lesson tables and link them to the topics table
    db.execute("CREATE TABLE flashcards (id INTEGER NOT NULL, title TEXT, topics TEXT, active BOOL NOT NULL, PRIMARY KEY (id))")
    db.execute("CREATE TABLE books (id INTEGER NOT NULL, title TEXT NOT NULL, author TEXT, collection TEXT, booknber TEXT, publisher TEXT, bookType TEXT, subtype TEXT, level TEXT, description TEXT, topics TEXT, active BOOL NOT NULL, PRIMARY KEY (id))")
    db.execute("CREATE TABLE games (id INTEGER NOT NULL, title TEXT NOT NULL, publisher TEXT, colour TEXT, gameType TEXT, description TEXT, duration INTEGER, numberPlayersMin INTEGER NOT NULL, numberPlayersMax INTEGER, ageMin INTEGER, ageMax INTEGER, topics TEXT, active BOOL NOT NULL, PRIMARY KEY (id))")
    db.execute("CREATE TABLE lessons (id INTEGER NOT NULL, title TEXT NOT NULL, publisher TEXT, type TEXT, activities TEXT, file TEXT, topics TEXT, active BOOL NOT NULL, PRIMARY KEY (id))")
    db.execute("CREATE TABLE crafts (id INTEGER NOT NULL, title TEXT, materials TEXT, duration INTEGER, image TEXT, instructions TEXT, active BOOL NOT NULL, PRIMARY KEY (id))")
    db.execute("CREATE TABLE resources (id INTEGER NOT NULL, ref TEXT NOT NULL, PRIMARY KEY (id, ref))")
    db.execute("CREATE TABLE topics (id INTEGER NOT NULL, topic TEXT UNIQUE NOT NULL, PRIMARY KEY (id))")
    db.execute("CREATE TABLE topicLink (topicId INTEGER, resourceId INTEGER, resourceType TEXT, FOREIGN KEY (topicId) REFERENCES topics(ID), FOREIGN KEY (resourceId, resourceType) REFERENCES resources(id, ref))")

    # Set up the student table
    db.execute("CREATE TABLE students (id INTEGER NOT NULL, name TEXT, address TEXT, phone TEXT, email TEXT, group_size INTEGER, age INTEGER, hobbies TEXT, pricePerStudent FLOAT(10, 2) NOT NULL, active BOOL NOT NULL, nberLessons INTEGER NOT NULL, nberCancelled INTEGER NOT NULL, amountPaid FLOAT(10, 2), amountDue FLOAT(10, 2), PRIMARY KEY (id))")
    db.execute("CREATE TABLE student_details1 (studentId INTEGER NOT NULL, resourceId INTEGER, resourceType TEXT, bookingId INTEGER, FOREIGN KEY (studentid) REFERENCES students(id), FOREIGN KEY (resourceId, resourceType) REFERENCES resources(id, ref), FOREIGN KEY (bookingId) REFERENCES bookings(id))")
    db.execute("CREATE TABLE student_details2 (studentId INTEGER NOT NULL, subject TEXT, studied BOOL, understood BOOL, mastered BOOL, FOREIGN KEY (studentid) REFERENCES students(id))")
    db.execute("CREATE TABLE bookings (id INTEGER NOT NULL, studentId INTEGER NOT NULL, date DATE NOT NULL, month INTEGER, year INTEGER, time TIME, groupSize INTEGER, subject TEXT, completed BOOL NOT NULL, cancelled BOOL NOT NULL, PRIMARY KEY (id), FOREIGN KEY (studentid) REFERENCES students(id))")
    db.execute("CREATE TABLE payments (id INTEGER NOT NULL, studentId INTEGER NOT NULL, date DATE NOT NULL, month INTEGER, year INTEGER, amount FLOAT NOT NULL, method TEXT NOT NULL, reductionApplied INTEGER, PRIMARY KEY (id), FOREIGN KEY (studentid) REFERENCES students(id))")


    # UPDATE THE DATA
    # Flashcards
    with open("Database\Flashcards.csv", "r") as flashcards:
        reader = csv.DictReader(flashcards)
        
        for row in reader:
            title = row["Title"]
            topics = row["Topics"]
            active = row["Active"]

            db.execute("INSERT INTO flashcards (title, topics, active) VALUES (?, ?, ?)", title, topics, active)

            # Get new ID number
            id = db.execute("SELECT id FROM flashcards ORDER BY id DESC LIMIT 1")[0]["id"]

            # Seperate topics and stick them to specific topic ids
            extractTopics(topics, id, topicFlashcardString)

            # Add to the resources table
            db.execute("INSERT INTO resources (id, ref) VALUES (?, ?)", id, "flashcards")

    # Books
    with open("Database\Books.csv", "r") as books:
        reader = csv.DictReader(books)

        for row in reader:
            title = row["Title"]
            author = row["Author"]
            collection = row["Collection"]
            booknber = row["Book nber"] 
            publisher = row["Publisher"]
            bookType = row["Book Type"]
            subtype= row["Subtype"]
            level = row["Level"]
            description = row["Description"]
            topics = row["Topics"]
            active = row["Active"]

            # Insert data into the db file
            db.execute("INSERT INTO books(title, author, collection, booknber, publisher, bookType, subtype, level, description, topics, active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                title, author, collection, booknber, publisher, bookType, subtype, level, description, topics, active)   

            # Get new ID number
            id = db.execute("SELECT id FROM books ORDER BY id DESC LIMIT 1")[0]["id"]

            # Seperate topics and stick them to specific topic ids
            extractTopics(topics, id, topicBookString)

            # Add to the resources table
            db.execute("INSERT INTO resources (id, ref) VALUES (?, ?)", id, "books")

    # Games
    with open("Database\Games.csv", "r") as games:
        reader = csv.DictReader(games)

        for row in reader:
            # Set up the csv column names into variables
            id = row["Id"]
            title = row["Title"]
            publisher = row["Publisher"]
            colour = row["Colour"]
            gameType = row["Type"]
            description = row["Description"]
            duration = row["Duration"]
            numberPlayersMin = row["Min nber player"]
            numberPlayersMax = row["Max nber player"]
            ageMin = row["Min age"]
            ageMax = row["Max age"]
            active = row["Active"]

            # Insert data into the db file
            db.execute("INSERT INTO games (title, publisher, colour, gameType, description, duration, numberPlayersMin, numberPlayersMax, ageMin, ageMax, active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                title, publisher, colour, gameType, description, duration, numberPlayersMin, numberPlayersMax, ageMin, ageMax, active)   

            # Get new ID number
            id = db.execute("SELECT id FROM games ORDER BY id DESC LIMIT 1")[0]["id"]

            # Seperate topics and stick them to specific topic ids
            extractTopics(topics, id, topicGameString)

            # Add to the resources table
            db.execute("INSERT INTO resources (id, ref) VALUES (?, ?)", id, "games")

    # Lessons
    with open("Database\Lessons.csv", "r") as lessons:
        reader = csv.DictReader(lessons)

        for row in reader:
            id = row["Id"]
            title = row["Title"]
            publisher = row["Publisher"]
            types = row["Type"]
            activity = row["Activities"]
            lessonFile = row["File"]
            topics = row["Topics"]
            active = row["Active"]

            db.execute("INSERT INTO lessons (title, publisher, type, activities, file, topics, active) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                title, publisher, types, activity, lessonFile, topics, active)

            # Get new ID number
            id = db.execute("SELECT id FROM lessons ORDER BY id DESC LIMIT 1")[0]["id"]

            # Seperate topics and stick them to specific topic ids 
            extractTopics(topics, id, topicLessonString)

            # Add to the resources table
            db.execute("INSERT INTO resources (id, ref) VALUES (?, ?)", id, "lessons")

    # Crafts
    with open("Database\Arts & crafts.csv", "r") as crafts:
        reader = csv.DictReader(crafts)
        
        for row in reader:
            id = row["Id"]
            title = row["Title"]
            materials = row["Materials"]
            duration = row["Duration"]
            image = row["Image"]
            instruc = row["Instructions"]
            active = row["Active"]

            db.execute("INSERT INTO crafts (title, materials, duration, image, instructions, active) VALUES (?, ?, ?, ?, ?, ?)",
                title, materials, duration, image, instruc, active)

            # Get new ID number
            id = db.execute("SELECT id FROM crafts ORDER BY id DESC LIMIT 1")[0]["id"]

            # Add to the resources table
            db.execute("INSERT INTO resources (id, ref) VALUES (?, ?)", id, "crafts")

    # Set up the topics table
    topiclist.sort()
    for values in topiclist:
        values.capitalize()
        db.execute("INSERT INTO topics (topic) VALUES (?)", values)

    # Link the topics and the resources
    linkTopics_Resourses(topicFlashcardString, "flashcards")
    linkTopics_Resourses(topicBookString, "books")
    linkTopics_Resourses(topicLessonString, "lessons")

    # Update the student list
    with open("Database\student list.csv", "r") as studentList:
        reader = csv.DictReader(studentList)

        for row in reader:
            name = row["Name"]
            address = row["Address"]
            phone = row["Phone"]
            email = row["Email"]
            groupSize = row["Group size"]
            age = row["Age"]
            hobbies = row["Hobbies"]
            pricePerStudent = row["PricePerStudent"]
            active = row["Active"]

            # Enter all data into the table
            db.execute("INSERT INTO students (name, address, phone, email, group_size, age, hobbies, pricePerStudent, active, nberLessons, nberCancelled) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0)",
                name, address, phone, email, groupSize, age, hobbies, pricePerStudent, active)

    # Update the bookings
    with open ("Database\Bookings.csv", "r") as bookings, open ("Database\BookingsPart2.csv", "r") as bookingsPart2:
        reader = csv.DictReader(bookings)
        
        for row in reader:
            studentId = db.execute("SELECT id FROM students WHERE name = ?",row["Student"])[0]["id"]
            date = row["Date"]
            d = str(date).split('/')
            month = d[1]
            year = d[2]
            time = row["Time"]
            groupSize = row["Group Size"]

            # Insert the data into the table
            db.execute("INSERT INTO bookings (studentId, date, month, year, time, groupSize, completed, cancelled) VALUES (?, ?, ?, ?, ?, ?, 0, 0)",
                studentId, date, month, year, time, groupSize) 

        # Extract the data from the second bookings csv file
        reader2 = csv.DictReader(bookingsPart2)
        
        for row in reader2:
            studentId = db.execute("SELECT id FROM students WHERE name = ?", row["Student"])[0]["id"]
            date = row["Date"]
            subject = db.execute("SELECT * FROM student_details1 ")
            completed = 0
            cancelled = 0
            if row["Completed"] == "x":
                completed = 1
            elif row["Cancelled"] == "x":
                cancelled = 1

            # Insert the data into the table
            db.execute("UPDATE bookings SET completed = ?, cancelled = ? WHERE studentId = ? AND date = ?",
                completed, cancelled, studentId, date)

    # Additional student details
    with open("Database\StudentdetailsA.csv", "r") as studentList2:
        reader = csv.DictReader(studentList2)

        for row in reader:
            studentId = db.execute("SELECT id FROM students WHERE name = ?",row["Student"])[0]["id"]
            bookingId = row["Booking Id"]
            resourceType = row["Resource Type"]
            if resourceType != "subject":
                resourceId = getResourceId(row["Resource"], resourceType)

                # Insert the data into the table
                db.execute("INSERT INTO student_details1 (studentId, resourceId, resourceType, bookingId) VALUES (?, ?, ?, ?)",
                    studentId, resourceId, resourceType, bookingId)
            else: 
                # Insert the data into the bookings table
                db.execute("UPDATE bookings SET subject = ? WHERE studentId = ? AND bookingId = ?",
                    subject, studentId, bookingId) 

    # Update the payments
    with open ("Database\Payments.csv", "r") as payments:
        reader = csv.DictReader(payments)
        
        for row in reader:
            studentId = db.execute("SELECT id FROM students WHERE name = ?", row["Student"])[0]["id"]
            date = row["Date"]
            d = str(date).split('/')
            month = d[1]
            year = d[2]
            amount = row["Amount"]
            method = row["Payment method"]
            reductionApplied = row["Reduction"]

            # Insert the data into the table
            db.execute("INSERT INTO payments (studentId, date, month, year, amount, method, reductionApplied) VALUES (?, ?, ?, ?, ?, ?, ?)",
                studentId, date, month, year, amount, method, reductionApplied)

    # Finish completing the 'students' database now that all other databases are completed
    studentId = db.execute("SELECT id FROM students")
    for key in studentId:
        id = key["id"]
        pricePerStudent = db.execute("SELECT pricePerStudent FROM students WHERE id = ?", id)[0]["pricePerStudent"]
        nberLessons = db.execute("SELECT COUNT(*) FROM bookings WHERE studentId = ? AND completed = 1", id)[0]["COUNT(*)"]
        nberCancelled = db.execute("SELECT COUNT(*) FROM bookings WHERE studentId = ? AND cancelled = 1", id)[0]["COUNT(*)"]
        amountPaid = db.execute("SELECT SUM(amount + reductionApplied) FROM payments WHERE studentId = ?", id)[0]["SUM(amount + reductionApplied)"] or 0
        multiplier = (db.execute("SELECT SUM(groupSize) FROM bookings WHERE studentId = ? AND completed = 1", id)[0]["SUM(groupSize)"]) or 0
        amountDue = (int(multiplier) * float(pricePerStudent)) - float(amountPaid)

        # Enter all data into the table
        db.execute("UPDATE students SET nberLessons = ?, nberCancelled = ?, amountPaid = ?, amountDue = ? WHERE id = ?",
            nberLessons, nberCancelled, amountPaid, amountDue, id)


def extractTopics(topics, idnum, dictionary):
    if topics != "":
        topics = topics.split(', ')
        for topic in topics:
            # Capitalize the topics
            topic = topic.capitalize()

            # Add a new topics to topicslist if needed
            if topic not in topiclist:
                topiclist.append(topic)

            # Set up the string to add to the categoryId
            # If this topic is not yet a key in the dictionary:
            if topic not in dictionary:
                dictionary[topic] = str(idnum)
            # If it is already a key, add this resources id number to the string associated with that key
            else: 
                dictionary[topic] = dictionary[topic] + ", " + str(idnum)

def linkTopics_Resourses(dictionary, category):
    for topic in dictionary:
        t = dictionary[topic].split(', ')
        for x in range(len(t)):
            ti = db.execute("SELECT id FROM topics WHERE topic = ?", topic)[0]["id"]
            db.execute("INSERT INTO topicLink (topicId, resourceId, resourceType) VALUES (?, ?, ?)", ti, t[x], category)

def getResourceId(value, table):
    x = db.execute("SELECT id FROM ? WHERE title = ?", table, value)[0]["id"]
    return x

main()