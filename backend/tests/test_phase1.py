import io
import unittest
from datetime import date, timedelta
from contextlib import redirect_stdout
from unittest.mock import patch

from backend.phase1.procedural_scheduler import (
    assign_staff,
    complete_task,
    find_staff,
    find_task,
    load_sample_data,
    schedule_task,
    view_due_today,
    view_overdue,
    view_upcoming,
)


class ProceduralSchedulerTests(unittest.TestCase):
    def setUp(self):
        self.today = date(2026, 11, 20)
        self.staff, self.tasks = load_sample_data(self.today)

    def test_sample_data_contains_required_categories(self):
        self.assertEqual(len(self.staff), 4)
        self.assertEqual(len(self.tasks), 10)
        self.assertTrue(find_staff(self.staff, 1))
        self.assertTrue(find_task(self.tasks, 101))

    def test_due_today_filter(self):
        matches = [
            task
            for task in self.tasks
            if task["status"] == "Scheduled"
            and task["due_date"] == self.today
        ]
        self.assertEqual({101, 109}, {task["task_id"] for task in matches})

    def test_overdue_filter(self):
        matches = [
            task
            for task in self.tasks
            if task["status"] == "Scheduled"
            and task["due_date"] < self.today
        ]
        self.assertIn(102, {task["task_id"] for task in matches})
        self.assertIn(103, {task["task_id"] for task in matches})
        self.assertIn(108, {task["task_id"] for task in matches})

    def test_upcoming_filter(self):
        matches = [
            task
            for task in self.tasks
            if task["status"] == "Scheduled"
            and task["due_date"] > self.today
        ]
        self.assertIn(104, {task["task_id"] for task in matches})
        self.assertIn(105, {task["task_id"] for task in matches})

    def test_schedule_valid_task(self):
        answers = iter(
            [
                "111",
                "Generator service",
                "Generator G-1",
                "Utility block",
                "45",
                "2026-12-01",
                "High",
                "4",
            ]
        )
        with patch("builtins.input", side_effect=answers):
            schedule_task(self.tasks, self.staff, self.today)

        task = find_task(self.tasks, 111)
        self.assertIsNotNone(task)
        self.assertEqual(task["equipment"], "Generator G-1")
        self.assertEqual(task["interval_days"], 45)
        self.assertEqual(task["assigned_staff_id"], 4)

    def test_schedule_rejects_duplicate_task_id(self):
        answers = iter(["101", "Duplicate"])
        with patch("builtins.input", side_effect=answers):
            schedule_task(self.tasks, self.staff, self.today)

        self.assertEqual(len(self.tasks), 10)

    def test_schedule_rejects_invalid_recurrence(self):
        answers = iter(
            [
                "111",
                "Generator service",
                "Generator G-1",
                "Utility block",
                "weekly",
            ]
        )
        with patch("builtins.input", side_effect=answers):
            schedule_task(self.tasks, self.staff, self.today)

        self.assertIsNone(find_task(self.tasks, 111))

    def test_assign_staff(self):
        answers = iter(["101", "3"])
        with patch("builtins.input", side_effect=answers):
            assign_staff(self.tasks, self.staff)

        task = find_task(self.tasks, 101)
        self.assertEqual(task["assigned_staff_id"], 3)

    def test_assign_rejects_missing_staff(self):
        answers = iter(["101", "99"])
        original = find_task(self.tasks, 101)["assigned_staff_id"]
        with patch("builtins.input", side_effect=answers):
            assign_staff(self.tasks, self.staff)

        self.assertEqual(find_task(self.tasks, 101)["assigned_staff_id"], original)

    def test_complete_recurring_task_advances_due_date(self):
        task = find_task(self.tasks, 101)
        original_due_date = task["due_date"]

        with patch("builtins.input", return_value="101"):
            complete_task(self.tasks, self.staff, self.today)

        self.assertEqual(
            task["due_date"],
            original_due_date + timedelta(days=task["interval_days"]),
        )
        self.assertEqual(task["status"], "Scheduled")

    def test_complete_one_time_task_marks_completed(self):
        task = find_task(self.tasks, 109)
        with patch("builtins.input", return_value="109"):
            complete_task(self.tasks, self.staff, self.today)

        self.assertEqual(task["status"], "Completed")

    def test_complete_missing_task_has_no_effect(self):
        original_count = len(self.tasks)
        with patch("builtins.input", return_value="999"):
            complete_task(self.tasks, self.staff, self.today)
        self.assertEqual(len(self.tasks), original_count)

    def test_due_overdue_and_upcoming_output_runs(self):
        output = io.StringIO()
        with redirect_stdout(output):
            view_due_today(self.tasks, self.staff, self.today)
            view_overdue(self.tasks, self.staff, self.today)
            view_upcoming(self.tasks, self.staff, self.today)

        text = output.getvalue()
        self.assertIn("Inspect HVAC filter", text)
        self.assertIn("Emergency light test", text)
        self.assertIn("Elevator monthly inspection", text)


if __name__ == "__main__":
    unittest.main()
