from PyQt5 import QtWidgets, QtCore
from UI_Styles import UI_Styles
import os
import sys
from time import sleep
import pandas as pd
from Tab1_Sorting import Tab1_Sorting
from Utils import getAttributes, AlignDelegate

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Scraping_Utils import search_result, scrape_data, driver, url

class ScrapingThread(QtCore.QThread):
    update_table_signal = QtCore.pyqtSignal(list)
    update_progress_signal = QtCore.pyqtSignal(int)
    setPauseLabel_signal = QtCore.pyqtSignal(str)
    resetScraping_signal = QtCore.pyqtSignal()
    
    def __init__(self, start_roll_no, end_roll_no):
        super().__init__()
        self.start_roll_no = start_roll_no
        self.end_roll_no = end_roll_no
        self.is_paused = False

    def run(self):
        arr = []
        for roll_no in range(self.start_roll_no, self.end_roll_no + 1):
            if self.is_paused:
                self.setPauseLabel_signal.emit("Waiting to resume...")
            else:
                self.setPauseLabel_signal.emit("Scrapping...")
            while self.is_paused:
                sleep(1)

            if not search_result(roll_no):
                print(f"Skipping roll number {roll_no} due to search error.")
                continue

            row = scrape_data(roll_no)
            if row:
                self.update_table_signal.emit(row)
                arr.append(row)
                
            self.update_progress_signal.emit((roll_no - self.start_roll_no + 1) * 100 // (self.end_roll_no - self.start_roll_no + 1))
            driver.get(url)
            sleep(1)
            
        self.resetScraping_signal.emit()
            
        if arr: 
            df = pd.DataFrame(arr, columns=[
                "Roll Number", "Name", "CNIC", "Urdu Marks", "English Marks", "Islamiat Marks",
                "Pak Study Marks", "Physics Marks", "Chemistry Marks", "Mathematics Marks", "Total Marks"
            ])
            df.to_csv("Scraping/biselahore_results.csv", mode='a', header=not os.path.isfile("Scraping/biselahore_results.csv"), index=False, encoding="utf-8")

class Tab2_Progress(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.scraping_thread = None

    def setupUi(self):
        self.layout = QtWidgets.QVBoxLayout(self)

        self.startLabel = QtWidgets.QLabel("Starting Roll No:", self)
        self.startLabel.setStyleSheet("""
            color: #2980b9;
            font-size: 16px;     
            font-weight: bold;
        """)
        self.layout.addWidget(self.startLabel)

        self.startInput = QtWidgets.QLineEdit(self)
        self.startInput.setStyleSheet(UI_Styles.getLineEditStyling())
        self.layout.addWidget(self.startInput)

        self.endLabel = QtWidgets.QLabel("Ending Roll No:", self)
        self.endLabel.setStyleSheet("""
            color: #2980b9;
            font-size: 16px;     
            font-weight: bold;
        """)
        self.layout.addWidget(self.endLabel)

        self.endInput = QtWidgets.QLineEdit(self)
        self.endInput.setStyleSheet(UI_Styles.getLineEditStyling())
        self.layout.addWidget(self.endInput)

        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setValue(0)
        self.progressBar.setStyleSheet("""
            QProgressBar {
                background-color: #e0e0e0;
                border: 2px solid #2980b9;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #2980b9;
                border-radius: 5px; 
            }
        """)
        self.progressBar.setTextVisible(False)
        self.progressBar.setFixedHeight(25)
        self.progressBar.setFixedWidth(300)
        
        self.percentageLabel = QtWidgets.QLabel("0%", self)
        self.percentageLabel.setStyleSheet("color: #2980b9; font-size: 16px; margin-top:10px;")
        self.percentageLabel.setAlignment(QtCore.Qt.AlignCenter)  
        self.layout.addWidget(self.percentageLabel)
        
        self.pauseLabel = QtWidgets.QLabel("", self)
        self.pauseLabel.setStyleSheet("""
            color: #2980b9;
            font-size: 17px;     
            font-weight: bold;
        """)
        self.layout.addWidget(self.pauseLabel, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.progressBar, alignment=QtCore.Qt.AlignCenter)

        self.button_layout = QtWidgets.QHBoxLayout()

        self.startBtn = UI_Styles.create_button("Start", self)
        self.startBtn.clicked.connect(self.startScraping)
        self.button_layout.addWidget(self.startBtn)

        self.pauseBtn = UI_Styles.create_button("Pause", self)
        self.pauseBtn.clicked.connect(self.pauseScraping)
        self.button_layout.addWidget(self.pauseBtn)

        self.resumeBtn = UI_Styles.create_button("Resume", self)
        self.resumeBtn.clicked.connect(self.resumeScraping)
        self.button_layout.addWidget(self.resumeBtn)

        self.stopBtn = UI_Styles.create_button("Stop/Reset", self)
        self.stopBtn.clicked.connect(self.resetScraping)
        self.button_layout.addWidget(self.stopBtn)

        self.layout.addLayout(self.button_layout)

        columns = getAttributes()[1:]
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.setHorizontalHeaderLabels(columns)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setStyleSheet(UI_Styles.getTableWidgetStyling())
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setColumnWidth(0,150)
        self.tableWidget.setColumnWidth(1,210)
        self.tableWidget.setColumnWidth(2,250)
        for i in range(3,self.tableWidget.columnCount()):
            self.tableWidget.setColumnWidth(i,157)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        delegate = AlignDelegate(self.tableWidget)
        self.tableWidget.setItemDelegate(delegate)
        self.layout.addWidget(self.tableWidget)

    def setPauseLabel(self,text):
        self.pauseLabel.setText(text)
        
    
    def startScraping(self):
        if not self.startInput.text() or not self.endInput.text() or not self.startInput.text().isdigit() or not self.endInput.text().isdigit():
            QtWidgets.QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers for roll numbers.")
            return
        start_roll_no = int(self.startInput.text())
        end_roll_no = int(self.endInput.text())
        
        if not (500001 <= start_roll_no <= 698365 and 500001 <= end_roll_no <= 698365):
            QtWidgets.QMessageBox.warning(self, "Invalid Input", "Roll numbers must be between 500001 and 698365.")
            return
        
        if start_roll_no > end_roll_no:
            QtWidgets.QMessageBox.warning(self, "Invalid Input", "Enter a valid range")
            return
        self.scraping_thread = ScrapingThread(start_roll_no, end_roll_no)
        self.scraping_thread.update_table_signal.connect(self.update_table)
        self.scraping_thread.update_progress_signal.connect(self.update_progress)
        self.scraping_thread.setPauseLabel_signal.connect(self.setPauseLabel)
        self.scraping_thread.resetScraping_signal.connect(self.resetScraping)
        self.scraping_thread.start()

    def update_table(self, row):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        for column, data in enumerate(row):
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, column, QtWidgets.QTableWidgetItem(str(data)))

    def update_progress(self, value):
        self.progressBar.setValue(value)
        self.percentageLabel.setText(f"{value}%")

    def pauseScraping(self):
        if self.scraping_thread:
            self.scraping_thread.is_paused = True

    def resumeScraping(self):
        if self.scraping_thread:
            self.scraping_thread.is_paused = False

    def resetScraping(self):
        if self.scraping_thread:
            self.scraping_thread.quit() 
            self.scraping_thread.wait() 
        self.startInput.clear()
        self.endInput.clear()
        self.update_progress(0)
        self.scraping_thread = None

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    tab2 = Tab2_Progress()
    window.setCentralWidget(tab2)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
