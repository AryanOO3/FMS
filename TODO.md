# Facilities Maintenance Scheduler

## Complete Phase-by-Phase Project Guide

This repository will contain the implementation of a **Facilities Maintenance Scheduler**. The application helps staff schedule routine equipment maintenance, assign employees to work, track the next due date, and identify jobs that are due today or overdue.

The project must remain based on the same core concept in all four phases:

1. Define recurring or one-time maintenance tasks.
2. Assign a staff member to a task.
3. View due-today and overdue jobs.
4. Complete tasks and update recurring task due dates.
5. Demonstrate every operation using sample data and no live institutional systems.

Do not replace the core project with an unrelated application in a later phase. Preserve the underlying entities, operations, terminology, and behavior across all phases.

---

## Table of Contents

1. [Project Objectives](#1-project-objectives)
2. [Agreed Data and Domain Rules](#2-agreed-data-and-domain-rules)
3. [Core Entities](#3-core-entities)
4. [Suggested Final Project Structure](#4-suggested-final-project-structure)
5. [Team Task Split and Workflow](#5-team-task-split-and-workflow)
6. [Phase 0: Project Setup](#6-phase-0-project-setup)
7. [Phase 1: Procedural Programming](#7-phase-1-procedural-programming)
8. [Phase 2: Object-Oriented Programming](#8-phase-2-object-oriented-programming)
9. [Phase 3: Error Handling and Testing](#9-phase-3-error-handling-and-testing)
10. [Phase 4: Flask Browser Front End](#10-phase-4-flask-browser-front-end)
11. [Cross-Phase Test Matrix](#11-cross-phase-test-matrix)
12. [Sample Data](#12-sample-data)
13. [Expected Console Menu](#13-expected-console-menu)
14. [Expected Web Routes and Pages](#14-expected-web-routes-and-pages)
15. [Data State and Transition Rules](#15-data-state-and-transition-rules)
16. [README and Submission Requirements](#16-readme-and-submission-requirements)
17. [Verification Checklists](#17-verification-checklists)
18. [Final Demonstration Script](#18-final-demonstration-script)
19. [Phase Dependencies](#19-phase-dependencies)
20. [Optional Enhancements](#20-optional-enhancements)
21. [Common Mistakes to Avoid](#21-common-mistakes-to-avoid)

---

## 1. Project Objectives

The project demonstrates the following academic concepts:

- Procedural decomposition using functions.
- Loops, conditionals, and collection-based data processing.
- Object-oriented design using classes, composition, and appropriate inheritance.
- Input validation and controlled error handling.
- Test design using normal, boundary, and failure cases.
- Flask routing, HTML templates, POST forms, redirects, and flash messages.
- A repeatable software development process across four phases.

The final application should let a user answer these questions:

- What maintenance work is scheduled?
- Which job is due today?
- Which jobs are overdue?
- Which jobs are upcoming?
- Which staff member is assigned to a job?
- What work has been completed?
- When is a recurring task next due?

The project does not need to connect to a real building-management system, user account system, payroll system, HR database, or institutional service.

---

## 2. Agreed Data and Domain Rules

The team should agree on these rules before implementation. After agreement, use the rules consistently in every phase.

### Dates

- Store dates using Python `datetime.date`.
- Accept and display ISO date strings in `YYYY-MM-DD` format.
- Parse values with `datetime.strptime(value, "%Y-%m-%d").date()` or `date.fromisoformat(value)`.
- Never compare due dates using an unparsed string.
- Use the injected or passed `today` date in tests instead of relying only on `date.today()`.
- Overdue means `due_date < today`.
- Due today means `due_date == today`.
- Upcoming means `due_date > today`.

### IDs

- Task IDs and staff IDs must be positive integers.
- IDs must be unique within their entity type.
- The system should not generate a duplicate ID.
- Do not reuse an ID after a record is removed.
- If removal is not implemented, do not reset ID counters between operations.
- IDs should be displayed clearly in tables and console output.
- If a string ID is accepted for an HTML route, convert it to an integer before checking the scheduler.

### Text Fields

- Task name is required.
- Equipment or location is required.
- Staff name is required.
- Staff role is required.
- Text values must not be empty or whitespace-only.
- Strip leading and trailing whitespace.
- Avoid silently truncating text.
- Task names and staff names may contain spaces.
- Case sensitivity for duplicate task names is not required unless the team documents a rule.

### Recurrence

- Recurrence is measured in whole days.
- The accepted interval is an integer greater than zero.
- Suggested limits:
  - Minimum: 1 day.
  - Maximum: 3650 days.
- The team must document an upper limit if one is enforced.
- A fixed due date may also be used for a one-time task.
- Recurrence applies to completed recurring tasks.
- Completing a recurring task should move the next due date forward by the recurrence interval.
- If the completion date is later than the old due date, decide whether the next date is based on the old due date or the completion date. Document the chosen rule.

A simple implementation rule is:

```text
next_due_date = previous_due_date + recurrence_interval
```

This keeps recurring schedules mathematically consistent and avoids losing missed occurrences. Do not implement this in route functions or menu input code; put it in the task or scheduler.

### Priority

Use one documented set, such as:

- `Low`
- `Medium`
- `High`
- `Critical`

Do not accept free-form priority values unless the team intentionally allows them. Keep the same allowed values in console input and Flask forms.

### Status

Use one documented set, such as:

- `Scheduled`
- `In Progress`
- `Completed`

The status `Overdue` can be calculated at runtime rather than stored. If stored, ensure it cannot become stale.

For a simple implementation:

- Store status as `Scheduled` or `Completed`.
- Determine overdue based on due date and current date.
- Display combined status such as `Overdue (Scheduled)`.

This prevents overdue status from becoming incorrect after a date changes.

### Assignment

- A task may have zero or one assigned staff member.
- A staff member may have many assigned tasks.
- Assignment must reference an existing task and existing staff.
- Reassignment replaces the old staff reference.
- Clearing an assignment may be implemented as an optional feature.
- Duplicate assignment of the same staff member to the same task does not create a second assignment.

### Sample Data

- The application must work immediately after startup.
- Do not require a database migration or live service.
- Provide at least four staff members.
- Provide at least eight maintenance tasks.
- Include:
  - One due-today task.
  - Two or more overdue tasks.
  - Two or more upcoming tasks.
  - One or more completed tasks.
  - One or more assigned tasks.
  - One or more unassigned tasks.
  - Recurring tasks with several interval lengths.

---

## 3. Core Entities

## 3.1 Staff

A staff object or record should contain:

- `staff_id`
- `name`
- `role`
- Optional skill/specialty
- Optional email or phone

Recommended console display:

```text
ID | Name | Role
1  | Aisha Khan | Electrician
2  | Rahul Mehta | HVAC Technician
3  | Sara D'Souza | Plumbing Technician
4  | Dev Patel | General Maintenance
```

Sample staff rules:

- Staff ID 1 may be assigned to electrical jobs.
- Staff ID 2 may be assigned to HVAC jobs.
- Staff ID 3 may be assigned to plumbing jobs.
- Staff ID 4 may handle general building tasks.
- Skill matching is optional and does not need to block assignment unless explicitly implemented.

### Staff Responsibilities

- Represent a staff member.
- Expose a readable display format.
- Allow the scheduler to calculate assigned jobs.
- Prevent duplicate staff IDs.
- Keep names and roles in a valid state.

Do not put menu input or Flask request handling inside the Staff class.

---

## 3.2 MaintenanceTask

A maintenance task or job should contain:

- `task_id`
- `name`
- `equipment`
- `location`
- `interval_days`
- `due_date`
- `priority`
- `status`
- `assigned_staff_id`

Optional fields:

- `description`
- `notes`
- `completed_date`
- `created_date`

Task example:

```text
Task ID: 101
Name: Fire alarm quarterly test
Equipment: Fire alarm panel
Location: Main block, first floor
Interval: 90 days
Next due date: 2026-12-01
Priority: High
Status: Scheduled
Assigned staff: 1
```

### MaintenanceTask Responsibilities

- Store task data.
- Validate task field values.
- Report whether the task is due today.
- Report whether the task is overdue.
- Report whether the task is upcoming.
- Display a readable row or detail view.
- Complete itself or delegate completion behavior to the scheduler.

Keep database, console menu, and Flask logic outside the basic task model when practical.

---

## 3.3 RecurringTask

A recurring task may inherit from `MaintenanceTask` or be represented by a `recurring` flag.

If inheritance is used:

```text
MaintenanceTask
  - task_id
  - name
  - equipment
  - location
  - due_date
  - priority
  - status

RecurringTask(MaintenanceTask)
  - interval_days
  - completion behavior
```

If one-time tasks are included:

- Repetition interval may be `None`.
- Completing a one-time task may set status to `Completed`.
- Completing a recurring task may set status to `Scheduled` and advance the due date.

Do not create an inheritance hierarchy with multiple unrelated subclasses solely to demonstrate inheritance.

---

## 3.4 MaintenanceScheduler

The scheduler is the central service for Phase 2 onward.

Suggested methods:

```text
add_staff(staff)
get_staff(staff_id)
get_all_staff()

schedule_task(...)
get_task(task_id)
get_all_tasks()

assign_staff(task_id, staff_id)
clear_assignment(task_id)
complete_task(task_id, today=None)

get_due_today(today=None)
get_overdue(today=None)
get_upcoming(today=None)
get_completed()
get_unassigned()
get_tasks_for_staff(staff_id)
get_dashboard(today=None)
```

### Scheduler Responsibilities

- Store lists or dictionaries of staff and tasks.
- Coordinate interactions between entities.
- Validate references such as task and staff IDs.
- Raise meaningful exceptions for invalid operations.
- Prevent duplicate IDs.
- Maintain assignment consistency.
- Filter tasks.
- Complete recurring tasks.
- Provide the dashboard summary.
- Supply data to console and Flask interfaces.

The scheduler should not use `input()`.

The scheduler should not directly render HTML or print menus.

It may return filtered lists or raise exceptions.

---

## 3.5 MaintenanceApp or MenuApp

For Phase 1, the menu controller may simply be a set of functions in `main.py`.

For Phase 2 onward, use a menu/application class.

Suggested responsibilities:

- Print menu options.
- Read console input.
- Convert string input to numbers and dates.
- Call scheduler methods.
- Display results.
- Catch expected application exceptions.
- Return to the menu after errors.
- Continue until the user exits.

Do not place assignment rules, recurring date calculations, duplicate checks, or filtering logic directly in menu input code.

---

## 4. Suggested Final Project Structure

The exact structure may vary, but this is recommended:

```text
FMS/
  TODO.md
  README.md
  requirements.txt
  main.py
  phase1/
    procedural_scheduler.py
  phase2/
    models.py
    scheduler.py
    menu_app.py
  phase3/
    exceptions.py
    validation.py
    tests/
  phase4/
    app.py
    models/
    templates/
      base.html
      dashboard.html
      tasks.html
      task_detail.html
      task_form.html
      assign_form.html
      staff.html
      jobs.html
    static/
      style.css
    tests/
  tests/
    test_scheduler.py
    test_validation.py
    test_routes.py
  sample_data/
    staff.py
    tasks.py
```

A team may use only a small number of these files. The key is to keep responsibilities clear.

### Structure Rules

- Do not place every class in `app.py`.
- Do not put HTML logic into scheduler classes.
- Do not put console input into task models.
- Do not duplicate sample data in every module.
- Create one source of truth for allowed statuses and priorities.
- Create one source of truth for sample staff and tasks.
- Keep Flask route functions thin.

---

## 5. Team Task Split and Workflow

With teams of four or five students, divide work without creating isolated incompatible implementations.

Possible roles:

- **Data/model developer**
  - Staff and task classes.
  - Data relationships.
- **Scheduler/domain developer**
  - Scheduling, assignment, filtering, and recurring logic.
- **Validation/testing developer**
  - Exceptions, validation, boundary tests, and failure tests.
- **Console/UI developer**
  - Menus and console formatting.
- **Flask/UI developer**
  - Routes, templates, forms, and browser testing.

For a five-person team:

- One person can lead integration and documentation.
- Everyone should understand and be able to explain the scheduler.
- Final testing should not be assigned to only one person.

### Recommended Workflow

1. Agree on names, fields, data types, and status values.
2. Complete the project setup.
3. Implement and verify Phase 1.
4. Freeze a working Phase 1 baseline.
5. Refactor Phase 1 only as much as needed for Phase 2.
6. Verify Phase 2 behavior before adding validation.
7. Add exceptions and tests in Phase 3.
8. Verify Phase 3 behavior before starting Flask.
9. Connect Flask to the Phase 3 classes.
10. Test routes and browser pages.
11. Run the final end-to-end demonstration.

Do not rewrite the project from scratch for each phase.

---

## 6. Phase 0: Project Setup

**Status:** Complete for Phase 1

### 6.1 Setup Checklist

- [x] Create a project folder.
- [ ] Install Python 3.10 or later if available.
- [ ] Create and activate a virtual environment.
- [ ] Create `requirements.txt` (required for Phase 4).
- [ ] Add Flask and test dependencies as needed.
- [ ] Add team names and student IDs if required by the rubric.
- [x] Create `README.md`.
- [x] Agree on naming conventions.
- [x] Agree on date, status, priority, ID, and recurrence rules.
- [x] Add sample staff and tasks.
- [x] Decide whether to use `unittest` or `pytest`.
- [x] Document commands for running the console app and tests.

### 6.2 Initial Project Decisions

Document:

- Due date format.
- Priority values.
- Status values.
- Recurrence interval limits.
- Whether a completed recurring task remains scheduled or is deleted.
- Whether reassignment is allowed.
- Whether staff can be unassigned.
- Whether task IDs can be entered or are generated.
- Whether dates in the past are accepted.
- Reference-date behavior for tests.

If these decisions are not documented, later team members may implement different behavior.

### 6.3 Environment Setup

Example:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The requirements file may contain:

```text
Flask>=3.0,<4.0
pytest>=8.0,<9.0
```

The exact versions may be adjusted, but the file must allow the project to be reproduced.

### 6.4 Project Setup Acceptance

- [x] A teammate can clone or copy the project and run setup instructions.
- [x] No secret credentials are needed.
- [x] No external database is required.
- [x] Sample data starts automatically.
- [x] The test command is documented.

---

## 7. Phase 1: Procedural Programming

**Status:** Complete

## 7.1 Phase 1 Objective

Build a menu-driven console program using:

- Functions.
- Lists and dictionaries.
- Loops.
- Conditional statements.
- String operations.
- Numeric operations.
- Date operations.
- Separate input and display functions.

Do not use classes in Phase 1 unless only a simple function-based version is later refactored.

## 7.2 Required Core Operation 1: Schedule a Task

The program must ask for or accept:

- Task ID, or generate it automatically.
- Task name.
- Equipment or facility area.
- Location or building.
- Recurrence interval.
- Next due date.
- Priority.
- Optional staff ID.

The task dictionary or record should resemble:

```python
{
    "task_id": 101,
    "name": "Inspect HVAC filter",
    "equipment": "AHU-1",
    "location": "Mechanical room",
    "interval_days": 30,
    "due_date": "2026-11-20",
    "priority": "Medium",
    "status": "Scheduled",
    "assigned_staff_id": None,
}
```

For Phase 1, if an invalid value is entered, display an error and return to the menu. Full exception handling belongs in Phase 3.

### Schedule Behavior

- Generate the next available task ID or accept a proposed ID.
- Store the task in a list.
- Display a success message.
- Show the created task details.
- Preserve tasks for the remainder of the console session.

## 7.3 Required Core Operation 2: Assign Staff

The user enters:

- Task ID.
- Staff ID.

The program should:

- Search for the task.
- Search for the staff member.
- Store the staff ID in the task.
- Display the assigned staff name and task name.
- Allow reassignment.
- Display a clear message if a record is missing.

Assignment should not create a separate, disconnected assignment list if the task can directly store `assigned_staff_id`.

## 7.4 Required Core Operation 3: View Jobs

The program should support at least:

- All jobs.
- Due today.
- Overdue jobs.
- Upcoming jobs.
- Completed jobs.
- Jobs assigned to a staff member.

Due and overdue calculations must use actual date objects.

Example output:

```text
ID  | Task                         | Equipment | Due Date   | Priority | Status
102 | Emergency light test         | EL-2      | 2026-11-18 | High     | Overdue
101 | Inspect HVAC filter          | AHU-1     | 2026-11-20 | Medium   | Due Today
104 | Elevator monthly inspection  | Lift 3    | 2026-12-05 | High     | Upcoming
```

## 7.5 Additional Required Menu Operations

Include:

- View all staff.
- Complete a task.
- Exit.

Completing a task should:

- Find it by ID.
- If already completed, display a clear message.
- If recurring, add `interval_days` to `due_date`.
- Keep status as `Scheduled`.
- If one-time, set status to `Completed`.
- Preserve the task and assignment.
- Display the updated due date.

## 7.6 Suggested Phase 1 Functions

At minimum:

```text
print_menu()
get_menu_choice()
add_task(tasks, staff)
assign_staff(tasks, staff)
complete_task(tasks, today)
view_all_tasks(tasks)
view_due_today(tasks, today)
view_overdue(tasks, today)
view_upcoming(tasks, today)
view_completed(tasks)
view_staff_jobs(tasks, staff)
find_task(tasks, task_id)
find_staff(staff, staff_id)
display_task(task)
display_task_list(tasks)
load_sample_data()
main()
```

Functions should perform one clear type of work.

For example, do not combine:

- Asking for input.
- Assigning staff.
- Printing all tasks.
- Calculating overdue status.

Instead, split these responsibilities across separate functions.

## 7.7 Phase 1 Testing

Even in the procedural phase, run manual tests:

- Start the program with sample data.
- Select every menu choice.
- Schedule a new task.
- Schedule a task with no assigned staff.
- Assign one staff member.
- Reassign a task.
- View due today.
- View overdue.
- View upcoming.
- Complete a recurring task.
- Attempt to exit.

Record the input and observed output to identify bugs before refactoring.

## 7.8 Phase 1 Acceptance Checklist

- [ ] Program runs as a standalone Python script.
- [ ] Main menu loops until the user exits.
- [ ] Three core operations are demonstrable.
- [ ] Sample data is loaded automatically.
- [ ] Functions are clearly named.
- [ ] Loops and conditionals are visible.
- [ ] Date objects are used for date classification.
- [ ] Completing recurring tasks updates their due dates.
- [ ] Output is readable.
- [ ] No database or external service is required.

---

## 8. Phase 2: Object-Oriented Programming

## 8.1 Phase 2 Objective

Refactor Phase 1 into classes. Preserve the same menu and operations.

Do not add a second and inconsistent application just to satisfy OOP.

The console menu should call a scheduler object, not manipulate task dictionaries directly.

## 8.2 Suggested Staff Class

```python
class Staff:
    def __init__(self, staff_id, name, role):
        self.staff_id = staff_id
        self.name = name
        self.role = role

    def __str__(self):
        return f"{self.staff_id} - {self.name} ({self.role})"
```

Fields may be properties rather than public attributes.

The class can include validation later in Phase 3.

## 8.3 Suggested MaintenanceTask Class

Responsibilities:

- Store task details.
- Check due status.
- Format its display.
- Complete itself or expose a completion method.

Example method names:

```text
is_due_today(today)
is_overdue(today)
is_upcoming(today)
complete(today)
assign(staff)
display_summary()
```

Avoid giving every model direct access to the console.

## 8.4 Suggested RecurringTask Inheritance

```python
class RecurringTask(MaintenanceTask):
    def __init__(..., interval_days, ...):
        super().__init__(...)
        self.interval_days = interval_days

    def complete(self, today=None):
        self.due_date += timedelta(days=self.interval_days)
        self.status = "Scheduled"
```

For a one-time task, inheritance may be omitted.

Inheritance is useful if a task-specific completion or display behavior differs.

If all task types behave identically except for interval handling, an `interval_days` or `recurring` field may be cleaner than extra subclasses.

## 8.5 Suggested MaintenanceScheduler Class

Store objects:

```python
class MaintenanceScheduler:
    def __init__(self):
        self.staff = {}
        self.tasks = {}
```

Using dictionaries keyed by ID makes lookup efficient and naturally prevents duplicate IDs.

Do not mix dictionaries and objects inconsistently.

## 8.6 Example Scheduler API

```text
schedule_task(
    task_id,
    name,
    equipment,
    location,
    interval_days,
    due_date,
    priority,
)

assign_staff(task_id, staff_id)
complete_task(task_id, today)
get_due_today(today)
get_overdue(today)
get_upcoming(today)
get_tasks_for_staff(staff_id)
get_completed_tasks()
get_task(task_id)
get_staff(staff_id)
```

The scheduler should return objects or lists.

The menu can format objects for display.

## 8.7 Composition Requirement

The scheduler must compose staff and task objects.

It may contain:

```text
self.staff
self.tasks
```

Each task may contain:

```text
self.assigned_staff_id
```

or:

```text
self.assigned_staff
```

An object reference is preferable to storing a duplicate staff name. Use one approach consistently.

## 8.8 Inheritance Requirement

The team must use inheritance or explain in the report why composition alone is a better fit.

The task explicitly allows composition or inheritance where it fits. A simple, justified design is preferred over fake inheritance.

Suitable inheritance examples:

- `RecurringTask(MaintenanceTask)`.
- `OneTimeTask(MaintenanceTask)`.

Unsuitable inheritance examples:

- `HVACTask`, `ElectricalTask`, and `PlumbingTask` without meaningfully different behavior.
- `TaskWithPriority` for field storage only.

## 8.9 Encapsulation

Use private attributes or properties where appropriate.

Examples:

- Prevent negative recurrence intervals.
- Prevent changing task ID after creation.
- Format assigned staff consistently.
- Update status only through methods.

Do not expose dozens of public mutable fields in every class.

## 8.10 MenuApp or App Class

The menu app should:

- Hold a `MaintenanceScheduler`.
- Read console input.
- Convert string values to dates and integers.
- Call scheduler methods.
- Catch expected exceptions.
- Print lists and messages.
- Repeat until exit.

The menu app should not calculate whether a task is overdue.

That calculation belongs in `MaintenanceTask` or `MaintenanceScheduler`.

## 8.11 Phase 2 Acceptance Checklist

- [ ] Phase 1 behavior is preserved.
- [ ] Domain logic is moved into classes.
- [ ] Scheduler and task responsibilities are distinct.
- [ ] Composition is used.
- [ ] Inheritance is used only where justified.
- [ ] The menu does not manipulate internal dictionaries directly.
- [ ] Task status and due dates are updated through methods.
- [ ] Each staff and task object has a clear responsibility.
- [ ] The console program still has sample data.
- [ ] The code can be reused by later Flask routes.

---

## 9. Phase 3: Error Handling and Testing

## 9.1 Phase 3 Objective

Add validation and controlled exceptions to the Phase 2 implementation.

The program must handle expected failures and continue running.

## 9.2 Custom Exceptions

Suggested exception hierarchy:

```text
SchedulerError
  ValidationError
  RecordNotFoundError
  DuplicateRecordError
  InvalidAssignmentError
  InvalidTaskStateError
```

Not every application needs all of these.

The exceptions should carry useful messages. They should not contain HTML.

Example method behavior:

```text
if task_id not in tasks:
    raise RecordNotFoundError("Task 999 was not found")
```

## 9.3 Required Validation Checks

### Task Name

- Required.
- Strip whitespace.
- Reject an empty or whitespace-only value.
- Reject `None`.

### Equipment

- Required.
- Reject blank value.

### Location

- Required in the final design.
- Reject blank value.

### Due Date

- Parse exact `YYYY-MM-DD`.
- Reject date strings that do not match.
- Reject missing values.
- Optionally reject past dates according to documented team rules.
- Accept today only if the team explicitly allows scheduling for today.
- If past dates are allowed, overdue classification must still work.

### Recurrence Interval

- Convert from a string only after checking.
- Reject negative values.
- Reject zero.
- Reject decimal values.
- Reject nonnumeric values.
- Reject values above the team maximum.

### Priority

- Accept only allowed values.
- Normalize case consistently if desired.
- Do not silently default an invalid priority.

### Status

- Accept only `Scheduled`, `In Progress`, or `Completed`.
- Do not allow arbitrary status strings.

### IDs

- Convert to positive integers.
- Reject zero.
- Reject negative values.
- Reject strings containing letters.
- Reject duplicate task IDs.
- Reject duplicate staff IDs.

### Assignment

- Check task existence first.
- Check staff existence second.
- If either is missing, raise a descriptive error.
- Do not partially update the task.

### Completion

- Check that task exists.
- Reject completion of an already completed task.
- For recurring tasks, calculate the next date only after validation succeeds.
- Do not lose the staff assignment.

### Menu Input

- Reject menu values outside the defined range.
- Reprint the menu after invalid input.
- Reject blank input.
- Convert input in a safe try block.

## 9.4 Atomic Updates

An invalid operation must not partially modify state.

For assignment:

1. Validate task.
2. Validate staff.
3. Update assignment.

For task creation:

1. Validate all fields.
2. Check duplicate ID.
3. Create and add the task.

For completion:

1. Validate task.
2. Validate state.
3. Calculate next date.
4. Update status and date.

Do not modify one field before discovering another field is invalid.

## 9.5 Normal Case Tests

- Add a valid scheduled task.
- Add a valid recurring task.
- Assign a valid staff member.
- Reassign to another valid staff member.
- Complete a valid recurring task.
- Complete a valid one-time task.
- View due today.
- View overdue.
- View upcoming.
- View completed.
- View tasks for a valid staff member.
- Load sample data.

## 9.6 Boundary Case Tests

- Due date exactly today.
- Due date one day before today.
- Due date one day after today.
- Recurrence interval exactly 1 day.
- Recurrence interval exactly the accepted maximum.
- Priority at the lowest and highest accepted options.
- Valid empty optional description.
- Minimum positive staff and task ID.
- Task with no assignment.
- Assignment list for staff with no jobs.

## 9.7 Failure Case Tests

- Duplicate task ID.
- Duplicate staff ID.
- Missing task ID.
- Missing staff ID.
- Negative task ID.
- Zero task ID.
- Blank task name.
- Blank staff name.
- Blank equipment.
- Invalid date format.
- Impossible date such as `2026-02-30`.
- Missing due date.
- Recurrence interval zero.
- Recurrence interval negative.
- Recurrence interval decimal.
- Recurrence interval text.
- Invalid priority.
- Invalid status.
- Invalid assignment.
- Completion of nonexistent task.
- Completion of completed task.
- Invalid menu selection.
- Blank menu input.
- Invalid staff filter.

## 9.8 Testing Approach

If using `pytest`:

```text
pytest -v
```

If using `unittest`:

```text
python -m unittest discover -s tests -v
```

The final README must contain the exact command that works in the project environment.

## 9.9 Suggested Test Files

```text
tests/test_staff.py
tests/test_maintenance_task.py
tests/test_scheduler.py
tests/test_validation.py
tests/test_menu_error_handling.py
tests/test_sample_data.py
```

## 9.10 Example Assertion Areas

Tests should verify:

- Object properties.
- Duplicate detection.
- Missing-record errors.
- Date classification.
- Assignment behavior.
- Recurring completion behavior.
- One-time completion behavior.
- Status changes.
- IDs remain unchanged.
- Invalid operations do not modify state.
- Filters contain only matching tasks.
- Dashboard counts are correct.

## 9.10 Deterministic Dates

Do not write tests that assume today's date.

Instead, call methods with a fixed date:

```text
today = date(2026, 11, 20)
```

Then verify tasks due on, before, or after that date.

## 9.11 Phase 3 Acceptance Checklist

- [ ] Expected failures have descriptive messages.
- [ ] Invalid input does not crash the console.
- [ ] Invalid input does not partially modify state.
- [ ] Custom exceptions or validation methods are used consistently.
- [ ] Missing records are distinct from duplicate records.
- [ ] Normal tests pass.
- [ ] Boundary tests pass.
- [ ] Failure tests pass.
- [ ] Tests can be rerun with one command.
- [ ] Tests use fixed dates or injected dates.
- [ ] No live data or external services are used.

---

## 10. Phase 4: Flask Browser Front End

## 10.1 Phase 4 Objective

Create a browser interface that connects to the same Phase 3 classes.

Do not rebuild scheduling logic in route functions or Jinja templates.

The Flask routes should translate web forms into scheduler calls.

## 10.2 Application Setup

The Flask application may resemble:

```python
app = Flask(__name__)
app.config["SECRET_KEY"] = "development-only"

scheduler = MaintenanceScheduler()
load_sample_data(scheduler)
```

The secret key must be appropriate for a local educational project.

Do not use an institutional secret or credential.

## 10.3 Suggested Flask Routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/` | Dashboard summary |
| GET | `/tasks` | List all tasks |
| GET, POST | `/tasks/new` | Create a task |
| GET | `/tasks/<int:task_id>` | Show task details |
| GET, POST | `/tasks/<int:task_id>/assign` | Assign or reassign staff |
| POST | `/tasks/<int:task_id>/complete` | Complete a task |
| GET | `/jobs/due` | Tasks due today |
| GET | `/jobs/overdue` | Overdue tasks |
| GET | `/jobs/upcoming` | Upcoming tasks |
| GET | `/jobs/completed` | Completed tasks |
| GET | `/staff` | List staff |
| GET | `/staff/<int:staff_id>` | Tasks assigned to one staff member |

Additional routes may be added, but these cover the core requirements.

## 10.4 Dashboard Page

The dashboard should display:

- Total task count.
- Due today count.
- Overdue count.
- Upcoming count.
- Completed count.
- Assigned count.
- Unassigned count.

Recommended sections:

- Summary cards.
- Overdue job table.
- Due-today job table.
- Upcoming job table.
- Quick links to create a task or view staff.

## 10.5 Task List Page

The task list should include:

- Task ID.
- Task name.
- Equipment.
- Location.
- Due date.
- Priority.
- Status.
- Assigned staff name.
- Detail link.
- Assign link.
- Complete action.

Do not show database internals or Python object representations.

## 10.6 Task Detail Page

The detail page should show:

- Task ID.
- Name.
- Equipment.
- Location.
- Recurrence interval.
- Due date.
- Priority.
- Status.
- Assigned staff.
- Classification such as due today or overdue.

It should also provide:

- Assign/reassign link.
- Complete button.
- Back to task list link.

## 10.7 Create Task Form

The form should collect:

- Task name.
- Equipment.
- Location.
- Recurrence interval.
- Due date.
- Priority.
- Optional staff ID.

Use HTML fields such as:

```text
input type="text"
input type="number"
input type="date"
select for priority
select for staff
```

### POST Behavior

On valid submission:

1. Parse form values.
2. Call a scheduler method.
3. Flash a success message.
4. Redirect to task detail or task list.

On invalid submission:

1. Catch expected validation exceptions.
2. Render the form again.
3. Display the error clearly.
4. Preserve valid field values.
5. Do not modify scheduler state.

The route should not implement interval or duplicate-ID logic.

## 10.8 Assignment Form

The page should receive `task_id`.

It should show:

- Task name.
- Equipment.
- Current assignee.
- Staff dropdown.
- Submit and cancel buttons.

On valid POST:

- Call `scheduler.assign_staff(task_id, staff_id)`.
- Flash success.
- Redirect to task detail or task list.

On invalid POST:

- Catch missing task/staff or invalid assignment.
- Re-render the page.
- Preserve the selected staff value.
- Show a clear message.

## 10.9 Complete Task Action

Because completion changes state, use POST.

On valid POST:

- Call `scheduler.complete_task(task_id, today=date.today())`.
- Flash success.
- If recurring, show the updated due date.
- Redirect to task detail or jobs view.

On invalid POST:

- Show a clear message.
- Do not change the state.

Do not implement a GET route that completes a task.

## 10.10 Staff Page

List:

- Staff ID.
- Name.
- Role.
- Number of assigned jobs.

Provide links to staff-specific job lists.

The staff-specific page should show:

- Staff details.
- Assigned tasks.
- Due, overdue, upcoming, and completed categories if useful.

## 10.11 Jinja Templates

Use template inheritance.

### base.html

Include:

- HTML doctype.
- Page title.
- Shared navigation.
- Flash message rendering.
- CSS reference.
- Main content block.

### Other Templates

- Reuse task-list partials if practical.
- Avoid repeating due/overdue table markup.
- Use links for navigation.
- Escape untrusted values by default.
- Use labels and `for` attributes.

## 10.12 Flash Messages

Use separate messages for:

- Successful scheduling.
- Successful assignment.
- Successful reassignment.
- Successful completion.
- Validation failure.
- Missing record.
- Duplicate record.
- Invalid transaction.

Example:

```text
Success: Task 101 scheduled.
Success: Task 101 assigned to Aisha Khan.
Error: Staff member 99 does not exist.
Error: Recurrence interval must be a positive whole number.
```

## 10.13 HTML Form Validation

HTML attributes can provide basic browser validation, but server-side validation is mandatory.

Do not rely only on:

- `required`.
- `min`.
- `maxlength`.
- HTML date input.

The scheduler and validation module must perform the final checks.

## 10.14 Flask Testing

Create Flask route tests using the test client.

Test:

- Dashboard returns HTTP 200.
- Task list returns HTTP 200.
- New task page returns HTTP 200.
- Task detail page returns HTTP 200.
- Valid POST creates a task.
- Invalid POST does not create a task.
- Valid assignment updates a task.
- Invalid assignment leaves state unchanged.
- Valid completion updates state.
- Invalid completion leaves state unchanged.
- Missing task ID does not crash.
- Staff route works.
- Overdue and due-today routes contain sample tasks.

Example test command:

```text
pytest phase4/tests -v
```

The README should provide the actual command used.

## 10.15 Browser Demonstration

Run:

```text
python app.py
```

or:

```text
python -m flask --app app run --debug
```

Then open the documented local address.

Do not leave the server running after final validation unless a live demo needs it.

## 10.16 Phase 4 Acceptance Checklist

- [ ] Flask starts without credentials or external setup.
- [ ] Dashboard is available.
- [ ] All required routes work.
- [ ] All forms have labels.
- [ ] Task creation works.
- [ ] Assignment works.
- [ ] Recurring completion updates the due date.
- [ ] Due and overdue pages work.
- [ ] Staff pages work.
- [ ] Validation messages appear on the page.
- [ ] Invalid submissions do not modify state.
- [ ] Flask route tests pass.
- [ ] Templates extend a shared base layout.
- [ ] CSS is applied to the interface.
- [ ] Browser demo uses sample data only.

---

## 11. Cross-Phase Test Matrix

| Case | Input / State | Expected Result |
|---|---|---|
| Valid task | Complete required fields | Task created |
| Blank name | Empty or whitespace | Validation error |
| Duplicate task ID | Existing positive ID | Duplicate error |
| Missing task ID | ID not in scheduler | Missing record error |
| Missing staff ID | ID not in staff collection | Missing record error |
| Invalid date | `2026-02-30` | Date parsing error |
| Wrong date format | `20/11/2026` | Format error |
| Today | Due date equals reference date | Due today |
| Overdue | Due date one day before reference date | Overdue |
| Upcoming | Due date one day after reference date | Upcoming |
| Interval 1 | Complete recurring task | Due date plus 1 day |
| Interval 30 | Complete recurring task | Due date plus 30 days |
| Zero interval | 0 | Validation error |
| Negative interval | -7 | Validation error |
| Decimal interval | 7.5 | Validation error |
| Nonnumeric interval | `weekly` | Validation error |
| Valid assignment | Existing task and staff | Assignment stored |
| Missing task assignment | No task | Assignment error |
| Missing staff assignment | No staff | Assignment error |
| Reassignment | Existing staff A then B | Staff B replaces A |
| Complete recurring | Scheduled recurring task | Status remains scheduled and due date advances |
| Complete one-time | Scheduled one-time task | Status becomes completed |
| Complete twice | Already completed | Invalid task-state error |
| Invalid menu | Choice 99 | Menu error and re-display |
| Empty menu input | Blank line | Menu error |
| Staff with no tasks | Valid staff | Empty task list |
| Dashboard | Mixed task statuses | Counts match actual categories |

---

## 12. Sample Data

### 12.1 Suggested Staff

| ID | Name | Role |
|---:|---|---|
| 1 | Aisha Khan | Electrical Technician |
| 2 | Rahul Mehta | HVAC Technician |
| 3 | Sara D'Souza | Plumbing Technician |
| 4 | Dev Patel | General Maintenance |

### 12.2 Suggested Tasks

For a fixed reference date of `2026-11-20`, use:

| ID | Task | Equipment | Location | Interval | Due Date | Priority | Status | Staff |
|---:|---|---|---|---:|---|---|---|---:|
| 101 | Inspect HVAC filter | AHU-1 | Mechanical room | 30 | 2026-11-20 | Medium | Scheduled | 2 |
| 102 | Emergency light test | EL-2 | Main block | 90 | 2026-11-18 | High | Scheduled | 1 |
| 103 | Water pump inspection | WP-1 | Utility room | 14 | 2026-11-15 | High | Scheduled | 3 |
| 104 | Elevator monthly inspection | Lift 3 | East wing | 30 | 2026-12-05 | High | Scheduled | 4 |
| 105 | Fire alarm panel test | FA-1 | Security room | 90 | 2026-11-26 | Critical | Scheduled | 1 |
| 106 | Replace AC belt | AHU-2 | Central block | 60 | 2026-12-10 | Medium | Scheduled | 2 |
| 107 | Quarterly drain cleaning | Drain 4 | Canteen | 7 | 2026-11-10 | Low | Completed | 3 |
| 108 | Exit sign inspection | EX-5 | South wing | 180 | 2026-11-19 | Medium | Scheduled | None |
| 109 | Replace corridor bulb | CB-12 | First floor | 1 | 2026-11-20 | Low | Scheduled | 4 |
| 110 | Annual fire extinguisher audit | FE-SET | Storage block | 365 | 2026-12-31 | Critical | Scheduled | None |

Adjust sample dates when running later if the program uses the real current date rather than the fixed date.

For a dynamic demo, generate some due-today and overdue dates relative to `date.today()` so the browser always has matching sample jobs.

---

## 13. Expected Console Menu

Example menu:

```text
Facilities Maintenance Scheduler
==============================
1. Schedule a maintenance task
2. Assign or reassign staff
3. View all tasks
4. View due today
5. View overdue tasks
6. View upcoming tasks
7. View completed tasks
8. View tasks for staff
9. Complete a task
10. View staff
0. Exit
Select an option:
```

After a valid operation, return to the menu.

After an invalid operation, display:

```text
Error: <clear explanation>
Please select an option again.
```

Do not exit for expected errors.

---

## 14. Expected Web Routes and Pages

### 14.1 Route Responsibilities

Routes should:

- Read request values.
- Perform basic integer conversion if needed.
- Call the scheduler or model.
- Catch expected exceptions.
- Render a template or redirect.
- Flash success or failure messages.

Routes should not:

- Compare many due dates.
- Search for staff manually with nested loops.
- Create task objects in HTML-specific code.
- Implement recurring-date calculations.
- Display raw exception objects.

### 14.2 Form Field Names

Use consistent names across Flask and tests:

```text
name
equipment
location
interval_days
due_date
priority
staff_id
status
```

### 14.3 Status Labels

The interface should classify jobs clearly:

- `Due Today`
- `Overdue`
- `Upcoming`
- `Completed`
- `Unassigned`

A task may belong to more than one category, except overdue/due/upcoming are mutually exclusive for scheduled tasks.

---

## 15. Data State and Transition Rules

### Scheduling

State before:

- Task ID not present.
- No task record.

State after:

- New task exists.
- Status is `Scheduled`.
- Due date is stored.
- Assignment may be empty.

### Assignment

State before:

- Existing task.
- Existing staff.

State after:

- Task stores selected staff reference or ID.
- No duplicate assignment record is created.

### Reassignment

State before:

- Task assigned to staff A.

State after:

- Task assigned to staff B.
- Staff A's assigned-job calculation no longer includes the task.

### Recurring Completion

State before:

- Status `Scheduled`.
- Due date D.
- Interval I.

State after:

- Status `Scheduled`.
- Due date D + I.
- Staff assignment remains unchanged.
- Task remains in the system.

### One-Time Completion

State before:

- Status `Scheduled`.
- No recurrence interval or `None`.

State after:

- Status `Completed`.
- Completed date may be stored.
- Staff assignment remains unchanged.

---

## 16. README and Submission Requirements

The README should contain:

- Project title.
- Team member names.
- Project statement.
- Core operations.
- Domain rules.
- Python version.
- Virtual environment instructions.
- Installation command.
- Console application command.
- Flask application command.
- Test command.
- Sample staff and task explanation.
- Phase features completed.
- Known limitations.
- Folder structure.
- Screenshots or demo notes if required.

The README should not claim that a live institution or API is used.

### 16.1 Requirements File

The requirements file should include:

- Flask.
- Testing package if external.
- Any additional library actually used.

Do not add packages that are not used.

### 16.2 Source Code Quality

- Use PEP 8 naming and formatting where practical.
- Use snake_case for functions and variables.
- Use PascalCase for classes.
- Use descriptive names.
- Avoid magic numbers.
- Avoid one-line functions that only restate another function.
- Remove unused imports.
- Remove temporary print statements.
- Add comments only for non-obvious logic.
- Add docstrings to public classes and complex functions if the team standard requests it.

---

## 17. Verification Checklists

## 17.1 Phase 1 Verification

- [x] Start the program.
- [x] Verify sample staff appears.
- [x] Verify sample tasks appear.
- [x] Schedule a sample task.
- [x] Assign that task.
- [x] View due today.
- [x] View overdue.
- [x] Complete a recurring task.
- [x] Confirm due date changed.
- [x] Exit normally.

## 17.2 Phase 2 Verification

- [ ] Run the same Phase 1 operations.
- [ ] Verify that a staff object is used.
- [ ] Verify that task objects are used.
- [ ] Verify that `MaintenanceScheduler` owns collections.
- [ ] Verify composition or inheritance has a clear purpose.
- [ ] Verify menu input is separated from domain logic.

## 17.3 Phase 3 Verification

- [ ] Run all unit tests.
- [ ] Run failure tests.
- [ ] Run boundary tests.
- [ ] Confirm invalid input returns to the menu.
- [ ] Confirm invalid assignment changes nothing.
- [ ] Confirm invalid task creation changes nothing.
- [ ] Confirm duplicate detection works.
- [ ] Confirm missing records work.

## 17.4 Phase 4 Verification

- [ ] Start Flask.
- [ ] Open the dashboard.
- [ ] Open all task views.
- [ ] Create a task.
- [ ] Assign a task.
- [ ] Reassign a task.
- [ ] Complete a task.
- [ ] Submit invalid forms.
- [ ] Verify flash messages and inline errors.
- [ ] Run Flask tests.
- [ ] Stop the server.

## 17.5 Submission Verification

- [ ] All four phase deliverables are represented.
- [ ] README is complete.
- [ ] Requirements file is complete.
- [ ] Tests run from a clean environment.
- [ ] No generated virtual-environment folders are submitted.
- [ ] No temporary files or logs are submitted.
- [ ] No unrelated institutional data is present.
- [ ] No live URLs or API credentials are required.
- [ ] Team members can explain the code.

---

## 18. Final Demonstration Script

Use this as the minimum final walkthrough:

1. Open the Flask dashboard.
2. Point out total, due-today, overdue, upcoming, completed, and assigned counts.
3. Open the overdue task page.
4. Open one overdue task's detail page.
5. Reassign the task or assign an unassigned task.
6. Create a new recurring maintenance task.
7. Enter valid data and confirm successful creation.
8. Complete the recurring task.
9. Show that the due date has advanced by the interval.
10. Submit invalid form data, such as a zero interval or nonexistent staff.
11. Show that an error message appears and state remains unchanged.
12. Open the staff page and show assigned tasks.
13. Briefly explain the scheduler and class responsibilities.
14. Run or mention the automated test command.
15. Explain that all data is sample data.

The team should be able to answer:

- Why is a task overdue?
- How is its next due date calculated?
- Where is assignment validation performed?
- Why does the Flask route not implement domain logic?
- How does the project distinguish missing and duplicate records?

---

## 19. Phase Dependencies

```text
Project Setup
  |
  v
Phase 1 - Procedural implementation
  |
  v
Phase 1 verification
  |
  v
Phase 2 - OOP refactor
  |
  v
Phase 2 verification
  |
  v
Phase 3 - validation and tests
  |
  v
Phase 3 verification
  |
  v
Phase 4 - Flask front end
  |
  v
Phase 4 verification
  |
  v
Final demonstration
```

Do not start Flask until the scheduler can pass Phase 3 tests.

Do not add advanced Flask features before core routes are working.

---

## 20. Optional Enhancements

Only add these after the required features are complete.

- Search tasks by name.
- Filter tasks by priority.
- Filter tasks by location.
- Filter tasks by staff role.
- Add task descriptions and notes.
- Sort overdue tasks by number of days overdue.
- Sort tasks by priority.
- Add a small completion history.
- Add JSON export.
- Add CSV export.
- Add pagination for large task lists.
- Add recurrence preview showing the next three due dates.
- Add a dashboard chart.
- Add CSS theme styles.
- Add keyboard-accessible navigation.
- Add confirmation messages for task completion.

Do not allow optional features to replace required routes or operations.

---

## 21. Common Mistakes to Avoid

- Using string comparisons for due dates.
- Comparing timezone-aware and timezone-naive values.
- Duplicating task logic in Flask routes.
- Using `except Exception` for every error.
- Catching errors silently.
- Letting invalid input partially update records.
- Using database-style code in Phase 1.
- Rebuilding classes in Phase 4.
- Calculating overdue in a Jinja template instead of the scheduler.
- Hardcoding the staff name instead of the staff ID or object.
- Using duplicate task names as the primary record key.
- Resetting task IDs after each menu operation.
- Treating overdue as a status that never changes.
- Completing an overdue recurring task and then losing the overdue schedule.
- Marking a recurring task as completed permanently.
- Allowing a negative interval.
- Accepting invalid dates such as `2026-13-40`.
- Returning raw Python errors in Flask.
- Using GET requests for completion or assignment changes.
- Requiring database setup for the demo.
- Using institutional data or real systems.
- Implementing features no team member can explain.
