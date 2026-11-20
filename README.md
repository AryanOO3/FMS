# Facilities Maintenance Scheduler

A menu-driven Facilities Maintenance Scheduler built for the first phase of the EL project. The program uses procedural Python, sample data, and no external services or institutional records.

## Phase 1 Features

- Schedule recurring or one-time maintenance tasks.
- Assign or reassign staff members.
- View all tasks.
- View tasks due today.
- View overdue tasks.
- View upcoming tasks.
- View completed tasks.
- View tasks assigned to a staff member.
- Complete tasks and advance recurring task due dates.

## Domain Rules

- Dates use ISO format: `YYYY-MM-DD`.
- Task and staff IDs are positive integers and must be unique.
- Recurrence intervals are positive whole numbers of days.
- One-time tasks use a recurrence interval of `0`.
- Due today is when `due_date == today`.
- Overdue is when `due_date < today`.
- Upcoming is when `due_date > today`.
- Completing a recurring task adds its interval to the previous due date.
- Completing a one-time task marks it as completed.

## Run the Console Application

Use Python 3.10 or later.

```powershell
py -m backend.main
```

On another Python installation, run:

```powershell
python -m backend.main
```

## Run Tests

```powershell
python -m unittest discover -s backend/tests -v
```

The test suite uses fixed dates so it does not depend on the system date.

## Project Structure

```text
backend/
  main.py
  phase1/
    procedural_scheduler.py
  phase2/
  phase3/
  tests/
    test_phase1.py
frontend/
  phase4/
TODO.md
README.md
```

## Sample Data

The application starts with four staff members and ten maintenance tasks. Sample data includes due-today, overdue, upcoming, completed, recurring, assigned, and unassigned tasks.
