# -*- coding: utf-8 -*-

"""This module provides views to manage the contacts table."""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QTableView
)
from .model import ContactsModel

class Window(QMainWindow):
    """Main Window."""
    def __init__(self,parent = None):
        """Initializer"""
        super().__init__(parent)
        self.setWindowTitle("RP Contacts")
        self.resize(550,250)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.contactsModel = ContactsModel()
        self.setupUI()

    def setupUI(self):
        """Setup the main window's GUI."""
        # Create the table view widget
        self.table = QTableView()
        self.table.setModel(self.contactsModel.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()
        # Create buttons
        self.addButton = QPushButton("ADD")
        self.addButton.clicked.connect(self.openAddDialog)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteContact)
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clearContact)
        # Layout the GUI
        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addStretch()
        layout.addWidget(self.clearAllButton)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)

    def deleteContact(self):
        """Delete the selected row from the database"""
        row = self.table.currentIndex().row()
        if row<0:
            return

        messageBox = QMessageBox.warning(
            self,
            "Waning!",
            "Do you want to delete the selected contact?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.contactsModel.deleteContact(row)

    def openAddDialog(self):
        """Open Add Contact Dialog."""
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.contactsModel.addContact(dialog.data)
            self.table.resizeColumnsToContents()

    def clearContact(self):
        """Remove all contacts from the database"""
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove all conatacts?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.contactsModel.clearContacts()

class AddDialog(QDialog):
    """ Add contact dialog."""
    def __init__(self,parent = None):
        super().__init__(parent=parent)
        self.setWindowTitle("Add Contact")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None
        self.setupUI()

    def setupUI(self):
        """Setup the add contacts GUI"""
        # Create line edits for data fields
        self.nameField = QLineEdit()
        self.nameField.setObjectName("Name")
        self.jobField = QLineEdit()
        self.jobField.setObjectName("Job")
        self.emailField = QLineEdit()
        self.emailField.setObjectName("Email")

        # Lay out of data fields
        layout = QFormLayout()
        layout.addRow("Name: ",self.nameField)
        layout.addRow("Job: ",self.jobField)
        layout.addRow("Email: ",self.emailField)
        self.layout.addLayout(layout)

        #Add standard buttons to the dialog and connect item
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        """Accept the data provided through dialog."""
        self.data = []
        for field in  (self.nameField,self.jobField,self.emailField):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide a contact's {field.objectName()}",
                )
                self.data = None
                return

            self.data.append(field.text())

        if not self.data:
            return

        super().accept()
