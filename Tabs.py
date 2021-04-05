# Add tabs as describe on https://doc-snapshots.qt.io/qtforpython-dev/PySide2/QtWidgets/QTabBar.html 
# and https://www.tutorialspoint.com/pyqt/pyqt_qtabwidget.htm

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis, QChart, QChartView
from LayoutClasses import *
import cs50
import csv
import datetime
import math
import os

db = cs50.SQL("sqlite:///Database/resources.db")

class Tabs(QtWidgets.QTabWidget):

    def __init__(self, parent=None):
        super(Tabs, self).__init__(parent)
        # Set the title of the programme
        self.setWindowIcon(QtGui.QIcon("Images/Logo.jpeg"))
        self.setWindowTitle("English Lesson Organiser")
                
        # Set the general style of the interface
        # Supporting many styling tags such as width, height, color, background-color, borders, padding, margin and other.
        self.setStyleSheet("QWidget {background-color: rgba(231,231,231,255); font: 17px;}"
            "QScrollBar:horizontal {width: 1px; height: 1px; background-color: rgba(0,41,59,255);}"
            "QScrollBar:vertical {width: 1px; height: 1px; background-color: rgba(0,41,59,255);}")
        self.setWindowOpacity(1)
        
        # Set up values that are useful in multiple segments of the code
        self.blockage = "no"
        # Values to show are from 5 years ago to this year with a limit at company inception
        self.year = datetime.datetime.now().year
        if self.year - 5 >= 2020:
            self.yearRange = range(self.year - 5, self.year + 1, 1)
        else:
            self.yearRange = range(2020, self.year + 1, 1)
        self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December", "Total"]

        # Set the positioning of the window.
        # Need to get a desktop resolution since we are setting size related to desktop resolution.
        # (copied from https://www.zeolearn.com/magazine/10-steps-for-getting-started-guis-with-python)
        desktop = QtWidgets.QApplication.desktop()
        self.resolution = desktop.availableGeometry()
        self.move(self.resolution.center() - self.rect().center())  
        self.setMinimumWidth(self.resolution.width() / 2)
        self.setMinimumHeight(self.resolution.height() / 1.5)
        

        # Add the required number of pages
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()

        # Attach tabs to those pages
        self.addTab(self.tab1, "Bookings ")
        self.addTab(self.tab2, "Payments ")
        self.addTab(self.tab3, "Student summary ")
        self.addTab(self.tab4, "Search resources ")
        self.addTab(self.tab5, "Add students ")
        self.addTab(self.tab6, "Add resources ")

        # Set the UI
        self.tab1_userinterface()
        self.tab2_userinterface()
        self.tab3_userinterface()
        self.tab4_userinterface()
        self.tab5_userinterface()
        self.tab6_userinterface()


    def tab1_userinterface(self):
        self.layout1 = QGridLayout()

        # SET UP AND ADD THE BOOKING FORM
        self.newBooking = QFormLayout()
        # Add title
        self.addBooking = QLabel("ADD BOOKINGS")
        self.setFontTitles(self.addBooking)
        self.newBooking.addRow(self.addBooking)
        # Add students
        self.studentLabel = QLabel("Student")
        self.studentPlaceholder1 = QComboBox()
        self.activeStudentList(self.studentPlaceholder1)
        self.newBooking.addRow(self.studentLabel, self.studentPlaceholder1)
        # Set up the other Widgets that need to be added
        self.date = QDateEdit()
        self.date.setDate(QtCore.QDate.currentDate())
        self.date.setDisplayFormat("dd/MM/yyyy")
        self.date.setCalendarPopup(True)
        self.dateLabel = QLabel("Date")
        self.newBooking.addRow(self.dateLabel, self.date)
        self.time = QTimeEdit()
        self.time.setTime(QtCore.QTime.currentTime())
        self.timeLabel = QLabel("Time")
        self.newBooking.addRow(self.timeLabel, self.time)
        # Add the confirm button
        self.confirmation_button1 = self.submitButton()
        self.newBooking.addRow(self.confirmation_button1)
        self.confirmation_button1.clicked.connect(self.saveBooking) 
        # Add all the Widgets to the grid
        self.layout1.addLayout(self.newBooking, 0, 0, 4, 4, alignment=Qt.AlignCenter)
    

        # SET UP A LIST OF ALL THE CURRENT BOOKINGS
        # Add the title
        self.bookingLabel = QLabel("CURRENT BOOKINGS")
        self.setFontTitles(self.bookingLabel)
        # Set up the table to contain the booking details
        self.bookingDetailTable = QTableWidget()
        self.bookingDetailTable.setColumnCount(13)
        self.bookingDetailTable.setHorizontalHeaderLabels(["Id", "Name", "Date", "Time", "Size", 
            "Lesson Subject", "Lessons used", "Books used", "Games used", "Craft ideas used",
            "", "", ""])
        self.bookingDetailTable.setAlternatingRowColors(True)
        self.bookingDetailTable.setColumnHidden(0, True)
        # Set the size of the columns
        # Set columns to stretch
        sc = [5, 6, 7, 8, 9]
        for c in sc:
            self.bookingDetailTable.horizontalHeader().setSectionResizeMode(c, QHeaderView.Stretch) 
        # Set Columns to size to content
        rc = [1, 2, 3, 4, 10, 11, 12]
        for c in rc:
            self.bookingDetailTable.horizontalHeader().setSectionResizeMode(c, QHeaderView.ResizeToContents)
        # Populate the table
        self.populateBookingsTable()
        # What to do if cell content is changed manually (Only for cells 'Date', 'Time' and 'Group size')
        self.bookingDetailTable.itemChanged.connect(lambda: self.saveBookingChanged(self.bookingDetailTable.currentRow(), self.bookingDetailTable.currentColumn()))
        # Reorder based on column header clicked
        self.bookingDetailTable.horizontalHeader().sectionClicked.connect(lambda: self.reorderTable(self.bookingDetailTable, self.bookingDetailTable.currentColumn()))
        
        # Add the table to the layout
        self.layout1.addWidget(self.bookingLabel, 6, 0, 1, 3)
        self.layout1.addWidget(self.bookingDetailTable, 7, 0, 1, 20)

    
        # Set column padding
        self.layout1.setColumnMinimumWidth(0, 20)
        self.layout1.setRowMinimumHeight(5, 40)
        self.layout1.setRowMinimumHeight(30, 40)


        # Print the self.layout1 onto the screen
        self.tab1.setLayout(self.layout1)        


    def tab2_userinterface(self):
        self.layout2 = QGridLayout()

        # ADD MONTHLY AMOUNTS TO DECLARE TO URSSAF
        # Add the title
        self.monthlyLabel = QLabel("MONTHLY SUMMARY")
        self.setFontTitles(self.monthlyLabel)
        self.layout2.addWidget(self.monthlyLabel, 0, 0)
        # Set up the table
        self.monthlySummary = QTableWidget()
        self.setScrollBar(self.monthlySummary)
        self.monthlySummary.setColumnCount(14)
        self.monthlySummary.setRowCount(13)
        self.monthlySummary.setHorizontalHeaderLabels(["Period", "Lessons", "General\npayments", "Cesu\npayments", "Total income", "", "Lesson\n" + str(self.year - 1), "Total income\n" + str(self.year - 1), "", "Lessons\n" + str(self.year - 2), "Total income\n" + str(self.year - 2), "", "Lessons\n" + str(self.year - 3), "Total income\n" + str(self.year - 3)])
        self.monthlySummary.setAlternatingRowColors(True)
        # Set column width and height
        col = [0, 1, 2, 3, 4, 6, 7, 9, 10, 12, 13]
        for c in col:
            self.monthlySummary.horizontalHeader().setSectionResizeMode(c, QHeaderView.Stretch)
        smallcol = [5, 8, 11]
        for sc in smallcol:
            self.monthlySummary.setColumnWidth(sc, 5)
        for i in range(self.monthlySummary.rowCount()):
            self.monthlySummary.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        # Hide columns if not needed
        if self.year - 2 < 2020:
            self.monthlySummary.setColumnHidden(8, True)
            self.monthlySummary.setColumnHidden(9, True)
            self.monthlySummary.setColumnHidden(10, True)
        if self.year - 3 < 2020:
            self.monthlySummary.setColumnHidden(11, True)
            self.monthlySummary.setColumnHidden(12, True)
            self.monthlySummary.setColumnHidden(13, True)
        # Add the first column
        col0 = [QTableWidgetItem("January"), QTableWidgetItem("February"), QTableWidgetItem("March"), QTableWidgetItem("April"), QTableWidgetItem("May"), QTableWidgetItem("June"), QTableWidgetItem("July"), QTableWidgetItem("August"), QTableWidgetItem("September"), QTableWidgetItem("October"), QTableWidgetItem("November"), QTableWidgetItem("December"), QTableWidgetItem("TOTAL")]
        col0[-1].setFont(self.boldFont())
        for i in range(len(col0)):
            self.monthlySummary.setItem(i, 0, col0[i])
        # Populate the table
        self.populateMonthlyPaymentTable()
        # Add to the layout
        self.layout2.addWidget(self.monthlySummary, 1, 0, 10, 15)

        # ADD A GRAPH TO SHOW MONTHLY DATA
        self.layout2.addWidget(self.addGraph(), 1, 17, 10, 40)


        # ADD A TABLE OF THE AMOUNT OF MONEY OWED
        # Add the title
        amountdueLayout = QVBoxLayout()
        self.owedLabel = QLabel("MONEY OWED")
        self.setFontTitles(self.owedLabel)
        amountdueLayout.addWidget(self.owedLabel)
        # Set up the table to contain the money owed details
        self.paymentDetailTable = QTableWidget()
        self.setScrollBar(self.paymentDetailTable)
        self.paymentDetailTable.setColumnCount(2)
        self.paymentDetailTable.setHorizontalHeaderLabels(["Name", "Amount"])
        for i in range(self.paymentDetailTable.columnCount()):     
            self.paymentDetailTable.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        self.paymentDetailTable.setAlternatingRowColors(True)
        # Populate the table with all the students and how much they each owe
        self.populateAmountDueTable()
        # What to do if cell content is changed manually
        self.paymentDetailTable.itemChanged.connect(lambda: self.saveAmountChanged(self.paymentDetailTable.currentRow()))
        # Add to layout
        amountdueLayout.addWidget(self.paymentDetailTable)
        self.layout2.addLayout(amountdueLayout, 13, 0, 10, 5)


        # SET UP AND ADD THE PAYMENTS FORM
        self.newPayment = QFormLayout()
        # Add title
        self.addPayment = QLabel("ADD PAYMENTS")
        self.setFontTitles(self.addPayment)
        self.newPayment.addRow(self.addPayment)
        # Set the list of students to choose who paid
        self.paidbyLabel = QLabel("Paid by")
        self.studentPlaceholder2 = QComboBox()
        self.studentPlaceholder2.setFixedWidth(350)
        self.activeStudentList(self.studentPlaceholder2)
        self.newPayment.addRow(self.paidbyLabel, self.studentPlaceholder2)
        self.studentPlaceholder2.currentTextChanged.connect(self.setAmount)
        # Enter the date
        self.paymentDateLabel = QLabel("Date")
        self.paymentDate = QDateEdit()
        self.paymentDate.setDate(QtCore.QDate.currentDate())
        self.paymentDate.setDisplayFormat("dd/MM/yyyy")
        self.paymentDate.setCalendarPopup(True)
        self.paymentDate.setFixedWidth(350)
        self.newPayment.addRow(self.paymentDateLabel, self.paymentDate)
        # Set the amount
        self.amountLabel = QLabel("Amount")
        self.amount = QDoubleSpinBox()
        self.amount.setFixedWidth(350)
        self.newPayment.addRow(self.amountLabel, self.amount)
        # Set the payment method
        self.paymentMethods = QComboBox()
        self.paymentMethodLabel = QLabel("Payment Method")
        self.paymentMethods.setFixedWidth(350)
        self.paymentMethods.addItem("")
        self.paymentMethods.addItem("Cash")
        self.paymentMethods.addItem("Cesu")
        self.paymentMethods.addItem("Transfer")
        self.newPayment.addRow(self.paymentMethodLabel, self.paymentMethods)      
        # Apply reductions
        self.reduction = QHBoxLayout()
        self.reductionLabel = QLabel("Reduction applied")
        self.reductionResponse = QRadioButton("Yes")
        self.reductionResponse.clicked.connect(self.addReduction)
        self.newPayment.addRow(self.reductionLabel, self.reductionResponse)
        # Add the confirm button
        self.confirmation_button2 = self.submitButton()
        self.newPayment.addRow(self.confirmation_button2)
        self.confirmation_button2.clicked.connect(self.submitNewPayment)
        # Add the form to the tab layout
        self.layout2.addLayout(self.newPayment, 13, 6, 10, 4)


        # Set column padding
        self.layout2.setColumnMinimumWidth(16, 20)
        self.layout2.setRowMinimumHeight(12, 40)
        self.layout2.setRowMinimumHeight(24, 40)


        # Print the layout onto the screen
        self.tab2.setLayout(self.layout2)


    def tab3_userinterface(self):
        self.layout3 = QVBoxLayout()
        self.layout3.setAlignment(Qt.AlignTop)
        # Choose which student to review
        quieryLayout = QHBoxLayout()
        label1 = QLabel("Choose a student")
        quieryLayout.addWidget(label1)
        self.studentPlaceholder3 = QComboBox()
        self.activeStudentList(self.studentPlaceholder3)
        quieryLayout.addWidget(self.studentPlaceholder3)
        oldStudents = QCheckBox("Include old students")
        oldStudents.clicked.connect(lambda: self.oldStudentList(oldStudents, self.studentPlaceholder3))
        quieryLayout.addWidget(oldStudents)
        quieryLayout.addStretch()
        self.layout3.addLayout(quieryLayout)
        self.layout3.addSpacing(30)

        # Add the backbones of the layout
        # Add the contact details
        middleLayout = QHBoxLayout()
        segment1Layout = QVBoxLayout()
        segment1Layout.setAlignment(Qt.AlignTop)
        title1 = QLabel("Contact details and general information")
        self.setFontTitles(title1)
        segment1Layout.addWidget(title1)
        self.contactDetails = QFormLayout()
        self.contactDetailsForm(self.contactDetails)
        for i in range(self.contactDetails.rowCount()):
            self.contactDetails.itemAt(i, 1).widget().setReadOnly(True)
        
        # Add the pushbuttons (hidden)
        # 'change details' button
        self.changeDetails = QPushButton("Change Contact Details")
        self.changeDetails.setMaximumWidth(170)
        # Add the window to display the new form
        self.contactDetailWindow = QWidget()
        layout = QFormLayout()
        self.contactDetailWindow.setLayout(layout)
        self.contactDetailWindow.create()
        self.changeDetails.clicked.connect(lambda: self.updateContactDetails(self.studentPlaceholder3.currentText()))
        self.studentStatus = QPushButton()
        self.studentStatus.setMaximumWidth(170)
        self.studentStatus.clicked.connect(lambda: self.updateStudentStatus(self.studentStatus, self.studentPlaceholder3.currentText()))
        # Set the buttons to 'hidden'
        self.changeDetails.setVisible(False)
        self.studentStatus.setVisible(False)
        # Add the buttons to the layout
        buttonRow = QHBoxLayout()
        buttonRow.addWidget(self.changeDetails)
        buttonRow.addWidget(self.studentStatus)
        self.contactDetails.addRow(buttonRow)
        # Add the form to the layout
        segment1Layout.addLayout(self.contactDetails)
        middleLayout.addLayout(segment1Layout)
        middleLayout.addSpacing(30)


        # Add 'financial' data table
        segment2aLayout = QHBoxLayout()
        segment2bLayout = QVBoxLayout()
        title2 = QLabel("General Data")
        self.setFontTitles(title2)
        segment2aLayout.addWidget(title2)
        # Add a combobox to decide what period to view
        self.monthChoice = QComboBox()
        for month in self.months:
            self.monthChoice.addItem(month)
        self.monthChoice.setCurrentText("Total")
        self.monthChoice.currentTextChanged.connect(self.lessonQuantityTable)
        segment2aLayout.addWidget(self.monthChoice)
        self.yearChoice = QComboBox()
        for year in self.yearRange:
            self.yearChoice.addItem(str(year))
        self.yearChoice.setCurrentText(str(self.year))
        self.yearChoice.currentTextChanged.connect(self.lessonQuantityTable)
        segment2aLayout.addWidget(self.yearChoice)
        segment2aLayout.addStretch()
        segment2bLayout.addLayout(segment2aLayout)
        # Set up the table
        self.studentData = QTableWidget()
        self.setBorders(self.studentData)
        self.setScrollBar(self.studentData)
        self.studentData.setColumnCount(4)
        self.studentData.setHorizontalHeaderLabels(["Period", "N° of lessons", "N° of cancelled\nlessons", "Total amount\npaid"])
        for i in range(self.studentData.columnCount()):
            self.studentData.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch) 
        self.studentData.setRowCount(1)
        self.studentData.verticalHeader().setSectionResizeMode(0, QHeaderView.Stretch) 
        self.studentData.setFixedHeight(100)
        segment2bLayout.addWidget(self.studentData, 1, Qt.AlignTop)
        middleLayout.addLayout(segment2bLayout)
        self.layout3.addLayout(middleLayout, 1)
        self.layout3.addSpacing(30)


        # Add knowledge data table
        title3 = QLabel("Student's knowledge")
        self.setFontTitles(title3)
        self.layout3.addWidget(title3)

        self.studentKnowledge = QTableWidget()
        self.setBorders(self.studentKnowledge)
        self.setScrollBar(self.studentKnowledge)
        self.layout3.addWidget(self.studentKnowledge, 2)

        # Activate the content for that student
        self.studentPlaceholder3.currentTextChanged.connect(lambda: self.showStudentData(self.studentPlaceholder3.currentText()))

        # Print the layout onto the screen
        self.tab3.setLayout(self.layout3)


    def tab4_userinterface(self):
        self.layout4 = QFormLayout()
        self.textLabel = QLabel("What topic are you hoping to teach: ")
        self.text = QLineEdit()
        self.text.setStyleSheet("background-color: white; color: brown;")
        emptyspace = QVBoxLayout()
        emptyspace.addWidget(self.text)
        emptyspace.addSpacing(30)
        self.layout4.addRow(self.textLabel, emptyspace)


        # Lessons table
        self.titlelessons = QLabel("LESSONS")
        self.setFontTitles(self.titlelessons)
        self.foundLessons = QTableWidget()
        self.setBorders (self.foundLessons)
        self.setScrollBar (self.foundLessons)
        self.foundLessons.setColumnCount(7)
        self.foundLessons.setHorizontalHeaderLabels(["Id", "Title", "Publisher", "Type", "Activities", "File", "Del"])
        self.foundLessons.setColumnHidden(0, True)
        # Set columns to stretch
        sc = [1, 2, 3]
        for c in sc:
            self.foundLessons.horizontalHeader().setSectionResizeMode(c, QHeaderView.Stretch) 
        # Set Columns to size to content
        rc = [4, 6]
        for c in rc:
            self.foundLessons.horizontalHeader().setSectionResizeMode(c, QHeaderView.ResizeToContents)
        # Connect the 'file' file hyperlink to an action (i.e opening the file in it's own programme)
        self.foundLessons.cellClicked.connect(lambda: self.openTextFiles(self.foundLessons, self.foundLessons.currentRow(), self.foundLessons.currentColumn(), 5, "lessons"))
        # What to do if cell content is changed manually
        self.foundLessons.itemChanged.connect(lambda: self.resourceChanged(self.foundLessons, 'lessons', self.foundLessons.currentRow(), self.foundLessons.currentColumn(), "Database/Lessons.csv"))
        # Reorder based on column header clicked
        self.foundLessons.horizontalHeader().sectionClicked.connect(lambda: self.reorderTable(self.foundLessons, self.foundLessons.currentColumn()))

        # Book table
        self.titlebooks = QLabel("BOOKS")
        self.setFontTitles(self.titlebooks)
        self.foundBooks = QTableWidget()
        self.setBorders (self.foundBooks)
        self.setScrollBar (self.foundBooks)
        self.foundBooks.setColumnCount(11)
        self.foundBooks.setHorizontalHeaderLabels(["Id", "Title", "Author", "Collection", "Book\nN°", "Publisher", "Book type", "Subtype", "Level", "Description", "Del"])
        self.foundBooks.setColumnHidden(0, True)
        # Set smaller font for some of the hearders
        sfh = [4, 8]
        for h in sfh:
            self.foundBooks.horizontalHeaderItem(h).setFont(self.smallerFont())
        # Set columns to stretch
        sc = [1, 2, 3, 5, 6, 7, 9]
        for c in sc:
            self.foundBooks.horizontalHeader().setSectionResizeMode(c, QHeaderView.Stretch) 
        # Set Columns to size to content
        rc = [4, 8, 10]
        for c in rc:
            self.foundBooks.horizontalHeader().setSectionResizeMode(c, QHeaderView.ResizeToContents)
        # What to do if cell content is changed manually
        self.foundBooks.itemChanged.connect(lambda: self.resourceChanged(self.foundBooks, 'books', self.foundBooks.currentRow(), self.foundBooks.currentColumn(), "Database/Books.csv"))
        # Reorder based on column header clicked
        self.foundBooks.horizontalHeader().sectionClicked.connect(lambda: self.reorderTable(self.foundBooks, self.foundBooks.currentColumn()))

        # Set sub layout for bottom part of the screen
        self.bottomSegment = QHBoxLayout()
        self.bottomSegmenta = QVBoxLayout()
        self.bottomSegmentb = QVBoxLayout()
        self.bottomSegmentc = QVBoxLayout()

        # Game table
        self.titlegames = QLabel("GAMES")
        self.setFontTitles(self.titlegames)
        self.bottomSegmenta.addWidget(self.titlegames)
        self.foundGames = QTableWidget()
        self.setBorders (self.foundGames)
        self.setScrollBar (self.foundGames)
        self.foundGames.setColumnCount(10)
        self.foundGames.setHorizontalHeaderLabels(["Id", "Title", "Publisher", "Colour", "Game type", "Description", "Duration\n(min)", "N° of\nplayers", "Age", "Del"])
        self.foundGames.setColumnHidden(0, True)
        # Set smaller font for some of the hearders
        sfh = [6, 7, 8]
        for h in sfh:
            self.foundGames.horizontalHeaderItem(h).setFont(self.smallerFont())
        # Set columns to stretch
        sc = [1, 2, 4, 5]
        for c in sc:
            self.foundGames.horizontalHeader().setSectionResizeMode(c, QHeaderView.Stretch) 
        # Set Columns to size to content
        rc = [6, 7, 8, 9]
        for c in rc:
            self.foundGames.horizontalHeader().setSectionResizeMode(c, QHeaderView.ResizeToContents)
        # Add it to the bottom widget of the screen
        self.bottomSegmenta.addWidget(self.foundGames)
        # What to do if cell content is changed manually
        self.foundGames.itemChanged.connect(lambda: self.resourceChanged(self.foundGames, 'games', self.foundGames.currentRow(), self.foundGames.currentColumn(), "Database/Games.csv"))
        # Reorder based on column header clicked
        self.foundGames.horizontalHeader().sectionClicked.connect(lambda: self.reorderTable(self.foundGames, self.foundGames.currentColumn()))

        # Crafts table
        self.titlecrafts = QLabel("CRAFTS")
        self.setFontTitles(self.titlecrafts)
        self.bottomSegmentb.addWidget(self.titlecrafts)
        self.foundCrafts = QTableWidget()
        self.setBorders (self.foundCrafts)
        self.setScrollBar (self.foundCrafts)
        self.foundCrafts.setColumnCount(7)
        self.foundCrafts.setHorizontalHeaderLabels(["Id", "Title", "Materials", "Duration\n(min)", "Image", "Instructions\nto print", "Del"])
        self.foundCrafts.setColumnHidden(0, True)
        # Set smaller font for some of the hearders
        sfh = [3]
        for h in sfh:
            self.foundCrafts.horizontalHeaderItem(h).setFont(self.smallerFont())
        # Set columns to stretch
        sc = [1, 2, 4, 5]
        for c in sc:
            self.foundCrafts.horizontalHeader().setSectionResizeMode(c, QHeaderView.Stretch) 
        # Set Columns to size to content
        rc = [3, 6]
        for c in rc:
            self.foundCrafts.horizontalHeader().setSectionResizeMode(c, QHeaderView.ResizeToContents)
        # Connect the 'image' hyperlink to an action
        self.foundCrafts.cellClicked.connect(lambda: self.showImages(self.foundCrafts, self.foundCrafts.currentRow(), self.foundCrafts.currentColumn(), "crafts"))
        # Connect the 'instructions' file hyperlink to an action (i.e opening the file in it's own programme)
        self.foundCrafts.cellClicked.connect(lambda: self.openTextFiles(self.foundCrafts, self.foundCrafts.currentRow(), self.foundCrafts.currentColumn(), 5, "crafts"))
        # Add it to the bottom widget of the screen
        self.bottomSegmentb.addWidget(self.foundCrafts)
        # What to do if cell content is changed manually
        self.foundCrafts.itemChanged.connect(lambda: self.resourceChanged(self.foundCrafts, 'crafts', self.foundCrafts.currentRow(), self.foundCrafts.currentColumn(), "Database/Arts & crafts.csv"))
        # Reorder based on column header clicked
        self.foundCrafts.horizontalHeader().sectionClicked.connect(lambda: self.reorderTable(self.foundCrafts, self.foundCrafts.currentColumn()))

        # Flashcard table
        self.titleflash = QLabel("FLASHCARDS")
        self.setFontTitles(self.titleflash)
        self.bottomSegmentc.addWidget(self.titleflash)
        self.foundFlashcards = QTableWidget()
        self.setBorders (self.foundFlashcards)
        self.setScrollBar (self.foundFlashcards)
        self.foundFlashcards.setColumnCount(3)
        self.foundFlashcards.setHorizontalHeaderLabels(["Id", "Title", "Del"])
        self.foundFlashcards.setColumnHidden(0, True)
        self.foundFlashcards.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.foundFlashcards.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        # Add it to the bottom widget of the screen
        self.bottomSegmentc.addWidget(self.foundFlashcards)
        # What to do if cell content is changed manually
        self.foundFlashcards.itemChanged.connect(lambda: self.resourceChanged(self.foundFlashcards, 'flashcards', self.foundFlashcards.currentRow(), self.foundFlashcards.currentColumn(), "Database/Flashcards.csv"))
        # Reorder based on column header clicked
        self.foundFlashcards.horizontalHeader().sectionClicked.connect(lambda: self.reorderTable(self.foundFlashcards, self.foundFlashcards.currentColumn()))


        # Add the Tables to the layout
        self.layout4.addRow(self.titlelessons)
        self.layout4.addRow(self.foundLessons)
        self.layout4.addRow(self.titlebooks)
        self.layout4.addRow(self.foundBooks)
        self.bottomSegment.addLayout(self.bottomSegmenta, 4)
        self.bottomSegment.addLayout(self.bottomSegmentb, 3)
        self.bottomSegment.addLayout(self.bottomSegmentc, 1)
        self.layout4.addRow(self.bottomSegment)


        # Populate the tables 
        self.text.textChanged.connect(self.search)


        # Print the layout onto the screen
        self.tab4.setLayout(self.layout4)


    def tab5_userinterface(self):
        self.layout5 = QFormLayout()

        # Add contact details
        self.newStudentNameLabel = QLabel("Name")
        self.newStudentName = QLineEdit()
        self.layout5.addRow(self.newStudentNameLabel, self.newStudentName)

        self.newStudentAddressLabel = QLabel("Address")
        self.newStudentAddress = QLineEdit()
        self.layout5.addRow(self.newStudentAddressLabel, self.newStudentAddress)

        self.newStudentPhoneLabel = QLabel("Phone")
        self.newStudentPhone = QLineEdit()
        self.layout5.addRow(self.newStudentPhoneLabel, self.newStudentPhone)

        self.newStudentEmailLabel = QLabel("Email")
        self.newStudentEmail = QLineEdit()
        self.layout5.addRow(self.newStudentEmailLabel, self.newStudentEmail)

        # Add group details
        self.groupSize = QSpinBox()
        self.groupSize.setMinimum(1)
        self.groupSizeLabel = QLabel("Group size")
        self.layout5.addRow(self.groupSizeLabel, self.groupSize)
        self.groupSize.textChanged.connect(self.addAges)
        self.ages = QHBoxLayout()
        self.ages.addWidget(QSpinBox())
        self.ageLabel = QLabel("Ages")
        self.layout5.insertRow(5, self.ageLabel, self.ages)
        self.hobbiesLabel = QLabel("Hobbies")
        self.hobbies = QLineEdit()
        self.layout5.addRow(self.hobbiesLabel, self.hobbies)

        # Add box with the amount per lesson per student
        self.amountPerStudent = QDoubleSpinBox()
        self.amountPerStudentLabel = QLabel("Price per student")
        self.amountPerStudent.setDecimals(2)
        self.amountPerStudent.setValue(20)
        self.amountPerStudent.setMinimum(10)
        self.amountPerStudent.setMaximum(50)
        self.layout5.addRow(self.amountPerStudentLabel, self.amountPerStudent)      
        
        # Add the submit button
        self.confirmation_button5 = self.submitButton()
        self.layout5.addRow(self.confirmation_button5)
        
        # Connect the submit button to a function
        self.confirmation_button5.clicked.connect(self.saveNewStudent)


        # Print the self.layout5 onto the screen
        self.tab5.setLayout(self.layout5)


    def tab6_userinterface(self):     
        # Organise the general layout 
        self.layout6 = QFormLayout()

        # Set up a list of different resources to chose from
        self.materialType = QHBoxLayout()
        self.materialTypeLabel = QLabel("Type of material")
        self.materialTypeLabel.setFixedWidth(120)
        self.lessonBox = QRadioButton("Lesson")
        self.bookBox = QRadioButton("Book")
        self.gameBox = QRadioButton("Game")
        self.craftBox = QRadioButton("Craft")
        self.flashcardBox = QRadioButton("Flashcard")
        self.materialType.addWidget(self.lessonBox)
        self.materialType.addWidget(self.bookBox)
        self.materialType.addWidget(self.gameBox)
        self.materialType.addWidget(self.craftBox)
        self.materialType.addWidget(self.flashcardBox)
        self.materialType.addStretch()
        layouthelp = QVBoxLayout()
        layouthelp.addLayout(self.materialType)
        layouthelp.addSpacing(30)
        self.layout6.addRow(self.materialTypeLabel, layouthelp)

        # Automate the info to appear based on what is clicked
        self.lessonBox.clicked.connect(self.somethingClicked)
        self.bookBox.clicked.connect(self.somethingClicked)
        self.gameBox.clicked.connect(self.somethingClicked)
        self.craftBox.clicked.connect(self.somethingClicked)
        self.flashcardBox.clicked.connect(self.somethingClicked)

        # Print the layout onto the screen
        self.tab6.setLayout(self.layout6)



    # Actions for TAB 1
    def saveBooking(self):
        if self.studentPlaceholder1.currentText() == "":
            self.missingData(self.studentPlaceholder1)
        
        else:
            # Add to the database
            self.si = db.execute("SELECT id FROM students WHERE name = ?", self.studentPlaceholder1.currentText())[0]["id"]
            self.fullDate = str(self.date.text()).split('/')
            self.m = int(self.fullDate[1])
            self.y = int(self.fullDate[2])
            self.gs = db.execute("SELECT group_size FROM students WHERE name = ?", self.studentPlaceholder1.currentText())[0]["group_size"]
            try:
                # Make sure the csv file isn't open
                with open ("Database/Bookings.csv", "a") as bookings:
                    db.execute("INSERT INTO bookings (studentId, date, month, year, time, groupSize, completed, cancelled) VALUES (?, ?, ?, ?, ?, ?, 0, 0)",
                        self.si, self.date.text(), self.m, self.y, self.time.text(), self.gs)
                    newbookingId = db.execute("SELECT id FROM bookings ORDER BY id DESC LIMIT 1")[0]["id"]
                    bookings.writelines(str(newbookingId) + ',' + self.studentPlaceholder1.currentText() + ',' + self.date.text() + ',' + str(self.time.text()) + ',' + str(self.gs) + '\n')

                # Add to the current bookings table
                self.populateBookingsTable()
                
                # Clear the form
                self.studentPlaceholder1.setStyleSheet("background-color: ")
                self.studentPlaceholder1.setCurrentIndex(0)
                self.date.setDate(QtCore.QDate.currentDate())
                self.time.setTime(QtCore.QTime.currentTime())

            # What to do if the file is open
            except PermissionError:
                self.fileOpen()

    def populateBookingsTable(self):
        self.bookingList = db.execute("SELECT * FROM bookings WHERE completed = 0 AND cancelled = 0 ORDER BY YEAR, MONTH, date, TIME")
        self.bookingDetailTable.setRowCount(len(self.bookingList))
        for i in range(len(self.bookingList)):
            self.bookingDetailTable.setItem(i, 0, QTableWidgetItem(str(self.bookingList[i]["id"])))
            self.studentName = db.execute("SELECT name FROM students WHERE id IN (SELECT studentId FROM bookings WHERE id = ?)", self.bookingList[i]["id"])[0]["name"]
            self.bookingDetailTable.setItem(i, 1, QTableWidgetItem(self.studentName))
            self.bookingDetailTable.setItem(i, 2, QTableWidgetItem(str(self.bookingList[i]["date"])))
            self.bookingDetailTable.setItem(i, 3, QTableWidgetItem(str(self.bookingList[i]["TIME"])))
            self.bookingDetailTable.setItem(i, 4, QTableWidgetItem(str(self.bookingList[i]["groupSize"])))
            self.completeTable(i)

    def completeTable(self, row):
        self.bookingDetailTable.setCellWidget(row, 5, (QLineEdit()))
        self.lessons = QComboBox()
        self.lessonList(self.lessons)
        self.books = QComboBox()
        self.bookList(self.books)
        self.games = QComboBox()
        self.gameList(self.games)
        self.crafts = QComboBox()
        self.craftList(self.crafts)
        self.bookingDetailTable.setCellWidget(row, 6, self.lessons)
        self.bookingDetailTable.setCellWidget(row, 7, self.books)
        self.bookingDetailTable.setCellWidget(row, 8, self.games)
        self.bookingDetailTable.setCellWidget(row, 9, self.crafts)
        self.bookingDetailTable.setCellWidget(row, 10, QRadioButton("Cancelled"))
        self.bookingDetailTable.setCellWidget(row, 11, QRadioButton("Completed"))
        self.saveButton = QPushButton("Save")
        self.bookingDetailTable.setCellWidget(row, 12, self.saveButton)
        self.saveButton.clicked.connect(self.saveAdditionalDetails)

    def saveAdditionalDetails(self):
        row = self.bookingDetailTable.currentRow()
        bookingId = self.bookingDetailTable.item(row, 0).text()
        nameOfRow = self.bookingDetailTable.item(row, 1).text()
        dateOfRow = self.bookingDetailTable.item(row, 2).text()
        adps = db.execute("SELECT pricePerStudent FROM students WHERE name = ?", nameOfRow)[0]["pricePerStudent"]
        gs = self.bookingDetailTable.item(row, 4).text()[0]
        toAdd = float(adps) * int(gs)
        # Resources to add
        rowSubject = self.bookingDetailTable.cellWidget(row, 5).text()
        rowLesson = self.bookingDetailTable.cellWidget(row, 6).currentText()
        rowBook = self.bookingDetailTable.cellWidget(row, 7).currentText()
        rowGame = self.bookingDetailTable.cellWidget(row, 8).currentText()
        rowCraft = self.bookingDetailTable.cellWidget(row, 9).currentText()

        # What to do if 'cancelled' is checked
        if self.bookingDetailTable.cellWidget(row, 10).isChecked():
            # Make sure the csv file isn't open
            try:
                with open ("Database/BookingsPart2.csv", "a") as bookingsPart2:
                    # Update the database
                    db.execute("UPDATE bookings SET cancelled = 1 WHERE id = ?", bookingId)
                    db.execute("UPDATE students SET nberCancelled = nberCancelled + 1 WHERE name = ?", nameOfRow)
                    bookingsPart2.writelines(bookingId + ',' + dateOfRow + ',' + nameOfRow + ',,x\n')
                    # Delete the data from the bookings table
                    self.bookingDetailTable.removeRow(row)
            # What to do if the file is open
            except PermissionError:
                self.fileOpen()

        # What to do if 'completed' is checked
        elif self.bookingDetailTable.cellWidget(row, 11).isChecked():

            self.allBookingData = "Ok"
            # If no details in the books/games used & topics, make sure this is not an error 
            if rowSubject == "" and rowBook == "" and rowGame == "" and rowCraft == "" and rowLesson == "":
                confirmationMessage = QMessageBox()
                confirmationMessage.setIcon(QMessageBox.Question)
                confirmationMessage.setText("Are you sure you don't want to add additional details to this booking?")
                confirmationMessage.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                confirmationMessage.buttonClicked.connect(lambda: self.confirmationMessageOutcome(confirmationMessage.clickedButton()))
                confirmationMessage.exec_()

            # If all the details have been provided, finish filling tables and deleting row
            if self.allBookingData == "Ok":
                # Make sure the csv file isn't open
                try:
                    # Update the database
                    with open ("Database/BookingsPart2.csv", "a") as bookingsPart2:
                        db.execute("UPDATE bookings SET completed = 1 WHERE id = ?", bookingId)
                        db.execute("UPDATE students SET nberLessons = nberLessons + 1, amountDue = amountDue + ? WHERE name = ?", toAdd, nameOfRow)
                        bookingsPart2.writelines(bookingId + ',' + dateOfRow + ',' + nameOfRow + ',x,\n')
                        # Add the additional details to the database
                        self.addToStudentDetails(row, bookingId, nameOfRow, rowSubject, rowLesson, rowBook, rowGame, rowCraft)
                        # Pause the function if the file used in above function caused an issue
                        if self.blockage == "no":
                            # Update the amount due table
                            self.populateAmountDueTable()
                            # Add +1 to number of completed lessons that month
                            self.populateMonthlyPaymentTable()
                            # Delete the data from the bookings table
                            self.bookingDetailTable.removeRow(row)     
                # What to do if the file is open
                except PermissionError:
                    self.fileOpen()


        # What to do if only adding resources
        else: 
            # Add the data to the database
            self.addToStudentDetails(row, bookingId, nameOfRow, rowSubject, rowLesson, rowBook, rowGame, rowCraft)
            # Clear the cells
            self.bookingDetailTable.cellWidget(row, 5).clear()
            self.bookingDetailTable.cellWidget(row, 6).setCurrentIndex(0)
            self.bookingDetailTable.cellWidget(row, 7).setCurrentIndex(0)
            self.bookingDetailTable.cellWidget(row, 8).setCurrentIndex(0)
            self.bookingDetailTable.cellWidget(row, 9).setCurrentIndex(0)
            
    def confirmationMessageOutcome (self, btn):
        if btn.text()[1:] == "Yes":
            self.allBookingData = "Ok"
        else:
            self.allBookingData = "Not Ok"

    def addToStudentDetails (self, row, bookingId, name, subject, lesson, book, game, craft):
        # Get the name id from the database
        nameId = db.execute("SELECT id FROM students WHERE name = ?", name)[0]["id"]
        # Make sure the csv file isn't open
        try:
            with open ("Database/StudentdetailsA.csv", "a") as studentDetailsA:
                # Add the data to the student_details1 table
                if lesson != "":
                    db.execute("INSERT INTO student_details1 (studentId, resourceId, resourceType, bookingId) VALUES (?, (SELECT id FROM lessons WHERE title = ?), ?, ?)",
                        nameId, lesson, "lessons", bookingId)
                    studentDetailsA.writelines(name + ',' + lesson + ',lessons,' + str(bookingId) + "\n")
                if book != "":
                    db.execute("INSERT INTO student_details1 (studentId, resourceId, resourceType, bookingId) VALUES (?, (SELECT id FROM books WHERE title = ?), 'books', ?)",
                        nameId, book, bookingId)
                    studentDetailsA.writelines(name + ',' + book + ',books,' + str(bookingId) + "\n")
                if game != "":
                    db.execute("INSERT INTO student_details1 (studentId, resourceId, resourceType, bookingId) VALUES (?, (SELECT id FROM games WHERE title = ?), 'games', ?)",
                        nameId, game, bookingId) 
                    studentDetailsA.writelines(name + ',' + game + ',games,' + str(bookingId) + "\n")
                if craft != "":
                    db.execute("INSERT INTO student_details1 (studentId, resourceId, resourceType, bookingId) VALUES (?, (SELECT id FROM crafts WHERE title = ?), 'crafts', ?)",
                        nameId, craft, bookingId)
                    studentDetailsA.writelines(name + ',' + craft + ',crafts,' + str(bookingId) + "\n")

                # Update the subject 
                if subject != "":
                    db.execute("UPDATE bookings SET subject = ? WHERE id = ?", subject, bookingId)
                    studentDetailsA.writelines(name + ',' + subject + ',subject,' + bookingId + "\n")
            self.blockage = "no"
        # What to do if the file is open
        except PermissionError:
            self.blockage = "yes"           
            self.fileOpen()

    def saveBookingChanged(self, row, column):
        if column == 1 or column == 2 or column == 3 or column == 4:
            bookingId = self.bookingDetailTable.item(row, 0).text()
            newdate = self.bookingDetailTable.item(row, 2).text()
            dor = str(newdate).split("/")
            newMonth = dor[1]
            newYear = dor[2] 
            newTime = self.bookingDetailTable.item(row, 3).text()
            newGroupSize = self.bookingDetailTable.item(row, 4).text()
            # Make sure the csv file isn't open
            try:
                with open ("Database/Bookings.csv", "a"):
                    self.blockage = "no"
            except PermissionError:
                self.blockage = "yes"
                self.fileOpen()
            
            if self.blockage == "no":
                # Update the bookings database
                db.execute("UPDATE bookings SET date = ?, MONTH = ?, YEAR = ?, TIME = ?, groupSize = ? WHERE id = ?", newdate, newMonth, newYear, newTime, newGroupSize, bookingId)
                data = db.execute("SELECT id, studentId, date, TIME, groupSize FROM bookings")
                for i in range(len(data)):
                    data[i]["studentId"] = db.execute("SELECT name FROM students WHERE id IN (SELECT studentId FROM bookings WHERE id = ?)", i + 1)[0]["name"]
                self.rewriteCSVFile("Database/Bookings.csv", data)
            else:
                self.bookingDetailTable.blockSignals(True)
                self.populateBookingsTable()
                self.bookingDetailTable.blockSignals(False)



    # Actions for TAB 2
    def addGraph(self):
        # Code taken for https://doc.qt.io/qt-5/qtcharts-barchart-example.html
        # Set up the series to contain the data
        series = QBarSeries()
        
        # Set the max value for the y axis
        maxValue = 0

        # Gather the data
        for year in self.yearRange:
            setX = QBarSet(str(year))
            for i in range(13):
                genaralPayments = db.execute("SELECT SUM (amount) FROM payments WHERE method != 'Cesu' AND month = ? AND year = ?", i + 1, year)[0]["SUM (amount)"]
                cesuPayments = db.execute("SELECT SUM (amount) FROM payments WHERE method = 'Cesu' AND month = ? AND year = ?", i + 1, year)[0]["SUM (amount)"]
                # Make sure it's not a 'None' type
                if genaralPayments == None:
                    genaralPayments = 0
                if cesuPayments == None:
                    cesuPayments = 0   
                total = (genaralPayments + cesuPayments)                 
                # Set the max value for the y axis
                if total > maxValue:
                    maxValue = total
                setX.append(total)             
                series.append(setX)

        # Add the data to the chart
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Monthly figures")

        # Set up the chart layout
        axisX = QBarCategoryAxis()
        axisX.append(self.months)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        axisY = QValueAxis()
        # Round the max value up
        mvs = str(int(maxValue))
        newMax = int(mvs[0]) + 1
        for i in range(1, len(mvs), 1):
            newMax *= 10
        axisY.setRange(0, newMax)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignRight)
        
        # Turn the chart into a widget
        self.chartView = QChartView()
        self.chartView.setChart(chart)

        # Return the graph
        return self.chartView

    def populateMonthlyPaymentTable(self):
        # Calculate the total values
        self.row12column1 = 0
        self.row12column2 = 0
        self.row12column3 = 0
        self.row12column4 = 0
        self.row12column6 = 0
        self.row12column7 = 0
        self.row12column9 = 0
        self.row12column10 = 0
        self.row12column12 = 0
        self.row12column13 = 0
        
        for i in range(12):
            # Fill in the data for this year
            self.column1 = db.execute("SELECT COUNT(*) FROM bookings WHERE completed = 1 AND cancelled = 0 AND MONTH = ? AND YEAR = ?", i + 1, self.year)[0]["COUNT(*)"]
            self.column2 = db.execute("SELECT SUM(amount) FROM payments WHERE method != 'Cesu' AND MONTH = ? AND YEAR = ?", i + 1, self.year)[0]["SUM(amount)"]
            self.column3 = db.execute("SELECT SUM(amount) FROM payments WHERE method = 'Cesu' AND MONTH = ? AND YEAR = ?", i + 1, self.year)[0]["SUM(amount)"]
            self.column4 = db.execute("SELECT SUM(amount) FROM payments WHERE MONTH = ? AND YEAR = ?", i + 1, self.year)[0]["SUM(amount)"]
            if self.column2 == None:
                self.column2 = 0
            if self.column3 == None:
                self.column3 = 0
            if self.column4 == None:
                self.column4 = 0
            # Add to the totals
            self.row12column1 += self.column1
            self.row12column2 += self.column2
            self.row12column3 += self.column3
            self.row12column4 += self.column4
            # Put into the table
            items = [QTableWidgetItem(str(self.column1)), QTableWidgetItem(str(self.column2)), QTableWidgetItem(str(self.column3)), QTableWidgetItem(str(self.column4))]
            for x in range(len(items)):
                items[x].setTextAlignment(Qt.AlignCenter)
                self.monthlySummary.setItem(i, x + 1, items[x])

            # Fill in the data for the previous years (up to 3)
            col = 6
            for j in range(1, 4, 1):
                self.columna = db.execute("SELECT COUNT(*) FROM bookings WHERE completed = 1 AND cancelled = 0 AND MONTH = ? AND YEAR = ?", i + 1, self.year - j)[0]["COUNT(*)"]
                self.columnb = db.execute("SELECT SUM(amount) FROM payments WHERE MONTH = ? AND YEAR = ?", i + 1, self.year - j)[0]["SUM(amount)"]
                if self.columnb == None:
                    self.columnb = 0
                itemA = QTableWidgetItem(str(self.columna))
                itemA.setTextAlignment(Qt.AlignCenter)
                itemB = QTableWidgetItem(str(self.columnb))
                itemB.setTextAlignment(Qt.AlignCenter)
                self.monthlySummary.setItem(i, col, itemA)
                self.monthlySummary.setItem(i, col + 1, itemB)
                # Add to total
                if col == 6:
                    self.row12column6 += self.columna
                    self.row12column7 += self.columnb
                elif col == 9:
                    self.row12column9 += self.columna
                    self.row12column10 += self.columnb
                else:
                    self.row12column12 += self.columna
                    self.row12column13 += self.columnb
                col += 3    
        
        # Fill in the totals row
        totalItems = [QTableWidgetItem(str(self.row12column1)), QTableWidgetItem(str(self.row12column2)), QTableWidgetItem(str(self.row12column3)), QTableWidgetItem(str(self.row12column4)), "", QTableWidgetItem(str(self.row12column6)), QTableWidgetItem(str(self.row12column7)), "", QTableWidgetItem(str(self.row12column9)), QTableWidgetItem(str(self.row12column10)), "", QTableWidgetItem(str(self.row12column12)), QTableWidgetItem(str(self.row12column13))]
        for i in range(len(totalItems)):
            if totalItems[i] != "":
                totalItems[i].setTextAlignment(Qt.AlignCenter)
                totalItems[i].setFont(self.boldFont())
                self.monthlySummary.setItem(12, i + 1, totalItems[i])

    def populateAmountDueTable(self):
        # Block the signals to stop other functions from being activated
        self.paymentDetailTable.blockSignals(True)

        totalNumStudents = db.execute("SELECT name FROM students WHERE active = 1 ORDER BY name")
        self.paymentDetailTable.setRowCount(len(totalNumStudents) + 1)
        for i in range(len(totalNumStudents)):
            self.paymentDetailTable.setItem(i, 0, QTableWidgetItem(totalNumStudents[i]["name"]))
            dueAmount = db.execute("SELECT amountDue FROM students WHERE name = ?", totalNumStudents[i]["name"])[0]["amountDue"]
            item = QTableWidgetItem(str(dueAmount))
            item.setTextAlignment(Qt.AlignCenter)
            self.paymentDetailTable.setItem(i, 1, item)
            self.paymentDetailTable.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        
        # Add a total line
        tItem0 = QTableWidgetItem("TOTAL")
        tItem0.setFont(self.boldFont())
        self.paymentDetailTable.setItem(len(totalNumStudents), 0, tItem0)
        dueAmount = db.execute("SELECT SUM(amountDue) FROM students")[0]["SUM(amountDue)"]
        tItem = QTableWidgetItem(str(dueAmount))
        tItem.setTextAlignment(Qt.AlignCenter)
        tItem.setFont(self.boldFont())
        self.paymentDetailTable.setItem(len(totalNumStudents), 1, tItem)
        self.paymentDetailTable.blockSignals(False)

    def setAmount(self):
        if self.studentPlaceholder2.currentText() != "":
            amount = float(db.execute("SELECT pricePerStudent FROM students WHERE name = ?", self.studentPlaceholder2.currentText())[0]["pricePerStudent"]) * float(db.execute("SELECT group_size FROM students WHERE name = ?", self.studentPlaceholder2.currentText())[0]["group_size"])
            self.amount.setValue(amount)

    def addReduction(self):
        if self.reductionResponse.isChecked():
            self.toDeduct = QLineEdit()
            self.toDeduct.setPlaceholderText("How much are you deducting (EUR)")
            self.toDeduct.setFixedWidth(350)
            self.newPayment.insertRow(self.newPayment.rowCount() - 1, "", self.toDeduct)
        elif self.reductionResponse.isChecked() == False and self.newPayment.rowCount() == 8:
            self.newPayment.removeRow(self.newPayment.rowCount() - 2)

    def submitNewPayment(self):
        # Check all the data is provded
        if self.studentPlaceholder2.currentIndex() == 0:
            self.missingData(self.studentPlaceholder2)
        elif float(self.amount.text()) == 0:
            self.missingData(self.amount)
        elif self.paymentMethods.currentText() == "": 
            self.missingData(self.paymentMethods)
        else:
            # Apply the reduction if required
            reduction = 0
            if self.newPayment.rowCount() == 8:
                reduction = float(self.toDeduct.text())

            # Delete from the money owed by student and add to total amount paid by student
            db.execute("UPDATE students SET amountDue = amountDue - ? - ?, amountPaid = amountPaid + ? WHERE name = ?", float(self.amount.text()), reduction, float(self.amount.text()), self.studentPlaceholder2.currentText())
                        
            # Add to the payments database
            studentId = db.execute("SELECT id FROM students WHERE name = ?", self.studentPlaceholder2.currentText())[0]["id"]
            d = self.paymentDate.text().split("/")
            month = d[1]
            year = d[2]
            # Make sure the csv file isn't open
            try: 
                with open ("Database/Payments.csv", "a") as payments:
                    db.execute("INSERT INTO payments (studentId, date, month, year, amount, method) VALUES (?, ?, ?, ?, ?, ?)", 
                        studentId, self.paymentDate.text(), month, year, float(self.amount.text()), self.paymentMethods.currentText())
                    paymentId = db.execute("SELECT id FROM payments ORDER BY id DESC LIMIT 1")[0]["id"]
                    payments.writelines(str(paymentId) + ',' + self.studentPlaceholder2.currentText() + ',' + self.paymentDate.text() +  ',' + str(self.amount.text()) +  ',' + self.paymentMethods.currentText() +  ',' + str(reduction) + '\n')

                    # Update the money owed table
                    self.populateAmountDueTable()
            
                    # Update the monthly summary table
                    self.populateMonthlyPaymentTable()

                    # Update the graph
                    self.layout2.removeWidget(self.chartView)
                    self.layout2.addWidget(self.addGraph(), 1, 17, 10, 40)

                    # Clear the form
                    self.amount.setStyleSheet("background-color: ")
                    self.paymentMethods.setStyleSheet("background-color: ")
                    self.studentPlaceholder2.setStyleSheet("background-color: ")
                    self.amount.setValue(0)
                    self.paymentMethods.setCurrentText("")
                    self.studentPlaceholder2.setCurrentText("")
                    self.reductionResponse.setChecked(False)
                    self.addReduction()
                    
            # What to do if the file is open
            except PermissionError:
                self.fileOpen()

    def saveAmountChanged(self, row):
        name = self.paymentDetailTable.item(row, 0).text()
        amount = float(self.paymentDetailTable.item(row, 1).text())
        # Update the database
        db.execute("UPDATE students SET amountDue = ? WHERE name = ?", amount, name)
        self.populateAmountDueTable()



    # Actions for TAB 3
    def contactDetailsForm(self, obj):
        labela = QLabel("Address")
        address = QLineEdit()
        obj.addRow(labela, address)
        labelb = QLabel("Phone number")
        phone = QLineEdit()
        obj.addRow(labelb, phone)
        labelc = QLabel("Email")
        email = QLineEdit()
        obj.addRow(labelc, email)
        labeld = QLabel("Group size")
        groupSize = QLineEdit()
        obj.addRow(labeld, groupSize)
        labele = QLabel("Ages")
        studentAges = QLineEdit()
        obj.addRow(labele, studentAges)
        labelf = QLabel("Hobbies")
        hobbies = QLineEdit()
        obj.addRow(labelf, hobbies)
        labelg = QLabel("Price per student")
        pricePerStudent = QLineEdit()
        obj.addRow(labelg, pricePerStudent)

    def showStudentData(self, name):
        # Close the previous student's window if required
        self.contactDetailWindow.close()

        if name != "":
            # Add contact details
            values = list(db.execute("SELECT address, phone, email, group_size, age, hobbies, pricePerStudent from students WHERE name = ?", name)[0].values())
            for i in range(len(values)):
                self.contactDetails.itemAt(i, 1).widget().setText(str(values[i]))
            
            # 'deactivate' or 'reactivate' student button
            if db.execute("SELECT active FROM students WHERE name = ?", self.studentPlaceholder3.currentText())[0]["active"] == 1:
                self.studentStatus.setText("Deactivate student")
            else:
                self.studentStatus.setText("Reactivate student")

            # Set Pushbuttons to visible
            self.changeDetails.setVisible(True)
            self.studentStatus.setVisible(True)
                
            # Add financial data
            self.lessonQuantityTable()

            # Add knowledge data
            self.studentKnowledge
        
        else:
            # clear data
            for i in range(7):
                self.contactDetails.itemAt(i, 1).widget().setText("")
            self.lessonQuantityTable()
            # Hide the buttons
            self.changeDetails.setVisible(False)
            self.studentStatus.setVisible(False)

    def lessonQuantityTable(self):
        if self.studentPlaceholder3.currentIndex() != 0:
            student = self.studentPlaceholder3.currentText()
            periodmonth = self.monthChoice.currentText()
            periodYear = self.yearChoice.currentText()
            period = QTableWidgetItem(periodmonth + " " + periodYear)
            period.setFont(self.boldFont())
            self.studentData.setItem(0, 0, period)
            # Get the needed data from the bookings and payment tables
            if periodmonth == "Total":
                values = [
                    db.execute("SELECT SUM(completed) FROM bookings WHERE YEAR = ? AND studentId IN (SELECT id FROM students WHERE name = ?)", periodYear, student)[0]["SUM(completed)"] or 0,
                    db.execute("SELECT SUM(cancelled) FROM bookings WHERE YEAR = ? AND studentId IN (SELECT id FROM students WHERE name = ?)", periodYear, student)[0]["SUM(cancelled)"] or 0,
                    db.execute("SELECT SUM(amount) FROM payments WHERE YEAR = ? AND studentId IN (SELECT id FROM students WHERE name = ?)", periodYear, student)[0]["SUM(amount)"] or 0
                ]
            else: 
                monthIndex = self.months.index(periodmonth) + 1
                values = [
                    db.execute("SELECT SUM(completed) FROM bookings WHERE YEAR = ? AND MONTH = ? AND studentId IN (SELECT id FROM students WHERE name = ?)", periodYear, monthIndex, student)[0]["SUM(completed)"] or 0,
                    db.execute("SELECT SUM(cancelled) FROM bookings WHERE YEAR = ? AND MONTH = ? AND studentId IN (SELECT id FROM students WHERE name = ?)", periodYear, monthIndex, student)[0]["SUM(cancelled)"] or 0,
                    db.execute("SELECT SUM(amount) FROM payments WHERE YEAR = ? AND MONTH = ? AND studentId IN (SELECT id FROM students WHERE name = ?)", periodYear, monthIndex, student)[0]["SUM(amount)"] or 0
                ]
            x = 1
            for value in values:
                self.studentData.setItem(0, x, QTableWidgetItem(str(value)))
                x += 1
        else: 
            for i in range(self.studentData.columnCount()):
                self.studentData.setItem(0, i, QTableWidgetItem(str("")))

    def updateContactDetails(self, name):
        # Set the title of the window to the craft name
        self.contactDetailWindow.setWindowTitle(name)

        # clear the layout 
        for i in reversed(range(self.contactDetailWindow.layout().rowCount())):
            self.contactDetailWindow.layout().removeRow(i)

        # Add new data to the form
        self.contactDetailsForm(self.contactDetailWindow.layout())
        values = list(db.execute("SELECT address, phone, email, group_size, age, hobbies, pricePerStudent from students WHERE name = ?", name)[0].values())
        for i in range(len(values)):
            self.contactDetailWindow.layout().itemAt(i, 1).widget().setText(str(values[i]))
        self.contactDetailWindow.layout().addWidget(self.submitButton())
        self.contactDetailWindow.layout().itemAt(7, 1).setAlignment(Qt.AlignRight)
        self.contactDetailWindow.layout().itemAt(7, 1).widget().clicked.connect(lambda: self.saveNewContactDetails(self.contactDetailWindow.layout(), name))

        # Show the new window
        self.contactDetailWindow.show()

    def saveNewContactDetails(self, obj, name):
        # Make sure the csv file is closed
        try:
            with open("Database/student list.csv"):
                values = []
                for i in range(obj.rowCount() - 1):
                    values.append(obj.itemAt(i, 1).widget().text())
                db.execute("UPDATE students SET address = ?, phone = ?, email = ?, group_size = ?, age = ?, hobbies = ?, pricePerStudent = ? WHERE name = ?", values[0], values[1], values[2], values[3], values[4], values[5], values[6], name)
                
                # Update the csv file
                data = db.execute("SELECT id, name, address, phone, email, group_size, age, hobbies, pricePerStudent, active FROM students")
                self.rewriteCSVFile("Database/student list.csv", data)

                # Update the visible contact details form
                self.showStudentData(name)

                # Cose the window
                self.contactDetailWindow.close()
        except PermissionError:
            self.fileOpen()

    def updateStudentStatus(self, btt, name):
        if btt.text() == "Deactivate student":
            db.execute("UPDATE students SET active = 0 WHERE name = ?", name)
        else:
            db.execute("UPDATE students SET active = 1 WHERE name = ?", name)

        # Update the 'Money owed' table
        self.populateAmountDueTable()
        # Update the comboboxes
        self.activeStudentList(self.studentPlaceholder1)
        self.activeStudentList(self.studentPlaceholder2)
        self.activeStudentList(self.studentPlaceholder3)



    # Actions for TAB 4
    def search(self, text):
        # Block the signals to stop other functions from being activated
        self.foundLessons.blockSignals(True)
        self.foundBooks.blockSignals(True)
        self.foundGames.blockSignals(True)
        self.foundCrafts.blockSignals(True)
        self.foundFlashcards.blockSignals(True)

        # Clear the tables if the full text is deleted
        if len(text) == 0:
            self.foundLessons.setRowCount(0)
            self.foundBooks.setRowCount(0)
            # Revert columns to stretch
            sc = [1, 2, 3, 5, 6, 7, 9]
            for c in sc:
                self.foundBooks.horizontalHeader().setSectionResizeMode(c, QHeaderView.Stretch) 
            self.foundGames.setRowCount(0)
            self.foundCrafts.setRowCount(0)
            self.foundFlashcards.setRowCount(0)

        else: 
            self.checkedbuttons = 0
            self.lesson = db.execute("SELECT * FROM lessons WHERE active = 1 and (title LIKE ? OR publisher LIKE ? OR TYPE LIKE ? OR topics LIKE ?) ORDER BY title",
                "%" + text + "%", "%" + text + "%", "%" + text + "%", "%" + text + "%")
            self.foundLessons.setRowCount(len(self.lesson))
            for i in range(len(self.lesson)):
                valueslist = list(self.lesson[i].values())
                for j in range(len(valueslist) - 3):
                    self.foundLessons.setItem(i, j, QTableWidgetItem(str(valueslist[j])))
                # Set the cells with hyperlinks
                f = QLabel(valueslist[len(valueslist) - 3])
                self.hyperlink(f)
                self.foundLessons.setCellWidget(i, self.foundLessons.columnCount() - 2, f)
                self.addCheckBox(self.foundLessons, i, self.foundLessons.columnCount() - 1, lambda: self.deleteButton(self.foundLessons))
            

            self.book = db.execute("SELECT * FROM books WHERE active = 1 and (title LIKE ? OR author LIKE ? OR collection LIKE ? OR publisher LIKE ? OR bookType LIKE ? OR subtype LIKE ? OR description LIKE ? OR topics LIKE ?) ORDER BY title", 
                "%" + text + "%", "%" + text + "%", "%" + text + "%", "%" + text + "%", "%" + text + "%", "%" + text + "%", "%" + text + "%", "%" + text + "%")
            self.foundBooks.setRowCount(len(self.book))
            for i in range(len(self.book)):
                valueslist = list(self.book[i].values())
                for j in range(len(valueslist) - 2):
                    self.foundBooks.setItem(i, j, QTableWidgetItem(str(valueslist[j])))
                self.addCheckBox(self.foundBooks, i, self.foundBooks.columnCount() - 1, lambda: self.deleteButton(self.foundBooks))
            

            self.game = db.execute("SELECT * FROM games WHERE active = 1 and (title LIKE ? OR publisher LIKE ? OR gameType LIKE ? OR description LIKE ? OR topics LIKE ? OR (numberPlayersMin <= ? AND numberPlayersMax >= ?)) ORDER BY title",
                "%" + text + "%", "%" + text + "%", "%" + text + "%", "%" + text + "%", "%" + text + "%", text, text)
            self.foundGames.setRowCount(len(self.game))
            for i in range(len(self.game)):
                valueslist = list(self.game[i].values())
                for j in range(len(valueslist) - 6):
                    self.foundGames.setItem(i, j, QTableWidgetItem(str(valueslist[j])))
                # Set the columns needing additional coding
                nberPlayers = str(self.game[i]["numberPlayersMin"]) + " - " + str(self.game[i]["numberPlayersMax"])
                age = str(self.game[i]["ageMin"]) + " - " + str(self.game[i]["ageMax"])
                self.foundGames.setItem(i, self.foundGames.columnCount() - 3, QTableWidgetItem(nberPlayers))
                self.foundGames.setItem(i, self.foundGames.columnCount() - 2, QTableWidgetItem(age))
                self.addCheckBox(self.foundGames, i, self.foundGames.columnCount() - 1, lambda: self.deleteButton(self.foundGames))


            self.craft = db.execute("SELECT * FROM crafts WHERE active = 1 and (title LIKE ? OR materials LIKE ?) ORDER BY title",
                "%" + text + "%", "%" + text + "%")
            self.foundCrafts.setRowCount(len(self.craft))
            for i in range(len(self.craft)):
                valueslist = list(self.craft[i].values())
                for j in range(len(valueslist) - 3):
                    self.foundCrafts.setItem(i, j, QTableWidgetItem(str(valueslist[j])))
                # Set the cells with hyperlinks
                im = QLabel(self.craft[i]["image"])
                self.hyperlink(im)
                self.foundCrafts.setCellWidget(i, self.foundCrafts.columnCount() - 3, im)
                instructions = QLabel(self.craft[i]["instructions"])
                self.hyperlink(instructions)
                self.foundCrafts.setCellWidget(i, self.foundCrafts.columnCount() - 2, instructions)
                self.addCheckBox(self.foundCrafts, i, self.foundCrafts.columnCount() - 1, lambda: self.deleteButton(self.foundCrafts))


            self.flashcard = db.execute("SELECT * FROM flashcards WHERE active = 1 and (title LIKE ? OR topics LIKE ?) ORDER BY title",
                "%" + text + "%", "%" + text + "%")
            self.foundFlashcards.setRowCount(len(self.flashcard))
            for i in range(len(self.flashcard)):
                self.foundFlashcards.setItem(i, 0, QTableWidgetItem(str(self.flashcard[i]["id"])))
                self.foundFlashcards.setItem(i, 1, QTableWidgetItem(self.flashcard[i]["title"]))
                self.addCheckBox(self.foundFlashcards, i, self.foundFlashcards.columnCount() - 1, lambda: self.deleteButton(self.foundFlashcards))

        # Reactivate the signals
        self.foundLessons.blockSignals(False)
        self.foundBooks.blockSignals(False)
        self.foundGames.blockSignals(False)
        self.foundCrafts.blockSignals(False)
        self.foundFlashcards.blockSignals(False)

    def deleteButton(self, obj):
        row = obj.currentRow()
        if obj.cellWidget(row, obj.columnCount() - 1).isChecked():
            self.checkedbuttons += 1
            if self.layout4.rowCount() != 7:
                b = QHBoxLayout()
                but = QPushButton("DELETE")
                but.setFixedWidth(200)
                b.addStretch()
                b.addWidget(but)
                b.addStretch()
                self.layout4.addRow(b)
                but.clicked.connect(self.deleteResources)
        else:
            self.checkedbuttons -= 1
            if self.checkedbuttons == 0:
                self.layout4.removeRow(6)

    def deleteResources(self):
        self.deletionConfirmed = "False"

        # Determine the list of all resources to be deleted
        lessonsToDelete = []
        for i in range (self.foundLessons.rowCount()):
            if self.foundLessons.cellWidget(i, self.foundLessons.columnCount() - 1).isChecked():
                lessonsToDelete.append([int(self.foundLessons.item(i, 0).text()), self.foundLessons.item(i, 1).text(), " - Lesson"])
        booksToDelete = []
        for i in range (self.foundBooks.rowCount()):
            if self.foundBooks.cellWidget(i, self.foundBooks.columnCount() - 1).isChecked():
                booksToDelete.append([int(self.foundBooks.item(i, 0).text()), self.foundBooks.item(i, 1).text(), " - Book"])
        gamesToDelete = []
        for i in range (self.foundGames.rowCount()):
            if self.foundGames.cellWidget(i, self.foundGames.columnCount() - 1).isChecked():
                gamesToDelete.append([int(self.foundGames.item(i, 0).text()), self.foundGames.item(i, 1).text(), " - Game"])
        craftsToDelete = []
        for i in range (self.foundCrafts.rowCount()):
            if self.foundCrafts.cellWidget(i, self.foundCrafts.columnCount() - 1).isChecked():
                craftsToDelete.append([int(self.foundCrafts.item(i, 0).text()), self.foundCrafts.item(i, 1).text(), " - Craft"])
        falshcToDelete = []
        for i in range (self.foundFlashcards.rowCount()):
            if self.foundFlashcards.cellWidget(i, self.foundFlashcards.columnCount() - 1).isChecked():
                falshcToDelete.append([int(self.foundFlashcards.item(i, 0).text()), self.foundFlashcards.item(i, 1).text(), " - Flashcard"])

        # popup box to confirm
        confirmationMessage = QMessageBox()
        confirmationMessage.setIcon(QMessageBox.Question)
        confirmationMessage.setText("Are you sure you want to delete the following:")
        detailstodisplay = []
        detailstodisplay += lessonsToDelete + booksToDelete + gamesToDelete + craftsToDelete + falshcToDelete
        dtd = ""
        for i in range(len(detailstodisplay)):
            dtd += str((i + 1)) + ". " + detailstodisplay[i][1] + detailstodisplay[i][2] + "\n"
        confirmationMessage.setDetailedText(dtd)
        confirmationMessage.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmationMessage.buttonClicked.connect(lambda: self.deletionOutcome(confirmationMessage.clickedButton()))
        confirmationMessage.exec_()

        # delete from the database
        if self.deletionConfirmed == "True":
            # Check the files aren't open before launching the functions
            try:
                with open("Database/Lessons.csv", "a"), open("Database/Books.csv", "a"), open("Database/Games.csv", "a"), open("Database/Arts & crafts.csv", "a"), open("Database/Flashcards.csv", "a"):
                    self.blockage = "no"

            # What to do if the files are open
            except PermissionError:
                self.blockage = "yes"
                self.fileOpen()

            if self.blockage == "no":
                for i in range(len(lessonsToDelete)):
                    db.execute("UPDATE lessons SET active = 0 WHERE id = ?", lessonsToDelete[i][0])
                data = db.execute("SELECT * FROM lessons")
                self.rewriteCSVFile("Database/Lessons.csv", data)

                for i in range(len(booksToDelete)):
                    db.execute("UPDATE books SET active = 0 WHERE id = ?", booksToDelete[i][0])
                data = db.execute("SELECT * FROM books")
                self.rewriteCSVFile("Database/Books.csv", data)

                for i in range(len(gamesToDelete)):
                    db.execute("UPDATE games SET active = 0 WHERE id = ?", gamesToDelete[i][0])
                data = db.execute("SELECT * FROM games")
                self.rewriteCSVFile("Database/Games.csv", data)
                
                for i in range(len(craftsToDelete)):
                    db.execute("UPDATE crafts SET active = 0 WHERE id = ?", craftsToDelete[i][0])
                data = db.execute("SELECT * FROM crafts")
                self.rewriteCSVFile("Database/Arts & crafts.csv", data)
                
                for i in range(len(falshcToDelete)):
                    db.execute("UPDATE flashcards SET active = 0 WHERE id = ?", falshcToDelete[i][0])    
                self.text.clear()
                data = db.execute("SELECT * FROM flashcards")
                self.rewriteCSVFile("Database/Flashcards.csv", data)
                
                # Update the comboboxes
                for i in range(self.bookingDetailTable.rowCount()):
                    self.lessonList(self.bookingDetailTable.cellWidget(i, 6))
                    self.bookList(self.bookingDetailTable.cellWidget(i, 7))
                    self.gameList(self.bookingDetailTable.cellWidget(i, 8))                
                    self.craftList(self.bookingDetailTable.cellWidget(i, 9))                

                # Remove the 'delete' button
                self.layout4.removeRow(6)

    def deletionOutcome(self, btn):
        if btn.text()[1:] == "Yes":
            self.deletionConfirmed = "True"

    def resourceChanged(self, obj, table, row, column, file):
        # Check the files aren't open before launching the functions
        try:
            with open(file, "a"):
                self.blockage = "no"

        # What to do if the files are open
        except PermissionError:
            # Tell the programme there is an issue
            self.blockage = "yes"
            # Open the dialogue box
            self.fileOpen()            

        if self.blockage == "no":
            rowId = obj.item(row, 0).text()
            titles = list(db.execute("SELECT * FROM ? LIMIT 1", table)[0].keys())
            if table == "games":
                for i in range(1, obj.columnCount() - 3, 1):
                    db.execute("UPDATE ? SET ? = ? WHERE id = ?", table, titles[i], obj.item(row, i).text(), rowId)
            else:
                for i in range(1, obj.columnCount() - 1, 1):
                    db.execute("UPDATE ? SET ? = ? WHERE id = ?", table, titles[i], obj.item(row, i).text(), rowId)
            # Update the csv file
            data = db.execute("SELECT * FROM ?", table)
            self.rewriteCSVFile(file, data)
        else:
            obj.blockSignals(True)
            # Revert the data back
            oldData = db.execute("SELECT * from ? WHERE id = ?", table, obj.item(row, 0).text())[0]
            dbTitle = list(oldData.keys())[column]
            obj.setItem(row, column, QTableWidgetItem(str(oldData[dbTitle])))
            obj.blockSignals(False)



    # Actions for TAB 5
    def addAges(self):
        self.layout5.removeRow(5)
        self.ages = QHBoxLayout()
        self.ageLabel = QLabel("Ages")
        for i in range(int(self.groupSize.text())):
            self.ages.addWidget(QSpinBox())
        self.layout5.insertRow(5, self.ageLabel, self.ages)

    def saveNewStudent(self):
        # Determine all the values
        name = self.newStudentName.text().title()
        address = self.newStudentAddress.text()
        phone = self.newStudentPhone.text()
        email = self.newStudentEmail.text()
        gSize = self.groupSize.text()
        hobbies = self.hobbies.text()
        ages = ""
        for i in range(self.ages.count()):
            if ages == "":
                ages = (self.ages.itemAt(i).widget().text())
            else:
                ages += ", " + (self.ages.itemAt(i).widget().text())          
        amountPerStudent = self.amountPerStudent.text()

        # Inform the user in case there is missing essential data
        if name == "":
            self.missingData(self.newStudentName)

        # If all the require data is entered, fill in the database
        else:
            # Revert the colours back to normal
            self.newStudentName.setStyleSheet("background-color: ")
            
            # Add to the database
            # Make sure the csv file isn't open
            try:
                with open ("Database/student list.csv", "a") as students:
                    db.execute("INSERT INTO students(name, address, phone, email, group_size, age, hobbies, pricePerStudent, active, nberLessons, nberCancelled, amountPaid, amountDue) VALUES(?, ?, ?, ?, ?, ?, ?, ?, 1, 0, 0, 0, 0)",
                        name, address, phone, email, gSize, ages, hobbies, amountPerStudent)
                    idnum = db.execute("SELECT id FROM students ORDER BY id DESC LIMIT 1")[0]["id"]
                    students.writelines(str(idnum) + ',' + name + ',' + address + ',' + str(phone) + ',' + email + ',' + str(gSize) + ',' + str(ages) + ',"' + hobbies + '",' + str(amountPerStudent) + ',1\n')
                
                    # Add to the money owed table
                    self.populateAmountDueTable()
                    
                    # Add to the student list combobox
                    self.activeStudentList(self.studentPlaceholder1)
                    self.activeStudentList(self.studentPlaceholder2)
                    self.activeStudentList(self.studentPlaceholder3)

                    # and clear the form
                    self.newStudentName.clear()
                    self.newStudentAddress.clear()
                    self.newStudentPhone.clear()
                    self.newStudentEmail.clear()
                    self.groupSize.setValue(1)
                    self.ages.itemAt(0).widget().setValue(0)
                    
                    self.hobbies.clear()
                    self.amountPerStudent.setValue(20)
            
            # What to do if the file is open
            except PermissionError:
                self.fileOpen()



    # Actions for TAB 6
    def somethingClicked(self):
        # Delete the content of the page if already data other than the 1st row
        if self.layout6.rowCount() > 1:
            for i in reversed(range(1, self.layout6.rowCount(), 1)):
                self.layout6.removeRow(i)
    
        # Add if lesson: 
        if self.lessonBox.isChecked():
            self.lessonLabel1 = QLabel("Title")
            self.lessonTitle = QLineEdit()
            self.lessonLabel2 = QLabel("Provider")
            self.lessonProvider = QLineEdit()
            self.lessonLabel4 = QLabel("Activities")
            self.lessonactivities = QLineEdit()
            self.lessonLabel5 = QLabel("File location")
            FileRow = QHBoxLayout()
            self.lessonFile = QLineEdit()
            FileRow.addWidget(self.lessonFile)
            searchFile = QPushButton("Search File")
            searchFile.setFixedWidth(150)
            searchFile.clicked.connect(lambda: self.searchFiles(searchFile.text(), self.lessonFile))
            FileRow.addWidget(searchFile)
            self.lessonLabel6 = QLabel("Subject")
            self.subject = QHBoxLayout()
            with open("Database/LessonTypes.txt", "r") as lessons:
                for row in lessons:
                    self.subject.addWidget(QCheckBox(row.strip('\n')))
            self.subject.addWidget(self.otherField())
            self.subject.addStretch()

            self.layout6.addRow(self.lessonLabel1, self.lessonTitle)
            self.layout6.addRow(self.lessonLabel2, self.lessonProvider)
            self.layout6.addRow(self.lessonLabel4, self.lessonactivities)
            self.layout6.addRow(self.lessonLabel5, FileRow)
            self.layout6.addRow(self.lessonLabel6, self.subject) 
            self.addTopicTable()
            self.addOtherRow()

        # Add if book
        elif self.bookBox.isChecked():
            self.bookDetailsLabel1 = QLabel("Title")
            self.bookTitle = QLineEdit()
            self.layout6.addRow(self.bookDetailsLabel1, self.bookTitle)
            self.bookDetailsLabel2 = QLabel("Author")
            self.bookAuthor = QLineEdit()
            self.layout6.addRow(self.bookDetailsLabel2, self.bookAuthor)
            self.bookDetailsLabel3 = QLabel("Collection")
            self.bookCollection = QLineEdit()
            self.layout6.addRow(self.bookDetailsLabel3, self.bookCollection)
            self.bookDetailsLabel4 = QLabel("Book number")
            self.bookNumber = QLineEdit()
            self.layout6.addRow(self.bookDetailsLabel4, self.bookNumber)
            self.bookDetailsLabel5 = QLabel("Publisher")
            self.bookPublisher = QLineEdit()
            self.layout6.addRow(self.bookDetailsLabel5, self.bookPublisher)
            
            self.bookDetailsLabel6 = QLabel("Type of book")
            self.bookType = QHBoxLayout()
            with open ("Database/BookTypes.txt", "r") as typeList6:
                for row in typeList6:
                    self.bookType.addWidget(QCheckBox(row.strip("\n")))
            self.bookType.addWidget(self.otherField())
            self.bookType.addStretch()
            self.layout6.addRow(self.bookDetailsLabel6, self.bookType)

            self.bookDetailsLabel7 = QLabel("Subtype of book")
            self.subType = QHBoxLayout()
            with open ("Database/BookSubcategories.txt", "r") as subtypeList6:
                for row in subtypeList6:
                    self.subType.addWidget(QCheckBox(row.strip("\n")))
            self.subType.addWidget(self.otherField())
            self.subType.addStretch()
            self.layout6.addRow(self.bookDetailsLabel7, self.subType)

            self.bookDetailsLabel8 = QLabel("Level")
            self.bookLevel = QHBoxLayout()
            with open ("Database/Levels.txt", "r") as levels:
                for row in levels:
                    self.bookLevel.addWidget(QCheckBox(row.strip("\n")))
            self.bookLevel.addStretch()
            self.layout6.addRow(self.bookDetailsLabel8, self.bookLevel)

            self.bookDetailsLabel9 = QLabel("Description")
            self.bookDescription = QLineEdit()
            self.layout6.addRow(self.bookDetailsLabel9, self.bookDescription)
            
            self.addTopicTable()
            self.addOtherRow()
            
        # Add if game
        elif self.gameBox.isChecked():
            self.gameLabel1 = QLabel("Title")
            self.gameTitle = QLineEdit()
            self.gameLabel2 = QLabel("Publisher")
            self.gamePublisher = QLineEdit()
            self.gameLabelColour = QLabel("Colour")
            self.gameColour = QLineEdit()
            self.gameLabel3 = QLabel("Type of game")
            self.gameType = QHBoxLayout()
            with open("Database/GameTypes.txt", "r") as gt:
                for row in gt:
                    self.gameType.addWidget(QCheckBox(row.strip('\n')))
            self.gameType.addWidget(self.otherField())
            self.gameType.addStretch()
            self.gameLabel4 = QLabel("Description")
            self.gameDescription = QLineEdit()
            self.gameLabel5 = QLabel("N° of players")
            self.numberPlayers = QHBoxLayout()
            self.numberPlayers.addWidget(QCheckBox("2"))
            self.numberPlayers.addWidget(QCheckBox("3"))
            self.numberPlayers.addWidget(QCheckBox("4"))
            self.numberPlayers.addWidget(QCheckBox("5"))
            self.numberPlayers.addWidget(QCheckBox("6"))
            self.numberPlayers.addWidget(QCheckBox("7"))
            self.numberPlayers.addWidget(QCheckBox("8+"))
            self.numberPlayers.addStretch()
            self.gameLabel6 = QLabel("Age")
            self.age = QHBoxLayout()
            self.age.addWidget(QCheckBox("3"))
            self.age.addWidget(QCheckBox("4"))
            self.age.addWidget(QCheckBox("5"))
            self.age.addWidget(QCheckBox("6"))
            self.age.addWidget(QCheckBox("7"))
            self.age.addWidget(QCheckBox("8"))
            self.age.addWidget(QCheckBox("9"))
            self.age.addWidget(QCheckBox("10"))
            self.age.addWidget(QCheckBox("10+"))
            self.age.addStretch()    
            self.gameLabel7 = QLabel("Duration (min)")
            self.gameDuration = QSpinBox()

            self.layout6.addRow(self.gameLabel1, self.gameTitle)
            self.layout6.addRow(self.gameLabel2, self.gamePublisher)
            self.layout6.addRow(self.gameLabelColour, self.gameColour)
            self.layout6.addRow(self.gameLabel3, self.gameType)
            self.layout6.addRow(self.gameLabel4, self.gameDescription)
            self.layout6.addRow(self.gameLabel5, self.numberPlayers)         
            self.layout6.addRow(self.gameLabel6, self.age)
            self.layout6.addRow(self.gameLabel7, self.gameDuration)
            
            self.addTopicTable()
            self.addOtherRow()

        # Add if craft
        elif self.craftBox.isChecked():
            self.craftLabel1 = QLabel("Title")
            self.whatMaking = QLineEdit()
            self.whatMaking.setFixedHeight(30)
            self.craftLabel2 = QLabel("Materials")
            self.materialsNeeded = QLineEdit()
            self.materialsNeeded.setFixedHeight(30)
            self.craftLabel3 = QLabel("Image")
            imageRow = QHBoxLayout()
            self.craftImage = QLineEdit()
            imageRow.addWidget(self.craftImage)
            searchImagefile = QPushButton("Search image")
            searchImagefile.setFixedWidth(150)
            searchImagefile.clicked.connect(lambda: self.searchFiles(searchImagefile.text(), self.craftImage))
            imageRow.addWidget(searchImagefile)
            self.craftLabel4 = QLabel("Document")
            instructionRow = QHBoxLayout()
            self.craftInstructions = QLineEdit()
            instructionRow.addWidget(self.craftInstructions)
            searchDocfile = QPushButton("Search document")
            searchDocfile.setFixedWidth(150)
            searchDocfile.clicked.connect(lambda: self.searchFiles(searchDocfile.text(), self.craftInstructions))
            instructionRow.addWidget(searchDocfile)
            self.craftLabel5 = QLabel("Duration (min)")
            self.craftDuration = QSpinBox()
            self.layout6.addRow(self.craftLabel1, self.whatMaking)
            self.layout6.addRow(self.craftLabel2, self.materialsNeeded)
            self.layout6.addRow(self.craftLabel3, imageRow)
            self.layout6.addRow(self.craftLabel4, instructionRow)
            self.layout6.addRow(self.craftLabel5, self.craftDuration)
        
        # Add if flashcard
        elif self.flashcardBox.isChecked():
            self.flashcardDetailsLabel1 = QLabel("Title")
            self.flashcardTitle = QLineEdit()
            self.layout6.addRow(self.flashcardDetailsLabel1, self.flashcardTitle)
            self.addTopicTable()
            self.addOtherRow()
           
        # Add the submit button
        self.confirmation_button6 = self.submitButton()
        self.confirmation_button6.clicked.connect(self.newResourcesSubmitted)
        self.layout6.addRow(self.confirmation_button6)

    def addTopicTable(self):
        topicLabel = QLabel("Topics")
        self.layout6.addRow(topicLabel, self.topicList())

    def topicList(self):
        # Set the table
        self.listOfTopics = QTableWidget()
        self.setScrollBar(self.listOfTopics)
        self.listOfTopics.setAlternatingRowColors(True)

        # Get the data to include in the table
        self.allTopics = db.execute("SELECT * FROM topics ORDER BY topic") + [{'id': '', 'topic': 'OTHER'}]
        
        # Set up number of columns based on full screen view
        geo = str(self.resolution)[19:]
        dimentions = geo.strip(')').split(', ')
        self.xSize = int(dimentions[2])
        colAsize = 210
        self.colBsize = 40
        x = round((self.xSize - 120) / (colAsize + self.colBsize))      
        self.listOfTopics.setColumnCount(x*3)
        # Hide the 'Id' columns
        for i in range(0, self.listOfTopics.columnCount(), 3):
            self.listOfTopics.setColumnHidden(i, True)

        # fill the table based on number of columns
        self.nberPerCol = math.ceil(len(self.allTopics) / x)
        self.listOfTopics.setRowCount(self.nberPerCol)
        self.fillTopicsTable(0, self.nberPerCol, 0)

        # What to do if cell content is changed manually
        self.listOfTopics.itemChanged.connect(lambda: self.saveTopicChanged(self.listOfTopics.currentRow(), self.listOfTopics.currentColumn()))

        # return the table 
        return(self.listOfTopics)

    def fillTopicsTable(self, start, end, currentCol):
        # Set base argument
        if end != len(self.allTopics):
            # Set recursion into place
            if (end + self.nberPerCol) > len(self.allTopics):
                self.fillTopicsTable(end, len(self.allTopics), currentCol + 3)
            else:
                self.fillTopicsTable(end, end + self.nberPerCol, currentCol + 3)

        # Set the column name
        if len(self.allTopics[start]["topic"]) == 1:
            ca = self.allTopics[start]["topic"][0]
        else:
            ca = self.allTopics[start]["topic"][0] + self.allTopics[start]["topic"][1]

        if self.allTopics[end - 1]["topic"] == "OTHER":
            cb = "OTHER"
        elif len(self.allTopics[end - 1]["topic"]) == 1:
            cb = self.allTopics[end - 1]["topic"][0]
        else:
            cb = self.allTopics[end - 1]["topic"][0] + self.allTopics[end - 1]["topic"][1]

        self.listOfTopics.setHorizontalHeaderItem(currentCol, QTableWidgetItem("Id"))
        self.listOfTopics.setHorizontalHeaderItem(currentCol + 1, QTableWidgetItem(ca + " - " + cb))
        self.listOfTopics.setHorizontalHeaderItem(currentCol + 2, QTableWidgetItem(""))


        # Fill in the content
        for i in range(end - start): 
            self.listOfTopics.setItem(i, currentCol, QTableWidgetItem(str(self.allTopics[start]["id"])))
            self.listOfTopics.setItem(i, currentCol + 1, QTableWidgetItem(self.allTopics[start]["topic"]))
            self.addCheckBox(self.listOfTopics, i, currentCol + 2, self.showOtherRow)
            start += 1

        # Set cell sizes
        for i in range(1, self.listOfTopics.columnCount(), 3):
            self.listOfTopics.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        for i in range(2, self.listOfTopics.columnCount(), 3):
            self.listOfTopics.setColumnWidth(i, self.colBsize)
        for i in range(self.listOfTopics.rowCount()):
            self.listOfTopics.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

    def saveTopicChanged(self, row, column):
        db.execute("UPDATE topics SET topic = ? WHERE id = ?", self.listOfTopics.item(row, column).text(), self.listOfTopics.item(row, column - 1).text())

    def addOtherRow(self):
        self.w = QWidget()
        l = QHBoxLayout()
        label = QLabel("Other topics")
        self.additionalTopics = QLineEdit()
        self.additionalTopics.setPlaceholderText("Write a list seperated by ', '")
        l.addWidget(label)
        l.addWidget(self.additionalTopics)
        self.w.setLayout(l)
        self.layout6.addWidget(self.w)
        self.w.hide()

    def showOtherRow(self):
        # Get the row and column of the 'Other' checkbox
        lastcol = self.listOfTopics.columnCount() - 1
        row = self.listOfTopics.findItems("OTHER", Qt.MatchExactly)[0].row()
        
        # If it is clicked, add row to screen to be able to add additional topics
        if self.listOfTopics.cellWidget(row, lastcol).isChecked():
            self.w.show()

        # If is is unclicked and the additional row had been added, delete that row
        elif self.listOfTopics.cellWidget(row, lastcol).isChecked() == False:
            self.additionalTopics.clear()
            self.w.hide()         

    def newResourcesSubmitted(self):
        # Set empty values
        resourceId = ""
        ref = ""
        topicString = ""

        # Complete the other tables as required 
        # Add if lesson: 
        if self.lessonBox.isChecked():
            # Make sure all the required info is included
            if self.lessonTitle.text() == "":
                self.missingData(self.lessonTitle)

            else:
                # Revert colours where required
                self.lessonTitle.setStyleSheet("background-color: ")

                # Put the topics into a string
                topicString = self.listOfChosenTopics()

                # Set up the string of types
                subject = ""
                for i in range(self.subject.count() - 1):
                    if i == self.subject.count() - 2 or self.subject.itemAt(i).widget().isChecked():
                        if subject == "":
                            subject += self.subject.itemAt(i).widget().text()
                        elif self.subject.itemAt(i).widget().text() != "":
                            subject += ", " + self.subject.itemAt(i).widget().text()
                    if i in range(self.subject.count() - 2):
                        self.subject.itemAt(i).widget().setChecked(False)
                # Add the value of the 'other' field to the string to be added into the database
                if self.subject.itemAt(self.subject.count() - 2).widget().text() != "":
                    # Add this new type to the txt file
                    self.addToTextFile(self.subject.itemAt(self.subject.count() - 2).widget().text(), "Database/LessonTypes.txt")
                    # Clear the field
                    self.subject.itemAt(self.subject.count() - 2).widget().clear()

                
                # Add to the database and csv file
                # Make sure the csv file isn't open
                try:
                    with open ("Database/Lessons.csv", "a") as lessons:
                        db.execute("INSERT INTO lessons (title, publisher, type, activities, file, topics, active) VALUES (?, ?, ?, ?, ?, ?, 1)",
                            self.lessonTitle.text().title(), self.lessonProvider.text().title(), subject, self.lessonactivities.text(), self.lessonFile.text(), topicString)
                        resourceId = db.execute("SELECT id from lessons ORDER BY id DESC LIMIT 1")[0]["id"]
                        lessons.writelines(str(resourceId) + ',' + self.lessonTitle.text().title() + ',' + self.lessonProvider.text().title() + ',"' + subject + '","' + self.lessonactivities.text() + '","' + self.lessonFile.text() + '","' + topicString + '",1\n')

                        # Update the Combobox
                        for i in range(self.bookingDetailTable.rowCount()):
                            self.lessonList(self.bookingDetailTable.cellWidget(i, 6))

                        # Clear all the QLineEdits
                        self.lessonTitle.clear()
                        self.lessonProvider.clear()
                        self.lessonactivities.clear()
                        self.lessonFile.clear()

                        # Get reference needs to link new resource and topics
                        ref = "lessons"
                            
                # What to do if the file is open
                except PermissionError:
                    self.fileOpen()

        # Add if book
        elif self.bookBox.isChecked():
            # Make sure all the required info is included
            if self.bookTitle.text() == "":
                self.missingData(self.bookTitle)

            else:
                # Revert colours where required
                self.bookTitle.setStyleSheet("background-color: ")

                # Put the topics into a string
                topicString = self.listOfChosenTopics()

                # Set up the string of types
                bookType = ""
                for i in range(self.bookType.count() - 1):
                    if i == self.bookType.count() - 2 or self.bookType.itemAt(i).widget().isChecked():
                        if bookType == "":
                            bookType += self.bookType.itemAt(i).widget().text()
                        elif self.bookType.itemAt(i).widget().text() != "":
                            bookType += ", " + self.bookType.itemAt(i).widget().text()
                    if i in range(self.bookType.count() - 2):
                        self.bookType.itemAt(i).widget().setChecked(False)
                # Add the value of the 'other' field to the string to be added into the database
                if self.bookType.itemAt(self.bookType.count() - 2).widget().text() != "":
                    # Add this new type to the txt file
                    self.addToTextFile(self.bookType.itemAt(self.bookType.count() - 2).widget().text(), "Database/BookTypes.txt")
                    # Clear the field
                    self.bookType.itemAt(self.bookType.count() - 2).widget().clear()

                # Set up the string of subtypes
                subType = ""
                for i in range(self.subType.count() - 1):
                    if i == self.subType.count() - 2 or self.subType.itemAt(i).widget().isChecked():
                        if subType == "":
                            subType += self.subType.itemAt(i).widget().text()
                        elif self.subType.itemAt(i).widget().text() != "":
                            subType += ", " + self.subType.itemAt(i).widget().text()
                    if i in range(self.subType.count() - 2):
                        self.subType.itemAt(i).widget().setChecked(False)    
                # Add the value of the 'other' field to the string to be added into the database
                if self.subType.itemAt(self.subType.count() - 2).widget().text() != "":
                    # Add this new type to the txt file
                    self.addToTextFile(self.subType.itemAt(self.subType.count() - 2).widget().text(), "Database/BookSubcategories.txt")
                    # Clear the field
                    self.subType.itemAt(self.subType.count() - 2).widget().clear()

                # Determine the level
                bookLevel = ""
                for i in range(self.bookLevel.count() - 1):
                    if self.bookLevel.itemAt(i).widget().isChecked():
                        bookLevel += self.bookLevel.itemAt(i).widget().text()
                        self.bookLevel.itemAt(i).widget().setChecked(False)
                
                # Add to the database and csv file
                # Make sure the csv file isn't open
                try:
                    with open ("Database/Books.csv", "a") as books:
                        db.execute("INSERT INTO books (title, author, collection, booknber, publisher, bookType, subtype, level, description, topics, active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
                            self.bookTitle.text().title(), self.bookAuthor.text().title(), self.bookCollection.text().title(), self.bookNumber.text(), self.bookPublisher.text(), bookType, subType, bookLevel, self.bookDescription.text(), topicString)
                        resourceId = db.execute("SELECT id FROM books ORDER BY id DESC LIMIT 1")[0]["id"]
                        books.writelines(str(resourceId) + ',' + self.bookTitle.text().title() + ',' + self.bookAuthor.text().title() + ',' + self.bookCollection.text().title() + ',' + self.bookNumber.text() + ',' + self.bookPublisher.text().title() + ',"' + bookType + '","' + subType + '",' + bookLevel + ',' + self.bookDescription.text() + ',"' + topicString + '",1\n')

                        # Update the Combobox
                        for i in range(self.bookingDetailTable.rowCount()):
                            self.bookList(self.bookingDetailTable.cellWidget(i, 7))

                        # Clear all the QLineEdits
                        self.bookTitle.clear()
                        self.bookAuthor.clear()
                        self.bookCollection.clear()
                        self.bookNumber.clear()
                        self.bookPublisher.clear()
                        self.bookDescription.clear()

                        # Get values needs to link new resource and topics
                        ref = "books"
                            
                # What to do if the file is open
                except PermissionError:
                    self.fileOpen()

        # Add if game
        elif self.gameBox.isChecked():
            # Make sure all the required info is included
            if self.gameTitle.text() == "":
                self.missingData(self.gameTitle)

            else:
                # Revert colours where required
                self.gameTitle.setStyleSheet("background-color: ")

                # Put the topics into a string
                topicString = self.listOfChosenTopics()
                
                # Set up the string of types
                gameType = ""
                for i in range(self.gameType.count() - 1):
                    if i == self.gameType.count() - 2 or self.gameType.itemAt(i).widget().isChecked():
                        if gameType == "":
                            gameType += self.gameType.itemAt(i).widget().text()
                        elif self.gameType.itemAt(i).widget().text() != "":
                            gameType += ", " + self.gameType.itemAt(i).widget().text()
                    if i in range(self.gameType.count() - 2):
                        self.gameType.itemAt(i).widget().setChecked(False)
                # Add the value of the 'other' field to the string to be added into the database
                if self.gameType.itemAt(self.gameType.count() - 2).widget().text() != "":
                    # Add this new type to the txt file
                    self.addToTextFile(self.gameType.itemAt(self.gameType.count() - 2).widget().text(), "Database/GameTypes.txt")
                    # Clear the field
                    self.gameType.itemAt(self.gameType.count() - 2).widget().clear()

                # Set up the string of nber players
                nberPlayers = []
                for i in range(self.numberPlayers.count() - 1):
                    if self.numberPlayers.itemAt(i).widget().isChecked():
                        nberPlayers.append(self.numberPlayers.itemAt(i).widget().text())
                        self.numberPlayers.itemAt(i).widget().setChecked(False)    
                if len(nberPlayers) != 0:
                    nbplayersmin = nberPlayers[0]
                    nbplayersmax = nberPlayers[-1]
                else: 
                    nbplayersmin = ""
                    nbplayersmax = ""

                # Determine the age
                ages = []
                for i in range(self.age.count() - 1):
                    if self.age.itemAt(i).widget().isChecked():
                        ages.append(self.age.itemAt(i).widget().text())
                        self.age.itemAt(i).widget().setChecked(False)
                if len(ages) != 0:
                    agemin = ages[0]
                    agemax = ages[-1]
                else:
                    agemin = ""
                    agemax = ""
                
                # Add to the database and csv file
                # Make sure the csv file isn't open
                try:
                    with open ("Database/Games.csv", "a") as games:
                        db.execute("INSERT INTO games (title, publisher, colour, gameType, description, duration, numberPlayersMin, numberPlayersMax, ageMin, ageMax, topics, active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
                            self.gameTitle.text().title(), self.gamePublisher.text().title(), self.gameColour.text(), gameType, self.gameDescription.text(), self.gameDuration.text(), nbplayersmin, nbplayersmax, agemin, agemax, topicString)
                        resourceId = db.execute("SELECT id FROM games ORDER BY id DESC LIMIT 1")[0]["id"]
                        games.writelines(str(resourceId) + ',' + self.gameTitle.text().title() + ',' + self.gamePublisher.text().title() + ',' + self.gameColour.text() + ',"' + gameType + '",' + self.gameDescription.text() + ',' + self.gameDuration.text() + ',' + nbplayersmin + ',' + nbplayersmax + ',' + agemin + ',' + agemax + ',"' + topicString + '",1\n')

                        # Update the Combobox
                        for i in range(self.bookingDetailTable.rowCount()):
                            self.gameList(self.bookingDetailTable.cellWidget(i, 8))

                        # Clear all the QLineEdits
                        self.gameTitle.clear()
                        self.gamePublisher.clear()
                        self.gameDescription.clear()
                        self.gameColour.clear()
                        self.gameDuration.clear()
                        
                        # Get reference needs to link new resource and topics
                        ref = "games"
                            
                # What to do if the file is open
                except PermissionError:
                    self.fileOpen()

        # Add if craft
        elif self.craftBox.isChecked():
            # Make sure all the required info is included
            if self.whatMaking.text() == "":
                self.missingData(self.whatMaking)

            else:
                # Revert colours where required
                self.whatMaking.setStyleSheet("background-color: ")
                
               # Add to the database and csv file
               # Make sure the csv file isn't open
                try:
                    with open ("Database/Arts & crafts.csv", "a") as crafts:
                        db.execute("INSERT INTO crafts (title, materials, duration, image, instructions, active) VALUES (?, ?, ?, ?, ?, 1)",
                            self.whatMaking.text().title(), self.materialsNeeded.text(), self.craftDuration.text(), self.craftImage.text(), self.craftInstructions.text())
                        resourceId = db.execute("SELECT id FROM crafts ORDER BY id DESC LIMIT 1")[0]["id"]
                        crafts.writelines(str(resourceId) + ',' + self.whatMaking.text().title() + ',"' + self.materialsNeeded.text() + '",' + self.craftDuration.text() + ',' + self.craftImage.text() + ',' + self.craftInstructions.text() + ',1\n')

                        # Update the Combobox
                        for i in range(self.bookingDetailTable.rowCount()):
                            self.craftList(self.bookingDetailTable.cellWidget(i, 9))

                        # Clear all the QLineEdits
                        self.whatMaking.clear()
                        self.materialsNeeded.clear()
                        self.craftImage.clear()
                        self.craftInstructions.clear()   
                        self.craftDuration.clear()             

                        # Get reference needs to link new resource and topics
                        ref = "crafts"
            
                # What to do if the file is open
                except PermissionError:
                    self.fileOpen()

        # Add if flashcards
        elif self.flashcardBox.isChecked():
            # Make sure all the required info is included
            if self.flashcardTitle.text() == "":
                self.missingData(self.flashcardTitle)
            
            else:
                # Revert the colours if required
                self.flashcardTitle.setStyleSheet("background-color: ")
                
                # Put the topics into a string
                topicString = self.listOfChosenTopics()

                # Add to the database and csv file
                # Make sure the csv file isn't open
                try:
                    with open ("Database/Flashcards.csv", "a") as f:
                        db.execute("INSERT INTO flashcards (title, topics, active) VALUES (?, ?, 1)", self.flashcardTitle.text().title(), topicString)
                        resourceId = db.execute("SELECT id FROM flashcards ORDER BY id DESC LIMIT 1")[0]["id"]
                        f.writelines(str(resourceId) + ',' + self.flashcardTitle.text() + ',"' + topicString + '",1\n')

                        # Clear the QLineEdits
                        self.flashcardTitle.clear()

                        # Get reference needs to link new resource and topics
                        ref = "flashcards"
                            
                # What to do if the file is open
                except PermissionError:
                    self.fileOpen()
        
        # Add to the resources table 
        if resourceId != "" and ref != "":
            db.execute("INSERT INTO resources (id, ref) VALUES (?, ?)", resourceId, ref)

        # Link to the topicLinks table when required
        if topicString != "":
            ts = topicString.split(", ")
            for t in ts:
                topicId = db.execute("SELECT id FROM topics WHERE topic = ?", t.capitalize())[0]['id']
                db.execute("INSERT INTO topicLink (topicId, resourceId, resourceType) VALUES (?, ?, ?)", topicId, resourceId, ref)

    def listOfChosenTopics(self):
        # Create a string with all the topics 
        topicString = ""
        for i in range(2, self.listOfTopics.columnCount(), 3):
            for j in range(self.listOfTopics.rowCount()):
                if self.listOfTopics.cellWidget(j, i) != None and self.listOfTopics.cellWidget(j, i).isChecked() and self.listOfTopics.item(j, i - 1).text() != "OTHER":
                    if topicString == "":
                        topicString += self.listOfTopics.item(j, i - 1).text()
                    else:
                        topicString += ", " + self.listOfTopics.item(j, i - 1).text()
                    self.listOfTopics.cellWidget(j, i).setChecked(False)

        # Deal with the 'other' topics        
        if self.additionalTopics.text() != "":
            # Add them to the topics string
            if topicString == "":
                topicString += self.additionalTopics.text()
            else:
                topicString += ", " + self.additionalTopics.text()

            # Also add the new topics to the topics table
            l = self.additionalTopics.text().split(', ')
            for value in l:
                value = value.capitalize()
                if db.execute("SELECT COUNT(*) FROM topics WHERE topic = ?", value)[0]['COUNT(*)'] == 0:
                    db.execute("INSERT INTO topics (topic) VALUES (?)", value)
            # Update the table accordingly
            self.layout6.removeRow(self.layout6.rowCount() - 3)
            self.additionalTopics.clear()
            self.w.hide()
            topicsLabel = QLabel('Topics')
            self.layout6.insertRow(self.layout6.rowCount() - 2, topicsLabel, self.topicList())

        return topicString



    # FORMATTING FUNCTIONS
    def setBorders(self, obj):
        obj.setFrameStyle(0x0001)
        obj.setFrameShadow(0x0020)
        obj.setLineWidth(5)
    
    def setScrollBar(self, obj):
            obj.setStyleSheet(
            "QScrollBar:horizontal {height: 20px; background-color: black;}"
            "QScrollBar:vertical {width: 20px; background-color: black;}")

    def setFontTitles(self, txt):
        txt.setStyleSheet("font: bold 18px")
    
    def boldFont(self):
        boldFont = QFont()
        boldFont.setBold(True)
        return boldFont

    def smallerFont(self):
        smallerFont = QFont()
        smallerFont.setPointSize(8)
        return smallerFont

    def hyperlink(self, txt):
        txt.setStyleSheet("font: 5px; color: blue; text-decoration: underline;")
    def hyperlinkClicked(self, txt):
        txt.setStyleSheet("font: 5px; color: green; text-decoration: underline;")

    def missingData(self, obj):
        obj.setStyleSheet("background-color: pink")

    def reorderTable(self, obj, column):
        if obj.horizontalHeader().sortIndicatorSection() != column:
            obj.sortItems(column, Qt.AscendingOrder)
        else:
            if obj.horizontalHeader().sortIndicatorOrder() == 1:
                obj.sortItems(column, Qt.DescendingOrder)
            else:
                obj.sortItems(column, Qt.AscendingOrder)



    # EXTERNAL FILES
    def addToTextFile(self, text, file):
        with open (file, 'a') as f:
            for value in text.split(', '):
                f.writelines(value + '\n')

    def rewriteCSVFile(self, file, data):
        # Extract the title's row
        t = []
        title = ""
        with open (file, "r") as readCSVFile:
            reader = csv.reader(readCSVFile)
            t = list(reader)[0]
        for i in range(len(t)):
            if i == 0:
                title += t[i]
            else: 
                title += ',' + t[i]

        # Update the csv file
        with open (file, "w") as writeCSVFile:
            writeCSVFile.writelines(title + '\n')
            for i in range(len(data)):
                values = list(data[i].values())
                valueString = ""
                for value in values:
                    if valueString == "":
                        valueString += '"' + str(value) + '"'
                    else:
                        valueString += ',"' + str(value) + '"'
                writeCSVFile.writelines(valueString + '\n')

    def openTextFiles(self, obj, row, currentcol, neededCol, table):
        # Show that the link was clicked
        if currentcol == neededCol:
            cell = obj.cellWidget(row, currentcol)
            if cell != None:
                self.hyperlinkClicked(cell)
                # Only take into consideration text editor and pdf files
                filePath = cell.text()
                if os.path.exists(filePath):
                    # Open the file in it's respective software
                    os.startfile(filePath)  
                # What to do if the file doesn't exist
                else:
                    self.fileError("No file with that name!", "Search document", obj, row, currentcol, table)
        
    def showImages(self, obj, row, column, table):
        # Only take into consideration the 'image' cell being clicked for this function
        if column == 4:
            # Set up the layout of the popup window that will contain the image and connect it to the hyperlink being clicked
            self.imagePopup = QWidget()
            lay = QHBoxLayout()
            self.imageRenderer = QLabel()
            lay.addWidget(self.imageRenderer)
            self.imagePopup.setLayout(lay)

            # Set the title of the window to the craft name
            self.imagePopup.setWindowTitle(self.foundCrafts.item(row, 1).text())
            
            # Make sure there is something written in the clicked cell
            clickedImageFileName = self.foundCrafts.cellWidget(row, column)
            if clickedImageFileName != None and clickedImageFileName.text() != "":
                # Change the font to show it has been clicked
                self.hyperlinkClicked(clickedImageFileName)
                # Set the image based on file path
                image = QPixmap(clickedImageFileName.text())
                fileTypes = (".png", ".jpg", ".jpeg", ".bmp")
                # Make sure it is the right file type and the file exists
                if clickedImageFileName.text().endswith(fileTypes) and os.path.exists(clickedImageFileName.text()):
                    self.imageRenderer.clear()
                    self.imageRenderer.setPixmap(image)
                    self.imagePopup.show()
                else:
                    # What to do if the file doesn't exist
                    if clickedImageFileName.text().endswith(fileTypes) and not os.path.exists(clickedImageFileName.text()):
                        message = "No file with that name!"
                        bttMessage = "Search Document"
                    # What to do if it is not an image
                    else:
                        message = "Wrong file type - this is not an image!"
                        bttMessage = "Search image"
                    self.fileError(message, bttMessage, obj, row, column, table)

    def fileError(self, message, bttMessage, obj, row, column, table):
        warning = QMessageBox()
        warning.setIcon(QMessageBox.Warning)
        warning.setText(message)
        warning.addButton("Find the correct file path", QMessageBox.YesRole)
        newFile = QLabel()
        self.hyperlink(newFile)
        # Connect the button to a new file search
        warning.buttonClicked.connect(lambda: self.searchFiles(bttMessage, newFile))
        # Show the popup box
        warning.exec_()  
        # Get db column title
        title = list(db.execute("SELECT * FROM ? LIMIT 1", table)[0].keys())[column]
        # Update the database
        db.execute("UPDATE ? SET ? = ? WHERE id = ?", table, title, newFile.text(), obj.item(row, 0).text())
        # Update the table
        obj.setCellWidget(row, column, newFile)

    def searchFiles(self, btt, line):
        # Popup window to search & select a document
        filesearch = QFileDialog()
        # Set the type of files that will appear in the search - will appear in 2 different rows so need to toggle between the 2
        if btt == "Search image":
            filesearch.setNameFilter("Image Files (*.png *.jpg *.jpeg *.bmp)")
        else:
            filesearch.setNameFilter("Text Files (*.docx *.pdf)")

        # Open the popup box
        filesearch.exec_()
        fileTypes = (".png", ".jpg", ".jpeg", ".bmp", ".docx", ".pdf")
        text = ""
        if len(filesearch.selectedFiles()) != 0:
            for i in range (len(filesearch.selectedFiles())):
                if filesearch.selectedFiles()[i].endswith(fileTypes):
                    text += filesearch.selectedFiles()[i]    
            line.setText(text)

    def fileOpen(self):
        warning = QMessageBox()
        warning.setIcon(QMessageBox.Warning)
        warning.setText("File open in another programme")
        warning.setInformativeText("CLOSE THE FILE BEFORE TRYING TO SAVE THE NEW DATA AGAIN")
        warning.exec_()



    # REPETITIVE STRUCTURES
    # Set up the QComboBoxes
    def activeStudentList(self, obj):
        obj.clear()
        obj.addItem("")
        # Automatically fill in the student list        
        s = db.execute("SELECT name FROM students WHERE active = 1 ORDER BY name")
        for i in range(len(s)):
            obj.addItem(s[i]['name'])
    def oldStudentList(self, box, obj):
        if box.isChecked():
            obj.clear()
            obj.addItem("")
            # Automatically fill in the student list        
            s = db.execute("SELECT name FROM students ORDER BY name")
            for i in range(len(s)):
                obj.addItem(s[i]['name'])
        else:
            self.activeStudentList(obj)
    def bookList(self, obj):
        obj.clear()
        obj.addItem("")
        b = db.execute("SELECT title FROM books WHERE active = 1 ORDER BY title")
        for i in range(len(b)):
            obj.addItem(b[i]["title"])
    def gameList(self, obj):
        obj.clear()
        obj.addItem("")
        g = db.execute ("SELECT title FROM games WHERE active = 1 ORDER BY title")
        for i in range(len(g)):
            obj.addItem(g[i]["title"])
    def craftList(self, obj):
        obj.clear()
        obj.addItem("")
        c = db.execute ("SELECT title FROM crafts WHERE active = 1 ORDER BY title")
        for i in range(len(c)):
            obj.addItem(c[i]["title"])
    def lessonList(self, obj):
        obj.clear()
        obj.addItem("")
        l = db.execute ("SELECT title FROM lessons WHERE active = 1 ORDER BY title")
        for i in range(len(l)):
            obj.addItem(l[i]["title"])

    # Set up the main push buttons
    def submitButton(self):
        b = QPushButton()
        b.setMaximumWidth(70)
        b.setText("Submit")
        return b 

    # Set up the 'Other' text field
    def otherField(self):
            other = QLineEdit()
            other.setPlaceholderText("Other")
            other.setFixedWidth(150)
            return other

    # Add a checkbox to a table and connect it to an action
    def addCheckBox(self, obj, row, column, function): 
        obj.setCellWidget(row, column, QCheckBox())
        obj.cellWidget(row, column).clicked.connect(function)   
