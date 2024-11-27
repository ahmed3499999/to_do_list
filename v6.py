import sys
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

    def __init__(self, task_name, task_desc, deadline, priority, repeat, parent=None):
        super().__init__(parent)

        # Layouts
        main_layout = QVBoxLayout()
        header_layout = QHBoxLayout()

        # Task Name
        self.task_name_label = QLabel(task_name)
        self.task_name_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #ffffff;"
        )
        header_layout.addWidget(self.task_name_label)

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
        self.task_desc_label = QLabel(task_desc)
        self.task_desc_label.setStyleSheet(
            "font-size: 14px; color: #cccccc; margin-top: 5px;"
        )

        # Assemble
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.repeat_label)
        main_layout.addWidget(self.task_desc_label)

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

        self.update_task_list()

        # Task list to hold added tasks
        

    def add_task(self):
        title = self.taskNameInput.text()
        desc = self.taskDescInput.toPlainText()
        ListManager.add_task('', title=title, describtion=desc)        
        self.update_task_list()
        # print(self.priorityInput.currentText())
        # Placeholder logic for adding a task
        # Retrieve inputs:. taskNameInput, taskDescInput, dateInput, priorityInput, repeatInput
        # Create a task object or entry in a list
       
    def update_task_list(self):
        #Empty list
        while self.taskListWidget.count() > 0:
            self.taskListWidget.takeItem(0)

        l: TaskList = ListManager.get_list('')
        self.taskListWidget.addItems([task.title for task in l.tasks])

    def remove_task(self):
        """Placeholder function for removing a selected task."""
        print("Remove Task button clicked")
        # Placeholder logic for removing a task
        # Identify the selected task from the QListWidget
        # Remove the task from the list and the QListWidget

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
