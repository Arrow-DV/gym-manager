# Made By Arrow-Dev | Ali Hany
# visit us https://arrow-dev.rf.gd/bio
# Created in 2/17/2024 | Last Update 2/7/2024



from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import QDate,Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6 import uic
from PIL import Image
import os
import sqlite3

os.system("start https://arrow-dev.rf.gd/bio")
os.system("start https://youtu.be/yGKSgWXjQBQ?si=Zezo7Ue8GwxSzWzG")
# Connect DataBase
sql = sqlite3.connect("Data/data.db")
# Cursor To Execute Commands
cursor = sql.cursor()
# Create Table
cursor.execute("CREATE TABLE IF NOT EXISTS users (id integer,name text,exp text,mobile text)")
sql.commit()


class window(QMainWindow):
    def enable(self):
        buttons = [self.add,  self.search]
        if self.username.toPlainText().strip() != "" or self.mobile.toPlainText().strip() != "":
            for button in buttons:
                button.setEnabled(True)
        else:
            for button in buttons:
                button.setEnabled(False)

    def __init__(self) -> None:
        super(window, self).__init__()
        uic.loadUi("Data/gui.ui", self)
        self.setFixedSize(self.size())
        self.show()

        # Set Time
        self.date.setDate(QDate.currentDate())

        # Data View
        self.model = QStandardItemModel(self.tree)
        self.model.setHorizontalHeaderLabels(['ID', 'NAME', 'EXPIRE DATE', "MOBILE"])
        self.tree.setModel(self.model)

        # Show Data
        self.load_data()

        # Check Textbox
        for textbox in [self.username, self.mobile]:
            textbox.textChanged.connect(self.enable)
        # Add Button
        self.add.clicked.connect(self.add_action)
        # Delete Button
        self.remove.clicked.connect(self.remove_action)
        # Search Button
        self.search.clicked.connect(self.search_action)

    def add_action(self):
        try:
            # Find the maximum existing ID
            cursor.execute("SELECT MAX(id) FROM users")
            max_id = cursor.fetchone()[0]

            # Increment the ID for the new entry
            if max_id is not None:
                new_id = max_id + 1
            else:
                new_id = 1

            # Insert the new entry with the incremented ID
            cursor.execute("INSERT INTO users (id, name, exp, mobile) VALUES (?, ?, ?, ?)",
                        (new_id,
                            self.username.toPlainText().strip(),
                            self.date.date().toString("yyyy/MM/dd"),
                            self.mobile.toPlainText().strip()))
            sql.commit()

            # Show confirmation message
            QMessageBox.information(self, "Success", "Data added successfully!")

        except sqlite3.Error as e:
            # Show error message box
            QMessageBox.critical(self, "Error", f"Error inserting data: {e}")

        self.load_data()


    def remove_action(self):
        selected_indexes = self.tree.selectionModel().selectedIndexes()

        if not selected_indexes:
            return  # No item selected, nothing to remove

        # Assuming the ID is in the first column (index 0)
        selected_id = selected_indexes[0].data()

        try:
            cursor.execute("DELETE FROM users WHERE id=?", (selected_id,))
            sql.commit()

            # Show confirmation message
            QMessageBox.information(self, "Success", "Data removed successfully!")

        except sqlite3.Error as e:
            # Show error message box
            QMessageBox.critical(self, "Error", f"Error removing data: {e}")

        self.load_data()

    def search_action(self):
        search_text = self.username.toPlainText().strip()
        if not search_text:
            search_text = self.mobile.toPlainText().strip()
        if not search_text:
            return None


        # Fetch and append new data based on the search criteria
        cursor.execute("SELECT * FROM users WHERE name LIKE ? OR mobile LIKE ?",
                   ('%' + search_text + '%', '%' + search_text + '%'))
        _list_ = cursor.fetchall()[0]
        message = f"""ID : {_list_[0]}
Name : {_list_[1]}
EXP : {_list_[2]}
Mobile : {_list_[3]}
""" 
        QMessageBox.information(self,"Found",message)
    def load_data(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['ID', 'NAME', 'EXPIRE DATE', "MOBILE"])
        self.tree.setModel(self.model)

        cursor.execute("SELECT * FROM USERS")
        _list_ = cursor.fetchall()
        for row in _list_:
            items = [QStandardItem(str(item)) for item in row]
            self.model.appendRow(items)


def main():
    app = QApplication([])
    main_window = window()
    app.exec()


if __name__ == "__main__":
    main()
