from PyQt5 import QtWidgets, QtCore
import csv

class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter

def loadData(tableWidget, file_path):
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row_data in reader:
                    row = tableWidget.rowCount()
                    tableWidget.insertRow(row)
                    for column, data in enumerate(row_data):
                        tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(data))
        except Exception as e:
            print(f"Error reading file: {e}")

def getAttributes():
    return ["--Select Attribute--","Roll Number", "Name", "CNIC", "Urdu", "English", "Islamiat", "Pak Study", "Physics", "Chemistry", "Mathematics", "Total Marks"]

def updateTable(self, data):
        self.tableWidget.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.tableWidget.insertRow(row_idx)
            for col_idx, col_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(col_data))
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(row_idx, col_idx, item)