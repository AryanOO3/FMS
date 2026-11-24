from datetime import date, timedelta


PRIORITIES = ("Low", "Medium", "High", "Critical")
VALID_STATUSES = ("Scheduled", "In Progress", "Completed")


class Staff:
    def __init__(self, staff_id, name, role):
        self.staff_id = staff_id
        self.name = name
        self.role = role

    def __str__(self):
        return f"{self.staff_id} - {self.name} ({self.role})"


class MaintenanceTask:
    def __init__(
        self,
        task_id,
        name,
        equipment,
        location,
        due_date,
        priority,
        assigned_staff_id=None,
        status="Scheduled",
    ):
        self.task_id = task_id
        self.name = name
        self.equipment = equipment
        self.location = location
        self.due_date = due_date
        self.priority = priority
        self.assigned_staff_id = assigned_staff_id
        self.status = status

    def assign(self, staff_id):
        self.assigned_staff_id = staff_id

    def is_due_today(self, today):
        return self.status == "Scheduled" and self.due_date == today

    def is_overdue(self, today):
        return self.status == "Scheduled" and self.due_date < today

    def is_upcoming(self, today):
        return self.status == "Scheduled" and self.due_date > today

    def complete(self, today=None):
        raise NotImplementedError

    def display_status(self, today):
        if self.status == "Completed":
            return "Completed"
        if self.is_overdue(today):
            return "Overdue"
        if self.is_due_today(today):
            return "Due Today"
        if self.is_upcoming(today):
            return "Upcoming"
        return self.status

    def __str__(self):
        staff = str(self.assigned_staff_id or "Unassigned")
        return (
            f"{self.task_id} | {self.name} | {self.equipment} | "
            f"{self.location} | Due {self.due_date.isoformat()} | "
            f"{self.priority} | {self.status} | Staff {staff}"
        )


class RecurringTask(MaintenanceTask):
    def __init__(
        self,
        task_id,
        name,
        equipment,
        location,
        interval_days,
        due_date,
        priority,
        assigned_staff_id=None,
        status="Scheduled",
    ):
        super().__init__(
            task_id,
            name,
            equipment,
            location,
            due_date,
            priority,
            assigned_staff_id,
            status,
        )
        self.interval_days = interval_days

    def complete(self, today=None):
        if self.status == "Completed":
            raise ValueError("This task is already completed.")
        self.due_date += timedelta(days=self.interval_days)
        self.status = "Scheduled"
        return self.due_date


class OneTimeTask(MaintenanceTask):
    def __init__(
        self,
        task_id,
        name,
        equipment,
        location,
        due_date,
        priority,
        assigned_staff_id=None,
        status="Scheduled",
    ):
        super().__init__(
            task_id,
            name,
            equipment,
            location,
            due_date,
            priority,
            assigned_staff_id,
            status,
        )
        self.interval_days = 0

    def complete(self, today=None):
        if self.status == "Completed":
            raise ValueError("This task is already completed.")
        self.status = "Completed"
        return self.due_date
