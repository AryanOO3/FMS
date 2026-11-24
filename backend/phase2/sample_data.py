from datetime import timedelta

from backend.phase2.models import Staff


def load_phase2_sample_data(scheduler, reference_today):
    staff_members = [
        Staff(1, "Aisha Khan", "Electrical Technician"),
        Staff(2, "Rahul Mehta", "HVAC Technician"),
        Staff(3, "Sara D'Souza", "Plumbing Technician"),
        Staff(4, "Dev Patel", "General Maintenance"),
        Staff(5, "Meera Iyer", "Fire Safety Technician"),
        Staff(6, "Kabir Singh", "Elevator Technician"),
        Staff(7, "Neha Rao", "Facilities Supervisor"),
        Staff(8, "Arjun Nair", "Generator Technician"),
    ]
    for staff in staff_members:
        scheduler.add_staff(staff)

    tasks = [
        (101, "Inspect HVAC filter", "AHU-1", "Mechanical Room", 30, 0, "Medium", 2),
        (102, "Emergency light test", "EL-2", "Main Block", 90, -2, "High", 1),
        (103, "Water pump inspection", "WP-1", "Utility Room", 14, -5, "High", 3),
        (104, "Elevator monthly inspection", "Lift 3", "East Wing", 30, 15, "High", 6),
        (105, "Fire alarm panel test", "FA-1", "Security Room", 90, 6, "Critical", 5),
        (106, "Replace AC belt", "AHU-2", "Central Block", 60, 20, "Medium", 2),
        (107, "Quarterly drain cleaning", "Drain 4", "Canteen", 90, -10, "Low", 3),
        (108, "Exit sign inspection", "EX-5", "South Wing", 180, -1, "Medium", None),
        (109, "Replace corridor bulb", "CB-12", "First Floor", 0, 0, "Low", 4),
        (110, "Fire extinguisher audit", "FE-SET", "Storage Block", 365, 41, "Critical", 5),
        (111, "Diesel generator load test", "DG-1", "Generator Shed", 180, 8, "Critical", 8),
        (112, "Clean roof drainage", "RD-7", "Roof", 30, -3, "Medium", None),
        (113, "Inspect boiler pressure valves", "BL-2", "Boiler Room", 45, 12, "High", 7),
        (114, "Calibrate water temperature sensor", "WT-8", "Kitchen", 14, 3, "Medium", 3),
        (115, "Emergency exit door check", "ED-4", "West Wing", 7, 0, "High", 4),
        (116, "UPS battery inspection", "UPS-2", "Server Room", 30, 22, "Critical", 1),
        (117, "Restroom fixture leak check", "RF-6", "West Block", 0, 1, "Low", 3),
        (118, "Replace lobby ceiling tile", "CT-9", "Reception", 0, -7, "Low", 4),
        (119, "HVAC duct sanitation", "DU-3", "All Blocks", 180, 35, "Medium", 2),
        (120, "Security access alarm test", "SA-1", "Main Gate", 30, 5, "High", 7),
    ]

    for task_id, name, equipment, location, interval, offset, priority, staff_id in tasks:
        task = scheduler.schedule_task(
            task_id,
            name,
            equipment,
            location,
            interval,
            reference_today + timedelta(days=offset),
            priority,
            staff_id,
        )

        if task_id in (107, 118):
            task.status = "Completed"

    return scheduler
