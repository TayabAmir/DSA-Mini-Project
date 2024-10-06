from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from Tab1_Sorting import Tab1_Sorting
from Tab2_Progress import Tab2_Progress
from Tab4_Search import Tab4_Search

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("BISE LAHORE DATA SCRAPPER")

        self.centralwidget = QtWidgets.QWidget(self)
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        
        self.title_layout = QtWidgets.QHBoxLayout()

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_pixmap = QtGui.QPixmap("images/bise-lahore-board-logo.jpg") 
        self.icon_label.setPixmap(self.icon_pixmap.scaled(100, 75, QtCore.Qt.KeepAspectRatio))  # Larger size
        self.title_layout.addWidget(self.icon_label)
        
        self.title_label = QtWidgets.QLabel("BISE LAHORE DATA SCRAPPER", self)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter) 
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2980b9;")
        self.title_layout.addWidget(self.title_label)
        
        self.title_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addLayout(self.title_layout)

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        self.tabWidget.setStyleSheet("""
            QTabBar::tab {  
                background-color: transparent;
                border: 2px solid #2980b9;
                color: #2980b9;
                height: 35px; width: 578px;
                border-radius: 8px;
                padding: 8px 20px; 
                margin: 5px;
                font-size: 16px;
            }
            QTabBar::tab:hover {
                background-color: #2980b9;
            }
            QTabBar::tab:selected { 
                background-color: #1f618d;
                color: white;
            }
            QTabBar::tab:!selected { 
                background-color: transparent;
            }
        """)


        self.tab1 = Tab1_Sorting()
        self.tabWidget.addTab(self.tab1, "Sorting")

        self.tab2 = Tab2_Progress()
        self.tabWidget.addTab(self.tab2, "Control & Progress")

        self.tab4 = Tab4_Search()
        self.tabWidget.addTab(self.tab4, "Search")

        self.main_layout.addWidget(self.tabWidget)
        self.setCentralWidget(self.centralwidget)
        
        self.tabWidget.tabBar().setExpanding(True)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(
            self, 'Close Confirmation',
            "Are you sure you want to close the application?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.showMaximized() 
    sys.exit(app.exec_())
