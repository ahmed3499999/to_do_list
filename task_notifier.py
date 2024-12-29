from datetime import datetime
import logging
from plyer import notification
from typing import List
from task_list import *

class TaskNotifier:
    def __init__(self):
        self.notification_levels = {
            3: "THREE DAYS NOTICE: Task approaching",
            1: "URGENT: Task due tomorrow",
            0: "FINAL NOTICE: Task due today",
        }

    def check_notifications(self, task_lists: List[TaskList]) -> None:
        """
        Check all tasks in all lists for approaching deadlines and send notifications.
        """
        try:
            now = datetime.now()

            for task_list in task_lists:
                for task in task_list.tasks:
                    # Skip if task is already completed or has no deadline
                    if task.checked:
                        continue

                    # Calculate days remaining
                    days_remaining = (task.deadline - now.date()).days

                    # Handle overdue tasks
                    if days_remaining < 0:
                        self._send_notification(
                            title=f"❗ OVERDUE: {task.title}",
                            message=(
                                f"Task is overdue by {abs(days_remaining)} days!\n"
                                f"Description: {task.description}\n"
                                f"Priority: {task.priority.name}"
                            ),
                        )
                        continue

                    # Check for matching notification levels (3 days, 1 day, or due today)
                    if days_remaining in self.notification_levels:
                        # Create appropriate time message
                        if days_remaining == 0:
                            time_message = "due today"
                        elif days_remaining == 1:
                            time_message = "due tomorrow"
                        else:
                            time_message = f"due in {days_remaining} days"

                        self._send_notification(
                            title=f"{self.notification_levels[days_remaining]}: {task.title}",
                            message=(
                                f"Task {time_message}\n"
                                f"Description: {task.description}\n"
                                f"Priority: {task.priority.name}\n"
                                f"Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M')}"
                            ),
                        )

        except Exception as e:
            logging.error(f"Error in notification check: {str(e)}")

    def _send_notification(self, title: str, message: str) -> None:
        """Send a notification with the given title and message."""
        try:
            notification.notify(title=title, message=message, timeout=10)
        except Exception as e:
            logging.error(f"Failed to send notification: {str(e)}")


def check_task_notifications():
    """Function to initialize and run task notifications."""
    try:
        notifier = TaskNotifier()
        task_lists = ListManager.get_all_lists()
        notifier.check_notifications(task_lists)
    except Exception as e:
        logging.error(f"Error checking notifications: {str(e)}")
