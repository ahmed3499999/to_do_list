import sys
from datetime import date
from task_list import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate, QTimer
from PyQt5.QtWidgets import (
    QMessageBox,
    QListWidgetItem,
    QListView,
    QWidget,
    QListWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
)


class TaskWidget(QWidget):
    """Custom widget to represent a task in the list."""

    def __init__(self, title, desc, deadline, priority, repeat, parent=None):
        super().__init__(parent)

        # Layouts
        main_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
    
        # Task Name
        self.title = title
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #ffffff;"
        )
        header_layout.addWidget(self.title_label)

        # Priority
        self.priority_label = QLabel(priority)
        self.priority_label.setStyleSheet(
            f"font-size: 12px; font-weight: bold; color: {'#ff4d4d' if priority == 'High' else '#ffd700' if priority == 'Medium' else '#4caf50'};"
        )
        header_layout.addWidget(self.priority_label)

        # Deadline
        self.deadline_label = QLabel(deadline)
        self.deadline_label.setStyleSheet("font-size: 12px; color: #aaaaaa;")
        header_layout.addWidget(self.deadline_label)

        # Repeat Frequency
        self.repeat_label = QLabel(f"Repeat: {repeat}")
        self.repeat_label.setStyleSheet(
            "font-size: 12px; color: #cccccc; margin-top: 5px;"
        )

        # Task Description
        self.desc_label = QLabel(desc)
        self.desc_label.setStyleSheet(
            "font-size: 14px; color: #cccccc; margin-top: 5px;"
        )

        # Assemble
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.repeat_label)
        main_layout.addWidget(self.desc_label)

        self.setLayout(main_layout)
        self.setStyleSheet(
            "background-color: #23272a; border-radius: 10px; padding: 10px;"
        )


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the .ui file
        uic.loadUi("v5.ui", self)

        # Connect GUI elements to their respective functions
        self.addTaskButton.clicked.connect(self.add_task)
        self.removeTaskButton.clicked.connect(self.remove_task)
        # self..clicked.connect(self.remove_task)
        self.sortTasksDropdown.currentIndexChanged.connect(self.sort_tasks)
        self.repeatInput.currentIndexChanged.connect(self.handle_repeat_change)

        # Initialize the date input with today's date
        self.dateInput.setDate(QDate.currentDate())

        # to retrieve tasks in database on startup
        self.update_task_list()
        

    def add_task(self):
        title = self.taskNameInput.text().strip()
        desc = self.taskDescInput.toPlainText().strip()
        qdate = self.dateInput.date()
        #convert QDate to python Date object
        deadline = date(qdate.year(),qdate.month(),qdate.day())
        priority_text = self.priorityInput.currentText().lower().strip()
        repeatness_text = self.repeatInput.currentText().lower().strip()
        
        # convert string priority and repeatness to integer for database storage
        TaskManager.add_task(title=title, description=desc, deadline=deadline,
                             priority=Priority[priority_text].value,
                             repeatness=Repeat[repeatness_text].value)        
        self.update_task_list()
       
    def update_task_list(self):
        # make the list empty first
        while self.taskListWidget.count() > 0:
            self.taskListWidget.takeItem(0)

        # loop over every task we have and create a widget for it in the gui list
        for task in TaskManager.get_all_tasks():
            # Create and add custom task widget
            task_widget = TaskWidget(
                task.title, task.description, task.deadline.strftime("%Y-%m-%d"),
                Priority(task.priority).name.capitalize(), Repeat(task.repeatness).name.capitalize()
            )
            
            # stuff for gui, doesnt matter
            list_item = QListWidgetItem()
            list_item.setSizeHint(task_widget.sizeHint())
            self.taskListWidget.addItem(list_item)
            self.taskListWidget.setItemWidget(list_item, task_widget)

    def remove_task(self):
        #find selected row in gui list
        row = self.taskListWidget.currentRow()
        if row < 0: return
        
        # retrieve item at row, then retrieve the task widget at that row and get its title
        item = self.taskListWidget.item(row)
        delete_task(self.taskListWidget.itemWidget(item).title)

        self.update_task_list()

    def sort_tasks(self):
        """Placeholder function for sorting tasks."""
        print("Sort Tasks dropdown value changed")
        # Placeholder logic for sorting tasks
        # Retrieve the selected sort option (e.g., by priority, deadline)
        # Sort the internal task list
        # Update the QListWidget with the sorted list

    def handle_repeat_change(self):
        """Placeholder function for handling changes to the repeat option."""
        repeat_option = self.repeatInput.currentText()
        print(f"Repeat option changed to: {repeat_option}")
        # Placeholder logic for handling repeat option changes

    def add_to_google_calendar(self, task):
        """Placeholder function for integrating Google Calendar."""
        print("Add to Google Calendar function triggered")
        # Placeholder logic for adding a task to Google Calendar
        # Integrate with Google Calendar API (requires credentials.json and authentication)

    def check_notifications(self):
        """Placeholder function for checking and sending notifications."""
        print("Notification timer triggered")
        # Placeholder logic for notifications
        # Check if any tasks are due within a certain timeframe (e.g., next hour)
        # Send a desktop notification for approaching deadlines


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
