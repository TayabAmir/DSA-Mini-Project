from PyQt5 import QtWidgets, QtGui, QtCore

class UI_Styles:
    
    @staticmethod
    def get_combo_style():
        return """
        QComboBox {
            background-color: white; 
            border: 2px solid #2980b9;
            border-radius: 5px; 
            padding: 4px 10px; 
            color: #2980b9; 
        }
        QComboBox:hover {
            border: 2px solid #1f618d; 
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px; 
            border-left: 1px solid #2980b9; 
        }
        QComboBox::down-arrow {
            image: url('images/downArrow.jpeg'); 
            width: 20px;
            height: 20px;
        }
        QScrollBar:vertical {
            border: none;
            background: white;
            width: 10px;
            margin: 22px 0 22px 0;
        }
        QScrollBar::handle:vertical {
            background: #2980b9; 
            border-radius: 5px; 
            min-height: 20px; 
        }
        """

    @staticmethod
    def create_button(text, parent=None):
        button = QtWidgets.QPushButton(text, parent)
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.setFont(QtGui.QFont("Times New Roman", 12, QtGui.QFont.Bold))
        button.setStyleSheet("""
        QPushButton {
            background-color: transparent; 
            border: 2px solid #2980b9; 
            color: #2980b9; 
            border-radius: 8px;
            padding: 8px 20px;
        }
        QPushButton:hover {
            background-color: #2980b9; 
            color: white; 
        }
        QPushButton:pressed {
            background-color: #1f618d; 
        }
        """)
        return button

    @staticmethod
    def create_combobox(items, parent=None):
        combobox = QtWidgets.QComboBox(parent)
        combobox.setFont(QtGui.QFont("Times New Roman", 14))
        combobox.addItems(items)
        combobox.setStyleSheet(UI_Styles.get_combo_style())
        return combobox
    
    @staticmethod
    def getTableWidgetStyling():
        return "QTableWidget { color: #1f6398; background-color: white; border: 2px solid #1f6398; } QHeaderView::section { background-color: #2980b9;color: white;font-weight: bold;}"
    
    @staticmethod
    def getLineEditStyling():
        return """
            QLineEdit {
                color: #1f618d;      
                font-size: 18px;     
                height: 35px;        
                border: 2px solid #2980b9;
                border-radius: 5px;       
                padding: 5px;             
            }
            QLineEdit:focus {
                border: 2px solid #1f618d;
            }
        """
