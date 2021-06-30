# -*- coding: utf-8 -*-
# rpcontacts/main.py

"""This module provides RP Contacts application."""

import sys
from .database import createConnection
from PyQt5.QtWidgets import QApplication
from .views import Window

def main():
    """RP Contacts Main function."""
    # Create the application
    app = QApplication(sys.argv)
    # Connect to database before creating window
    if not createConnection("contacts.sqlite"):
        sys.exit(1)
    # Create the main windows.
    win = Window()
    win.show()
    # Run the event loop
    sys.exit(app.exec())

