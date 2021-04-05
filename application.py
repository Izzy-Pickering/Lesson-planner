# import all needed libraries
from cs50 import SQL
from PyQt5 import QtWidgets
from Tabs import Tabs
import sys


# Open the app (calling pyqt base app, calling show() to starting our GUI application) 
app = QtWidgets.QApplication(sys.argv)

# Display the tabs
tab = Tabs()
tab.showMaximized()
    
# Exit the application
sys.exit(app.exec_())
