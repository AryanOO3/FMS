from datetime import date, timedelta


PRIORITIES = ("Low", "Medium", "High", "Critical")
VALID_STATUSES = ("Scheduled", "In Progress", "Completed")


def load_sample_data(reference_today=None):
    """Create sample staff and tasks based on a reference date."""
    today = reference_today or date.today()

    staff = [
        {"staff_id": 1, "name": "Aisha Khan", "role": "Electrical Technician"},
        {"staff_id": 2, "name": "Rahul Mehta", "role": "HVAC Technician"},
        {"staff_id": 3, "name": "Sara D'Souza", "role": "Plumbing Technician"},
        {"staff_id": 4, "name": "Dev Patel", "role": "General Maintenance"},
    ]

    tasks = [
        {
            "task_id": 101,
            "name": "Inspect HVAC filter",
            "equipment": "AHU-1",
            "location": "Mechanical room",
            "interval_days": 30,
            "due_date": today,
            "priority": "Medium",
            "status": "Scheduled",
            "assigned_staff_id": 2,
        },
        {
            "task_id": 102,
            "name": "Emergency light test",
            "equipment": "EL-2",
            "location": "Main block",
            "interval_days": 90,
            "due_date": today - timedelta(days=2),
            "priority": "High",
            "status": "Scheduled",
            "assigned_staff_id": 1,
        },
        {
            "task_id": 103,
            "name": "Water pump inspection",
            "equipment": "WP-1",
            "location": "Utility room",
            "interval_days": 14,
            "due_date": today - timedelta(days=5),
            "priority": "High",
            "status": "Scheduled",
            "assigned_staff_id": 3,
        },
        {
            "task_id": 104,
            "name": "Elevator monthly inspection",
            "equipment": "Lift 3",
            "location": "East wing",
            "interval_days": 30,
            "due_date": today + timedelta(days=15),
            "priority": "High",
            "status": "Scheduled",
            "assigned_staff_id": 4,
        },
        {
            "task_id": 105,
            "name": "Fire alarm panel test",
            "equipment": "FA-1",
            "location": "Security room",
            "interval_days": 90,
            "due_date": today + timedelta(days=6),
            "priority": "Critical",
            "status": "Scheduled",
            "assigned_staff_id": 1,
        },
        {
            "task_id": 106,
            "name": "Replace AC belt",
            "equipment": "AHU-2",
            "location": "Central block",
            "interval_days": 60,
            "due_date": today + timedelta(days=20),
            "priority": "Medium",
            "status": "Scheduled",
            "assigned_staff_id": 2,
        },
        {
            "task_id": 107,
            "name": "Quarterly drain cleaning",
            "equipment": "Drain 4",
            "location": "Canteen",
            "interval_days": 7,
            "due_date": today - timedelta(days=10),
            "priority": "Low",
            "status": "Completed",
            "assigned_staff_id": 3,
        },
        {
            "task_id": 108,
            "name": "Exit sign inspection",
            "equipment": "EX-5",
            "location": "South wing",
            "interval_days": 180,
            "due_date": today - timedelta(days=1),
            "priority": "Medium",
            "status": "Scheduled",
            "assigned_staff_id": None,
        },
        {
            "task_id": 109,
            "name": "Replace corridor bulb",
            "equipment": "CB-12",
            "location": "First floor",
            "interval_days": 0,
            "due_date": today,
            "priority": "Low",
            "status": "Scheduled",
            "assigned_staff_id": 4,
        },
        {
            "task_id": 110,
            "name": "Annual fire extinguisher audit",
            "equipment": "FE-SET",
            "location": "Storage block",
            "interval_days": 365,
            "due_date": today + timedelta(days=41),
            "priority": "Critical",
            "status": "Scheduled",
            "assigned_staff_id": None,
        },
    ]
    return staff, tasks


def print_menu():
    print("\nFacilities Maintenance Scheduler")
    print("=" * 40)
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
    print("0. Exit")


def get_positive_integer(prompt):
    value = input(prompt).strip()
    if not value.isdigit():
        return None
    number = int(value)
    return number if number > 0 else None


def parse_date(prompt):
    value = input(prompt).strip()
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def find_task(tasks, task_id):
    return next((task for task in tasks if task["task_id"] == task_id), None)


def find_staff(staff, staff_id):
    return next((person for person in staff if person["staff_id"] == staff_id), None)


def staff_name(staff, staff_id):
    person = find_staff(staff, staff_id)
    return person["name"] if person else "Unassigned"


def display_staff(staff):
    print("\nStaff")
    print("-" * 55)
    print(f"{'ID':<4} {'Name':<22} {'Role'}")
    for person in staff:
        print(
            f"{person['staff_id']:<4} "
            f"{person['name']:<22} "
            f"{person['role']}"
        )


def display_task_list(tasks, staff, today=None):
    if not tasks:
        print("\nNo tasks found.")
        return

    today = today or date.today()
    print(
        f"\n{'ID':<5} {'Task':<30} {'Due Date':<12} "
        f"{'Priority':<9} {'Status':<12} {'Assigned Staff'}"
    )
    print("-" * 115)

    for task in tasks:
        assigned_name = staff_name(staff, task["assigned_staff_id"])
        status = task["status"]
        if status == "Scheduled" and task["due_date"] < today:
            status = "Overdue"
        elif status == "Scheduled" and task["due_date"] == today:
            status = "Due Today"
        elif status == "Scheduled" and task["due_date"] > today:
            status = "Upcoming"

        print(
            f"{task['task_id']:<5} "
            f"{task['name'][:30]:<30} "
            f"{task['due_date'].isoformat():<12} "
            f"{task['priority']:<9} "
            f"{status:<12} "
            f"{assigned_name}"
        )


def schedule_task(tasks, staff, today=None):
    task_id = get_positive_integer("Task ID (positive integer): ")
    if task_id is None:
        print("Error: Task ID must be a positive integer.")
        return
    if find_task(tasks, task_id):
        print("Error: A task with that ID already exists.")
        return

    name = input("Task name: ").strip()
    equipment = input("Equipment: ").strip()
    location = input("Location: ").strip()
    if not name or not equipment or not location:
        print("Error: Task name, equipment, and location are required.")
        return

    interval_text = input(
        "Recurrence interval in days (0 for a one-time task): "
    ).strip()
    try:
        interval_days = int(interval_text)
    except ValueError:
        print("Error: Recurrence interval must be a whole number.")
        return
    if interval_days < 0:
        print("Error: Recurrence interval cannot be negative.")
        return

    due_date = parse_date("Next due date (YYYY-MM-DD): ")
    if due_date is None:
        print("Error: Use a valid date in YYYY-MM-DD format.")
        return

    print("Priorities: " + ", ".join(PRIORITIES))
    priority = input("Priority: ").strip().title()
    if priority not in PRIORITIES:
        print("Error: Invalid priority.")
        return

    staff_id_text = input(
        "Staff ID (leave blank for unassigned): "
    ).strip()
    staff_id = None
    if staff_id_text:
        if not staff_id_text.isdigit():
            print("Error: Staff ID must be a positive integer.")
            return
        staff_id = int(staff_id_text)
        if find_staff(staff, staff_id) is None:
            print("Error: Staff member was not found.")
            return

    task = {
        "task_id": task_id,
        "name": name,
        "equipment": equipment,
        "location": location,
        "interval_days": interval_days,
        "due_date": due_date,
        "priority": priority,
        "status": "Scheduled",
        "assigned_staff_id": staff_id,
    }
    tasks.append(task)
    print(f"\nSuccess: Task {task_id} '{name}' was scheduled.")
    display_task_list([task], staff, today)


def assign_staff(tasks, staff):
    task_id = get_positive_integer("Task ID: ")
    if task_id is None:
        print("Error: Task ID must be a positive integer.")
        return

    task = find_task(tasks, task_id)
    if task is None:
        print("Error: Task was not found.")
        return

    staff_id = get_positive_integer("Staff ID: ")
    if staff_id is None:
        print("Error: Staff ID must be a positive integer.")
        return

    person = find_staff(staff, staff_id)
    if person is None:
        print("Error: Staff member was not found.")
        return

    task["assigned_staff_id"] = staff_id
    print(
        f"Success: Task {task_id} '{task['name']}' "
        f"was assigned to {person['name']}."
    )


def view_due_today(tasks, staff, today=None):
    today = today or date.today()
    matches = [
        task
        for task in tasks
        if task["status"] == "Scheduled" and task["due_date"] == today
    ]
    display_task_list(matches, staff, today)


def view_overdue(tasks, staff, today=None):
    today = today or date.today()
    matches = [
        task
        for task in tasks
        if task["status"] == "Scheduled" and task["due_date"] < today
    ]
    display_task_list(matches, staff, today)


def view_upcoming(tasks, staff, today=None):
    today = today or date.today()
    matches = [
        task
        for task in tasks
        if task["status"] == "Scheduled" and task["due_date"] > today
    ]
    display_task_list(matches, staff, today)


def view_completed(tasks, staff, today=None):
    today = today or date.today()
    matches = [task for task in tasks if task["status"] == "Completed"]
    display_task_list(matches, staff, today)


def view_tasks_for_staff(tasks, staff, today=None):
    staff_id = get_positive_integer("Staff ID: ")
    if staff_id is None:
        print("Error: Staff ID must be a positive integer.")
        return

    person = find_staff(staff, staff_id)
    if person is None:
        print("Error: Staff member was not found.")
        return

    matches = [
        task for task in tasks if task["assigned_staff_id"] == staff_id
    ]
    print(f"\nTasks assigned to {person['name']}")
    display_task_list(matches, staff, today)


def complete_task(tasks, staff, today=None):
    today = today or date.today()
    task_id = get_positive_integer("Task ID: ")
    if task_id is None:
        print("Error: Task ID must be a positive integer.")
        return

    task = find_task(tasks, task_id)
    if task is None:
        print("Error: Task was not found.")
        return

    if task["status"] == "Completed":
        print("Error: This task is already completed.")
        return

    if task["interval_days"] > 0:
        task["due_date"] = task["due_date"] + timedelta(
            days=task["interval_days"]
        )
        task["status"] = "Scheduled"
        print(
            f"Success: Task {task_id} '{task['name']}' was completed. "
            f"Next due date is {task['due_date'].isoformat()}."
        )
    else:
        task["status"] = "Completed"
        print(
            f"Success: One-time task {task_id} "
            f"'{task['name']}' was completed."
        )


def run_console_app():
    staff, tasks = load_sample_data()
    today = date.today()

    while True:
        print_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            schedule_task(tasks, staff, today)
        elif choice == "2":
            assign_staff(tasks, staff)
        elif choice == "3":
            display_task_list(tasks, staff, today)
        elif choice == "4":
            view_due_today(tasks, staff, today)
        elif choice == "5":
            view_overdue(tasks, staff, today)
        elif choice == "6":
            view_upcoming(tasks, staff, today)
        elif choice == "7":
            view_completed(tasks, staff, today)
        elif choice == "8":
            view_tasks_for_staff(tasks, staff, today)
        elif choice == "9":
            complete_task(tasks, staff, today)
        elif choice == "10":
            display_staff(staff)
        elif choice == "0":
            print("Exiting Facilities Maintenance Scheduler.")
            break
        else:
            print("Error: Invalid menu selection.")
