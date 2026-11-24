from datetime import date

from backend.phase2.models import (
    OneTimeTask,
    PRIORITIES,
    RecurringTask,
)


class MaintenanceScheduler:
    def __init__(self):
        self.staff = {}
        self.tasks = {}

    def add_staff(self, staff):
        if staff.staff_id in self.staff:
            raise ValueError(f"Staff ID {staff.staff_id} already exists.")
        self.staff[staff.staff_id] = staff

    def get_staff(self, staff_id):
        if staff_id not in self.staff:
            raise KeyError(f"Staff member {staff_id} was not found.")
        return self.staff[staff_id]

    def get_all_staff(self):
        return list(self.staff.values())

    def schedule_task(
        self,
        task_id,
        name,
        equipment,
        location,
        interval_days,
        due_date,
        priority,
        assigned_staff_id=None,
    ):
        if task_id in self.tasks:
            raise ValueError(f"Task ID {task_id} already exists.")
        if priority not in PRIORITIES:
            raise ValueError("Invalid priority.")
        if interval_days < 0:
            raise ValueError("Recurrence interval cannot be negative.")
        if assigned_staff_id is not None:
            self.get_staff(assigned_staff_id)

        if interval_days == 0:
            task = OneTimeTask(
                task_id,
                name,
                equipment,
                location,
                due_date,
                priority,
                assigned_staff_id,
            )
        else:
            task = RecurringTask(
                task_id,
                name,
                equipment,
                location,
                interval_days,
                due_date,
                priority,
                assigned_staff_id,
            )

        self.tasks[task_id] = task
        return task

    def get_task(self, task_id):
        if task_id not in self.tasks:
            raise KeyError(f"Task {task_id} was not found.")
        return self.tasks[task_id]

    def get_all_tasks(self):
        return list(self.tasks.values())

    def assign_staff(self, task_id, staff_id):
        task = self.get_task(task_id)
        staff = self.get_staff(staff_id)
        task.assign(staff.staff_id)
        return task

    def complete_task(self, task_id, today=None):
        task = self.get_task(task_id)
        next_due_date = task.complete(today)
        return task, next_due_date

    def get_due_today(self, today=None):
        today = today or date.today()
        return [task for task in self.tasks.values() if task.is_due_today(today)]

    def get_overdue(self, today=None):
        today = today or date.today()
        return [task for task in self.tasks.values() if task.is_overdue(today)]

    def get_upcoming(self, today=None):
        today = today or date.today()
        return [task for task in self.tasks.values() if task.is_upcoming(today)]

    def get_completed(self):
        return [
            task
            for task in self.tasks.values()
            if task.status == "Completed"
        ]

    def get_tasks_for_staff(self, staff_id):
        self.get_staff(staff_id)
        return [
            task
            for task in self.tasks.values()
            if task.assigned_staff_id == staff_id
        ]

    def get_dashboard(self, today=None):
        today = today or date.today()
        return {
            "total": len(self.tasks),
            "due_today": len(self.get_due_today(today)),
            "overdue": len(self.get_overdue(today)),
            "upcoming": len(self.get_upcoming(today)),
            "completed": len(self.get_completed()),
            "assigned": sum(
                task.assigned_staff_id is not None
                for task in self.tasks.values()
            ),
            "unassigned": sum(
                task.assigned_staff_id is None
                for task in self.tasks.values()
            ),
        }
