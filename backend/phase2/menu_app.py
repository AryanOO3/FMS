from datetime import date

from backend.phase2.models import PRIORITIES


class MaintenanceMenuApp:
    def __init__(self, scheduler, today=None):
        self.scheduler = scheduler
        self.today = today or date.today()

    @staticmethod
    def get_positive_integer(prompt):
        value = input(prompt).strip()
        if not value.isdigit():
            return None
        number = int(value)
        return number if number > 0 else None

    @staticmethod
    def parse_date(prompt):
        value = input(prompt).strip()
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None

    def print_menu(self):
        print("\nFacilities Maintenance Scheduler - Phase 2")
        print("=" * 48)
        print("1. Schedule a maintenance task")
        print("2. Assign or reassign staff")
        print("3. View all tasks")
        print("4. View due today")
        print("5. View overdue tasks")
        print("6. View upcoming tasks")
        print("7. View completed tasks")
        print("8. View tasks for staff")
        print("9. Complete a task")
        print("10. View staff")
        print("11. View dashboard summary")
        print("0. Exit")

    def display_staff(self):
        print("\nStaff")
        print("-" * 55)
        print(f"{'ID':<4} {'Name':<22} {'Role'}")
        for staff in self.scheduler.get_all_staff():
            print(f"{staff.staff_id:<4} {staff.name:<22} {staff.role}")

    def display_tasks(self, tasks):
        if not tasks:
            print("\nNo tasks found.")
            return

        print(
            f"\n{'ID':<5} {'Task':<31} {'Equipment':<12} {'Due Date':<12} "
            f"{'Priority':<9} {'Status':<12} {'Assigned Staff'}"
        )
        print("-" * 125)

        for task in tasks:
            if task.assigned_staff_id is None:
                assigned_name = "Unassigned"
            else:
                try:
                    assigned_name = self.scheduler.get_staff(
                        task.assigned_staff_id
                    ).name
                except KeyError:
                    assigned_name = "Unknown"

            print(
                f"{task.task_id:<5} "
                f"{task.name[:31]:<31} "
                f"{task.equipment[:12]:<12} "
                f"{task.due_date.isoformat():<12} "
                f"{task.priority:<9} "
                f"{task.display_status(self.today):<12} "
                f"{assigned_name}"
            )

    def schedule_task(self):
        task_id = self.get_positive_integer("Task ID (positive integer): ")
        if task_id is None:
            print("Error: Task ID must be a positive integer.")
            return

        name = input("Task name: ").strip()
        equipment = input("Equipment: ").strip()
        location = input("Location: ").strip()
        if not name or not equipment or not location:
            print("Error: Task name, equipment, and location are required.")
            return

        try:
            interval_days = int(
                input("Recurrence interval in days (0 for one-time): ").strip()
            )
        except ValueError:
            print("Error: Recurrence interval must be a whole number.")
            return

        due_date = self.parse_date("Next due date (YYYY-MM-DD): ")
        if due_date is None:
            print("Error: Use a valid date in YYYY-MM-DD format.")
            return

        print("Priorities: " + ", ".join(PRIORITIES))
        priority = input("Priority: ").strip().title()

        staff_id_text = input(
            "Staff ID (leave blank for unassigned): "
        ).strip()
        staff_id = None
        if staff_id_text:
            if not staff_id_text.isdigit():
                print("Error: Staff ID must be a positive integer.")
                return
            staff_id = int(staff_id_text)

        try:
            task = self.scheduler.schedule_task(
                task_id,
                name,
                equipment,
                location,
                interval_days,
                due_date,
                priority,
                staff_id,
            )
        except (ValueError, KeyError) as error:
            print(f"Error: {error}")
            return

        print(f"\nSuccess: Task {task.task_id} '{task.name}' was scheduled.")
        self.display_tasks([task])

    def assign_staff(self):
        task_id = self.get_positive_integer("Task ID: ")
        if task_id is None:
            print("Error: Task ID must be a positive integer.")
            return

        staff_id = self.get_positive_integer("Staff ID: ")
        if staff_id is None:
            print("Error: Staff ID must be a positive integer.")
            return

        try:
            task = self.scheduler.assign_staff(task_id, staff_id)
            staff = self.scheduler.get_staff(staff_id)
        except (KeyError, ValueError) as error:
            print(f"Error: {error}")
            return

        print(
            f"Success: Task {task.task_id} '{task.name}' "
            f"was assigned to {staff.name}."
        )

    def complete_task(self):
        task_id = self.get_positive_integer("Task ID: ")
        if task_id is None:
            print("Error: Task ID must be a positive integer.")
            return

        try:
            task, next_due_date = self.scheduler.complete_task(
                task_id, self.today
            )
        except (KeyError, ValueError) as error:
            print(f"Error: {error}")
            return

        if task.status == "Scheduled":
            print(
                f"Success: Task {task.task_id} '{task.name}' was completed. "
                f"Next due date is {next_due_date.isoformat()}."
            )
        else:
            print(
                f"Success: One-time task {task.task_id} "
                f"'{task.name}' was completed."
            )

    def view_tasks_for_staff(self):
        staff_id = self.get_positive_integer("Staff ID: ")
        if staff_id is None:
            print("Error: Staff ID must be a positive integer.")
            return

        try:
            staff = self.scheduler.get_staff(staff_id)
            tasks = self.scheduler.get_tasks_for_staff(staff_id)
        except KeyError as error:
            print(f"Error: {error}")
            return

        print(f"\nTasks assigned to {staff.name}")
        self.display_tasks(tasks)

    def view_dashboard(self):
        dashboard = self.scheduler.get_dashboard(self.today)
        print("\nDashboard Summary")
        print("-" * 40)
        for label, value in dashboard.items():
            print(f"{label.replace('_', ' ').title():<15}: {value}")

    def run(self):
        while True:
            self.print_menu()
            choice = input("Select an option: ").strip()

            if choice == "1":
                self.schedule_task()
            elif choice == "2":
                self.assign_staff()
            elif choice == "3":
                self.display_tasks(self.scheduler.get_all_tasks())
            elif choice == "4":
                self.display_tasks(self.scheduler.get_due_today(self.today))
            elif choice == "5":
                self.display_tasks(self.scheduler.get_overdue(self.today))
            elif choice == "6":
                self.display_tasks(self.scheduler.get_upcoming(self.today))
            elif choice == "7":
                self.display_tasks(self.scheduler.get_completed())
            elif choice == "8":
                self.view_tasks_for_staff()
            elif choice == "9":
                self.complete_task()
            elif choice == "10":
                self.display_staff()
            elif choice == "11":
                self.view_dashboard()
            elif choice == "0":
                print("Exiting Facilities Maintenance Scheduler.")
                break
            else:
                print("Error: Invalid menu selection.")
