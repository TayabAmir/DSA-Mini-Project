import time
from PyQt5 import QtWidgets, QtCore
from UI_Styles import UI_Styles
from Utils import getAttributes,AlignDelegate,loadData,updateTable

from PyQt5 import QtWidgets

class SortingDialog(QtWidgets.QDialog):
    logicalOperators = ["AND", "OR"]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Attributes")
        self.setModal(True)
        self.setFixedSize(500, 400)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.combo1 = UI_Styles.create_combobox(getAttributes(), self)
        self.combo1.setStyleSheet(UI_Styles.get_combo_style())
        self.layout.addWidget(self.combo1)

        self.textbox1 = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.textbox1)

        self.condition1 = UI_Styles.create_combobox(self.logicalOperators, self)
        self.layout.addWidget(self.condition1)

        self.combo2 = UI_Styles.create_combobox(getAttributes(), self)
        self.combo2.setStyleSheet(UI_Styles.get_combo_style())
        self.layout.addWidget(self.combo2)

        self.textbox2 = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.textbox2)

        self.condition2 = UI_Styles.create_combobox(self.logicalOperators, self)
        self.layout.addWidget(self.condition2)

        self.combo3 = UI_Styles.create_combobox(getAttributes(), self)
        self.combo3.setStyleSheet(UI_Styles.get_combo_style())
        self.layout.addWidget(self.combo3)

        self.textbox3 = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.textbox3)

        self.button_box = QtWidgets.QDialogButtonBox(self)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)


class Tab4_Search(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.values = None        
        self.layout = QtWidgets.QVBoxLayout(self)

        self.tableWidget = QtWidgets.QTableWidget(self)
        columns = getAttributes()[1:]
        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.setStyleSheet(UI_Styles.getTableWidgetStyling())
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setColumnWidth(0,150)
        self.tableWidget.setColumnWidth(1,210)
        self.tableWidget.setColumnWidth(2,250)
        for i in range(3,self.tableWidget.columnCount()):
            self.tableWidget.setColumnWidth(i,157)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(columns)
        
        delegate = AlignDelegate(self.tableWidget)
        self.tableWidget.setItemDelegate(delegate)
          
        self.layout.addWidget(self.tableWidget)

        self.row_layout = QtWidgets.QHBoxLayout()

        
        self.dialogBtn = UI_Styles.create_button("Select Columns", self)
        self.dialogBtn.clicked.connect(self.openDialog)
        self.row_layout.addWidget(self.dialogBtn)
        
        self.filters = UI_Styles.create_combobox(["--Filter--", "Starts With", "Contains", "Ends With"], self)
        self.filters.setStyleSheet(UI_Styles.get_combo_style())
        self.row_layout.addWidget(self.filters)

        self.resetButton = UI_Styles.create_button("Reset",self)
        self.row_layout.addWidget(self.resetButton)
        
        self.layout.addLayout(self.row_layout)

        search_layout = QtWidgets.QHBoxLayout()

        self.runtimeLabel = QtWidgets.QLabel("Runtime: N/A", self)
        self.runtimeLabel.setStyleSheet("""
            color: #2980b9;
            font-size: 16px;     
            font-weight: bold;
        """)
        search_layout.addWidget(self.runtimeLabel)

        self.layout.addLayout(search_layout)

        self.searchBtn = UI_Styles.create_button("Search", self)
        self.searchBtn.setFixedWidth(400)
        self.layout.addWidget(self.searchBtn)
        
        search_button_layout = QtWidgets.QHBoxLayout()
        search_button_layout.addStretch()
        search_button_layout.addWidget(self.searchBtn)
        search_button_layout.addStretch() 

        self.layout.addLayout(search_button_layout)
        self.resetButton.clicked.connect(self.resetData)
        self.searchBtn.clicked.connect(self.searchValue)
        loadData(self.tableWidget, 'Scraping/biselahore_results.csv')

    def resetData(self):
        self.tableWidget.setRowCount(0)
        self.runtimeLabel.setText(f"Runtime: N/A")
        loadData(self.tableWidget, 'Scraping/biselahore_results.csv')

    def openDialog(self):
        dialog = SortingDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            col1 = dialog.combo1.currentIndex()-1
            val1 = dialog.textbox1.text()
            condition1 = dialog.condition1.currentText()

            col2 = dialog.combo2.currentIndex()-1
            val2 = dialog.textbox2.text()
            condition2 = dialog.condition2.currentText()

            col3 = dialog.combo3.currentIndex()-1
            val3 = dialog.textbox3.text()

            self.values = {
                "col1": col1,
                "value1": val1,
                "cond1": condition1,
                "col2": col2,
                "value2": val2,
                "cond2": condition2,
                "col3": col3,
                "value3": val3
            }
    
    def searchValue(self):
        if not self.values:
            QtWidgets.QMessageBox.warning(self, "Search Error", "Please Enter Some Value to Search")
            return
        
        data = []
        filter = self.filters.currentText()
        print(self.values)
        row_count = self.tableWidget.rowCount()
        for row in range(row_count):
            row_data = []
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                row_data.append(item.text())
            data.append(row_data)
            
        start_time = time.time()
        
        def applyFilter(value, filter_type, search_term):
            if filter_type == "Starts With":
                return value.startswith(search_term)
            elif filter_type == "Contains":
                return search_term in value
            elif filter_type == "Ends With":
                return value.endswith(search_term)
            else:
                return value == search_term

        def filterSearch(data, column, value, filter_type):
            result = []
            for row in data:
                if applyFilter(str(row[column]), filter_type, str(value)):
                    result.append(row)
            return result

        active_columns = [col for col in ["col1", "col2", "col3"] if self.values[col] != -1]
        num_active_columns = len(active_columns)

        if num_active_columns == 1:
            result = filterSearch(data, self.values[active_columns[0]], self.values[f"value{active_columns[0][-1]}"], filter)
        
        elif num_active_columns == 2:
            col1, col2 = active_columns
            value1, value2 = self.values[f"value{col1[-1]}"], self.values[f"value{col2[-1]}"]
            condition = self.values["cond1"]

            if condition == "AND":
                result = filterSearch(data, self.values[col1], value1, filter)
                result = filterSearch(result, self.values[col2], value2, filter)
            elif condition == "OR":
                result1 = filterSearch(data, self.values[col1], value1, filter)
                result2 = filterSearch(data, self.values[col2], value2, filter)
                result = list(set(result1 + result2)) 
        
        else:
            if self.values["cond1"] == "AND" and self.values["cond2"] == "OR":
                searchedArray = filterSearch(data, self.values["col1"], self.values["value1"], filter)
                searchedArray = filterSearch(searchedArray, self.values["col2"], self.values["value2"], filter)
                result = filterSearch(data, self.values["col3"], self.values["value3"], filter) + searchedArray
                result = list(set(map(tuple, result))) 

            elif self.values["cond1"] == "OR" and self.values["cond2"] == "AND":
                searchedArray = filterSearch(data, self.values["col2"], self.values["value2"], filter)
                searchedArray = filterSearch(searchedArray, self.values["col3"], self.values["value3"], filter)
                result = filterSearch(data, self.values["col1"], self.values["value1"], filter) + searchedArray
                result = list(set(map(tuple, result))) 

            elif self.values["cond1"] == "AND" and self.values["cond2"] == "AND":
                result = filterSearch(data, self.values["col1"], self.values["value1"], filter)
                result = filterSearch(result, self.values["col2"], self.values["value2"], filter)
                result = filterSearch(result, self.values["col3"], self.values["value3"], filter)

            elif self.values["cond1"] == "OR" and self.values["cond2"] == "OR":
                result = (filterSearch(data, self.values["col1"], self.values["value1"], filter) +
                        filterSearch(data, self.values["col2"], self.values["value2"], filter) +
                        filterSearch(data, self.values["col3"], self.values["value3"], filter))
                result = list(set(map(tuple, result)))

        updateTable(self, result)
        
        end_time = time.time()
        
        self.runtimeLabel.setText(f"Runtime: {end_time - start_time} seconds")
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    tab1 = Tab4_Search()
    window.setCentralWidget(tab1)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())