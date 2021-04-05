from PyQt5 import QtWidgets, QtGui, QtCore, QtPrintSupport


# Used 
# Creates a button that can be clicked
class QPushButton(QtWidgets.QPushButton):

   # Imported from https://www.zeolearn.com/magazine/10-steps-for-getting-started-guis-with-python
    def __init__(self, parent=None):
        super(QPushButton, self).__init__(parent)
        self.setMouseTracking(True)
        self.setFixedHeight(30)
        self.setStyleSheet("font: 15px; margin: 1px; padding: 7px; background-color: black; color: white; border-style: solid; border-radius: 3px; border-width: 0.5px; border-color: black;")
    
    def enterEvent(self, event):
        self.setStyleSheet("font: 15px; margin: 1px; padding: 7px; background-color: grey; color: white; border-style: solid; border-radius: 3px; border-width: 0.5px; border-color: black;")
   
    def leaveEvent(self, event):
        self.setStyleSheet("font: 15px; margin: 1px; padding: 7px; background-color: black; color: white; border-style: solid; border-radius: 3px; border-width: 0.5px; border-color: black;")

# Can click as many of the boxes as you want
class QCheckBox(QtWidgets.QCheckBox):
   
    def __init__(self, parent=None):
        super(QCheckBox, self).__init__(parent)
        format(self)

# Can only click one or the other
class QRadioButton(QtWidgets.QRadioButton):
   
    def __init__(self, parent=None):
        super(QRadioButton, self).__init__(parent)
        format(self)

class QLabel(QtWidgets.QLabel):
   
    def __init__(self, parent=None):
        super(QLabel, self).__init__(parent)
        self.setStyleSheet("font: bold 15px")

class QLineEdit(QtWidgets.QLineEdit):
   
    def __init__(self, parent=None):
        super(QLineEdit, self).__init__(parent)
        format(self)

class QDateEdit(QtWidgets.QDateEdit):
   
    def __init__(self, parent=None):
        super(QDateEdit, self).__init__(parent)
        format(self)

class QTimeEdit(QtWidgets.QTimeEdit):
   
    def __init__(self, parent=None):
        super(QTimeEdit, self).__init__(parent)
        format(self)

class QSpinBox(QtWidgets.QSpinBox):
   
    def __init__(self, parent=None):
        super(QSpinBox, self).__init__(parent)
        format(self)

class QDoubleSpinBox(QtWidgets.QDoubleSpinBox):
   
    def __init__(self, parent=None):
        super(QDoubleSpinBox, self).__init__(parent)
        format(self)

class QComboBox(QtWidgets.QComboBox):
   
    def __init__(self, parent=None):
        super(QComboBox, self).__init__(parent)
        format(self)

class QFormLayout(QtWidgets.QFormLayout):
   
    def __init__(self, parent=None):
        super(QFormLayout, self).__init__(parent)

class QHBoxLayout(QtWidgets.QHBoxLayout):
   
    def __init__(self, parent=None):
        super(QHBoxLayout, self).__init__(parent)

class QVBoxLayout(QtWidgets.QVBoxLayout):
   
    def __init__(self, parent=None):
        super(QVBoxLayout, self).__init__(parent)

class QGridLayout(QtWidgets.QGridLayout):
   
    def __init__(self, parent=None):
        super(QGridLayout, self).__init__(parent)

class QTableWidget(QtWidgets.QTableWidget):
   
    def __init__(self, parent=None):
        super(QTableWidget, self).__init__(parent)
        self.setStyleSheet("font: 15px")
        tableFont = QFont()
        self.setFont(tableFont)
        self.horizontalHeader().setFixedHeight(50)
        self.verticalHeader().setVisible(False)
        self.setWordWrap(True)

class QTableWidgetItem(QtWidgets.QTableWidgetItem):
   
    def __init__(self, parent=None):
        super(QTableWidgetItem, self).__init__(parent)

class QHeaderView(QtWidgets.QHeaderView):
   
    def __init__(self, parent=None):
        super(QHeaderView, self).__init__(parent)
     
class QPixmap(QtGui.QPixmap):
       
    def __init__(self, parent=None):
        super(QPixmap, self).__init__(parent)

class QFileDialog(QtWidgets.QFileDialog):
   
    def __init__(self, parent=None):
        super(QFileDialog, self).__init__(parent)

class QMessageBox(QtWidgets.QMessageBox):
   
    def __init__(self, parent=None):
        super(QMessageBox, self).__init__(parent)

class QWidget(QtWidgets.QWidget):
   
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

class QFont(QtGui.QFont):
   
    def __init__(self, parent=None):
        super(QFont, self).__init__(parent)
        self.setPointSize(13)
        self.setFamily('Arial')



# Harmonise the format throughout all the classes
def format(self):
    self.setFixedHeight(30)
    self.setStyleSheet("font: 15px")
