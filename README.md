# ENGLISH LESSON ORGANISER
## By Izzy Pickering for CS50
### [Video Demo] (https://www.youtube.com/watch?v=YOWPUXCu1Ls&feature=youtu.be)


### Description:
This software is made mainly for private tutors.
The purpose is to serve as a database containing student details, payment / financial details and a list of resources that is easily searched.


### Built with
- Python
- SQL
- PyQt5


### Programme content
#### Files
##### application.py
This file's sole purpose is to execute the application. It contains the software's main() function.

##### LayoutClasses.py
This file is used to define the various classes used from PyQt5 and to overwrite the style of some of these classes.
In most cases, the overwriting was to improve readability (e.g. increasing the size of the fonts, increasing the size of the boxes, setting the style sheets).

##### Tabs.py
This file sets up the tabs. It defines what each one contains and how they should behave in specific situations.

###### Tab 1 - 'Bookings'
This tab gathers all data related to the bookings.

The top segment is for adding new bookings. Once entered, the booking will be added automatically to the 'Current bookings' table.

The bottom table includes a list of all current bookings. The details of the bookings can be modified directly in the table if required. The user can add a list of the resources used for the lesson and a general subject (this data will be used in the 'knowledge' table).

###### Tab 2 - 'Payments'
This tab gathers all data related to the payments.

The top segment provides a monthly summary of payments and number of lessons completed. The graph and table are programmed to add columns every year with a limit of 5 years; 2020 being the first possible year.

The bottom segment is divided in 2 parts.
The left side provides a list of all active students and how much they currently owe.
The right side is a form to be completed when adding new payments. Once submitted, all linked tables will be automatically updated.

###### Tab 3 - 'Student Summary'
This tab gathers all data related to the students.

At the top of the tab, the user selects which student's details they would like to view using the drop-down menu. By ticking the box next to the drop-down menu, they can include non-active students in the drop-down list. Once a student selected, all other tables with populate automatically with data about that student.

The first segment under the selection box is the student’s contact details and useful information. This data can only be modified by clicking on the 'Change Contact Details' button. The other button is to either deactivate the student (if they are no longer a student) or to reactivate them (if they return for more lessons).

The table in the top right side of the screen provides the basic data related to the number of completed and cancelled lessons and the total amount paid for selected periods by that student. The period can be modified by choosing from the 2 drop-down menus above the table (one for the month, the other for the year).

The bottom part of the screen – called 'Student's knowledge' – is a work in progress. It will use the information gathered from the bookings table.

###### Tab 4 - 'Search resources'
This tab is used to search all the resources in the database. The result is divided into 5 tables, one for each type (i.e. lessons, books, games, craft ideas and flashcards). This data can be modified directly within the tables if needed (i.e. if errors or spelling mistakes). The resources can also be ‘deleted’ from this tab too. Once ‘deleted’, they will no longer appear in the searches but will only be marked as not active in the actual database.

The search takes into consideration all columns of the resource tables to find relevant results.

###### Tab 5 - 'Add students'
This tab is used to add new students to the database.

The minimum requirement is that the student have a name. The other rows can be left blank, noting however that if there is no value in the ‘Price per student’ row, 0€ will be added to the ‘Money owed’ table when lessons are marked as completed.

Once submitted, they will automatically be added to the relevant drop-down menus, the 'Money owed' table on the 'Payments' tab and the 'Student Summary' tab.

###### Tab 6 - 'Add resources'
This tab is used to add new resources to the database.

Each type requires different information thus the user first needs to select what type of resource they want to add.

The minimum requirement is that the resource have a title. The other rows can be left blank, noting however that the more details added, the more likely the resource will be accurately found when using the ‘search’ function.

Once submitted, the new resource will automatically be added to the relevant drop-down menus and will be found when using the 'Search resources' tab.


##### UpdateDBfromCSV.py
This file can be launched within an IDE to update the database from the various CSV files contained in the 'Database' folder.
This can used for multiple reasons including:
- first setting up the database if the user prefers entering the data into CSV rather than adding them one by one via the software.
- correcting big segments of the database
- deleting data permanently
The plan is to include a button in the programme to call this function (to avoid having to run UpdateDBfromCSV.py manually from the IDE).

#### Folders
##### Database
Contains all the CSV files and the db file. All data added using the software will be added to both the db database and the corresponding CSV file.

This folder also contains txt files. The lists in those txt files are used to populate the checkboxes lists in the "Add resources" tab.


### Before starting
Make sure you have the right programmes installed on your computer to run the software:
1. Python 3.x:
Install python 3: https://www.python.org/downloads/

2. PyQt5:
In the computer's search bar, look for "Command Prompt"
In the text area, enter: pip install PyQt5
In the text area, enter: pip install PyQtChart


### Getting Started
#### Launch the programme
Run application.py to open the programme.

#### Setting up the database
Option 1: Set up the database by completing the CSV files directly then running UpdateDBfromCSV.py.
Option 2: Set up the database by entering the data directly via the programme.


### Future developments
- Setting up an icon to be able to launch the programme directly on the desktop.
- Setting up a button in the programme to call the updateDBfromCSV function (to avoid having to run it manually from the IDE).
- Completing the 'Knowledge' table in the 'Students' tab.
- Setting up a segment to be able to view old data.
- Setting up a 'print' function.
- Setting up an option to correct the financial data.
- Setting up an option to delete topics.
