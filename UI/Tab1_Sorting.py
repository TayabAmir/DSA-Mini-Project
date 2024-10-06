from PyQt5 import QtWidgets, QtGui, QtCore
from UI_Styles import UI_Styles
from sorting_algorithms import *
import time
from Utils import loadData,getAttributes,AlignDelegate,updateTable

class SortingDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, columns=[]):
        super().__init__(parent)
        self.setWindowTitle("Select Sorting Priorities")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.columns = columns

        self.combo1 = UI_Styles.create_combobox(columns, self)
        self.combo2 = UI_Styles.create_combobox(columns, self)
        self.combo3 = UI_Styles.create_combobox(columns, self)

        self.layout.addWidget(QtWidgets.QLabel("Primary Attribute:"))
        self.layout.addWidget(self.combo1)
        self.layout.addWidget(QtWidgets.QLabel("Secondary Attribute:"))
        self.layout.addWidget(self.combo2)
        self.layout.addWidget(QtWidgets.QLabel("Tertiary Attribute:"))
        self.layout.addWidget(self.combo3)

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout.addWidget(self.buttonBox)
    
    def setComboBoxes(self,values):
        self.combo1.setCurrentIndex(values[0]+1)
        self.combo2.setCurrentIndex(values[1]+1)
        self.combo3.setCurrentIndex(values[2]+1)

    def get_selected_columns(self):
        return self.combo1.currentIndex(), self.combo2.currentIndex(), self.combo3.currentIndex()


class Tab1_Sorting(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
    
    available_algorithms = ["--Select Algorithm--","Bubble Sort", "Insertion Sort", "Selection Sort", "Merge Sort",
                         "Hybrid Merge Sort", "Quick Sort", "Bucket Sort", "Radix Sort",
                         "Counting Sort", "Heap Sort", "Shell Sort", "Tim Sort"]
    columns = getAttributes()

    def setupUi(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setColumnCount(len(self.columns)-1)
        self.tableWidget.setHorizontalHeaderLabels(self.columns[1:])
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnWidth(0,150)
        self.tableWidget.setColumnWidth(1,210)
        self.tableWidget.setColumnWidth(2,250)
        self.tableWidget.setStyleSheet(UI_Styles.getTableWidgetStyling())
        self.tableWidget.verticalHeader().setVisible(False)
        
        
        for i in range(3,self.tableWidget.columnCount()):
            self.tableWidget.setColumnWidth(i,157)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        delegate = AlignDelegate(self.tableWidget)
        self.tableWidget.setItemDelegate(delegate)
        
        self.layout.addWidget(self.tableWidget)

        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.setHorizontalSpacing(20)
        self.main_layout.setVerticalSpacing(20)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        
        self.Attributes = UI_Styles.create_combobox(self.columns, self)
        self.Attributes.setStyleSheet(UI_Styles.get_combo_style())
        self.main_layout.addWidget(self.Attributes, 0, 0)

        self.Sorts = UI_Styles.create_combobox(self.available_algorithms, self)
        self.Sorts.setStyleSheet(UI_Styles.get_combo_style())
        self.main_layout.addWidget(self.Sorts, 0, 1) 
        
        self.startInput = QtWidgets.QLineEdit(self)
        self.startInput.setPlaceholderText("Start Index")
        self.startInput.setFixedWidth(200)
        self.startInput.setFixedHeight(30)
        self.startInput.setStyleSheet(UI_Styles.getLineEditStyling())
        self.main_layout.addWidget(self.startInput, 1, 0, alignment=QtCore.Qt.AlignLeft) 

        self.endInput = QtWidgets.QLineEdit(self)
        self.endInput.setPlaceholderText("End Index")
        self.endInput.setFixedWidth(200)
        self.endInput.setFixedHeight(30) 
        self.endInput.setStyleSheet(UI_Styles.getLineEditStyling())
        self.main_layout.addWidget(self.endInput, 1, 1, alignment=QtCore.Qt.AlignLeft) 

        self.radioAscending = QtWidgets.QRadioButton("Ascending", self)
        self.radioAscending.setStyleSheet("color: #2980b9; font-size: 16px; font-weight: bold;")
        self.radioAscending.setChecked(True)

        self.radioDescending = QtWidgets.QRadioButton("Descending", self)
        self.radioDescending.setStyleSheet("color: #2980b9; font-size: 16px; font-weight: bold;")
        self.radio_layout = QtWidgets.QHBoxLayout()
        self.radio_layout.addWidget(self.radioAscending)
        self.radio_layout.addWidget(self.radioDescending)

        self.main_layout.addLayout(self.radio_layout, 1, 2, alignment=QtCore.Qt.AlignLeft)

        self.sortingPriorityBtn = UI_Styles.create_button("Set Sorting Priorities", self)
        self.sortingPriorityBtn.clicked.connect(self.open_sorting_dialog)
        self.main_layout.addWidget(self.sortingPriorityBtn, 0, 2)

        self.runtimeLabel = QtWidgets.QLabel("Runtime: N/A", self)
        self.main_layout.addWidget(self.runtimeLabel, 0, 3, alignment=QtCore.Qt.AlignLeft)
        self.runtimeLabel.setStyleSheet("""
            color: #2980b9;    
            font-size: 16px;      
            font-weight: bold;   
        """)
        
        self.sortBtn = UI_Styles.create_button("Sort", self)
        self.sortBtn.setFixedWidth(400)
        self.sortBtn.clicked.connect(self.sortTable)
        self.main_layout.addWidget(self.sortBtn, 2, 0, 1, 4, alignment=QtCore.Qt.AlignCenter)

        self.layout.addLayout(self.main_layout)
        self.sortingColumns = [-1, -1, -1]

        
    def showEvent(self, event):
        self.tableWidget.setRowCount(0)
        loadData(self.tableWidget, 'Scraping/biselahore_results.csv')
        super().showEvent(event)
    
    def open_sorting_dialog(self):
        dialog = SortingDialog(self, columns=self.columns)
        dialog.setComboBoxes(self.sortingColumns)
        
        dialogResult = dialog.exec_()

        if dialogResult == QtWidgets.QDialog.Accepted:
            self.sortingColumns = list(dialog.get_selected_columns())
            for i in range(0,len(self.sortingColumns)):
                self.sortingColumns[i] -= 1
            if self.sortingColumns[0] >= 0 and self.sortingColumns[1] >= 0 and self.sortingColumns[2] >= 0:
                self.Sorts.setCurrentIndex(4)
                self.Attributes.setCurrentIndex(0)
                self.Sorts.setEnabled(False)
                self.Attributes.setEnabled(False)
            else:
                self.Sorts.setEnabled(True)
                self.Attributes.setEnabled(True)
                
        if dialogResult == QtWidgets.QDialog.Rejected:
            self.sortingColumns[0] = self.sortingColumns[1] = self.sortingColumns[2] = -1
            self.Sorts.setEnabled(True)
            self.Attributes.setEnabled(True)
    
    def sortTable(self):
        
        selectedColumn = self.Attributes.currentIndex()-1
        sortingAlgorithm = self.Sorts.currentText()
        
        if (selectedColumn == -1 or sortingAlgorithm == "--Select Algorithm--") and (self.sortingColumns[0] == -1 or self.sortingColumns[1] == -1 or self.sortingColumns[2] == -1):
            QtWidgets.QMessageBox.warning(
                self, "Input Error", "Please select Algorithm or Column to sort"
            )
            return
        
        if self.startInput.text():
            if self.startInput.text().isdigit():
                start = int(self.startInput.text())
                if not (0 <= start <= self.tableWidget.rowCount()):
                    QtWidgets.QMessageBox.warning(
                        self, "Input Error", "Please enter a valid start index within the range."
                    )
                    return
            else:
                QtWidgets.QMessageBox.warning(
                    self, "Input Error", "Please enter valid integer values for start index."
                )
                return
        else:
            start = 0

        if self.endInput.text():
            if self.endInput.text().isdigit():
                end = int(self.endInput.text())
                if not (0 <= end <= self.tableWidget.rowCount()):
                    QtWidgets.QMessageBox.warning(
                        self, "Input Error", "Please enter a valid end index within the range."
                    )
                    return
            else:
                QtWidgets.QMessageBox.warning(
                    self, "Input Error", "Please enter valid integer values for end index."
                )
                return
        else:
            end = self.tableWidget.rowCount()

        if start >= end:
            QtWidgets.QMessageBox.warning(
                self, "Input Error", "Please enter a valid range where start is less than end."
            )
            return
        
        arr = ["Bucket Sort", "Radix Sort", "Counting Sort"]
        if sortingAlgorithm in arr and selectedColumn in [0, 1, 2]:
            QtWidgets.QMessageBox.warning(
                self,
                "Sorting Error",
                "Cannot sort the selected column using this sorting algorithm."
            )
            return

        data = []
        rowCount = self.tableWidget.rowCount()
        for row in range(rowCount):
            row_data = []
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                if col in [3,4,5,6,7,8,9,10]:
                    row_data.append(int(item.text()))
                else:
                    row_data.append(item.text())
            data.append(row_data)

        start_time = time.time()
        singleSorting = True
        if self.sortingColumns[0] != -1 and self.sortingColumns[1] != -1 and self.sortingColumns[2] != -1:
            self.multiColumnSort(data, start, end, self.sortingColumns)
            self.sortingColumns = [-1,-1,-1]
            singleSorting = False
        else:
            if sortingAlgorithm == "Bubble Sort":
                bubble_sort(data, start, end, selectedColumn)
            elif sortingAlgorithm == "Insertion Sort":
                insertion_sort(data, start, end, selectedColumn)
            elif sortingAlgorithm == "Selection Sort":
                selection_sort(data, start, end, selectedColumn)
            elif sortingAlgorithm == "Merge Sort":
                merge_sort(data, start, end, selectedColumn)
            elif sortingAlgorithm == "Hybrid Merge Sort":
                hybrid_merge_sort(data, start, end, selectedColumn)
            elif sortingAlgorithm == "Quick Sort":
                quick_sort(data, start, end - 1, selectedColumn)
            elif sortingAlgorithm == "Bucket Sort":
                bucket_sort(data, start, end, selectedColumn)
            elif sortingAlgorithm == "Radix Sort":
                radix_sort(data, start, end, selectedColumn)
            elif sortingAlgorithm == "Counting Sort":
                counting_sort(data, start, end, selectedColumn)
            elif sortingAlgorithm == "Heap Sort":
                heap_sort(data, start, end, selectedColumn)
            elif sortingAlgorithm == "Shell Sort":
                shell_sort(data, start, end, selectedColumn)
            elif sortingAlgorithm == "Tim Sort":
                tim_sort(data, start, end, selectedColumn)

        end_time = time.time()

        if self.radioDescending.isChecked():
            data.reverse()
            
        updateTable(self, data)
        self.runtimeLabel.setText(f"Runtime: {end_time - start_time} seconds")
        
        
        if singleSorting:
            QtWidgets.QMessageBox.information(
                self,
                "Sorted",
                "Single-Column sorting is applied"
            )
        else:
            self.Sorts.setEnabled(True)
            self.Attributes.setEnabled(True)
            QtWidgets.QMessageBox.information(
                self,
                "Sorted",
                "Multi-Column sorting is applied"
            )
    
    def multiColumnSort(self, data, start, end, sortingColumns):
        
        col1, col2, col3 = sortingColumns[0], sortingColumns[1], sortingColumns[2]        
        merge_sort(data, start, end, col1)
        
        i = 0
        while i < len(data):
            strt = nd = i
            value = data[i][col1]
            while nd < len(data) and data[nd][col1] == value:
                nd += 1
            merge_sort(data, strt, nd, col2)
            
            j = strt
            while j < nd:
                strt2 = nd2 = j
                value2 = data[j][col2]
                while nd2 < nd and data[nd2][col2] == value2:
                    nd2 += 1
                merge_sort(data, strt2, nd2, col3)
                j = nd2
                
            i = nd

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    tab1 = Tab1_Sorting()
    window.setCentralWidget(tab1)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())