# utils/file_io.py

import json
import os
from models import User, Project, Task

DATA_FILE = "data/data.json"


def save_data():
    """Save all users, projects, and tasks to JSON file."""
    data = {
        "users": [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
            for user in User.all()
        ],
        "projects": [
            {
                "id": project.id,
                "title": project.title,
                "description": project.description,
                "due_date": project.due_date,
                "owner": project.owner.name
            }
            for project in Project.all()
        ],
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "assigned_to": task.assigned_to,
                "status": task.status,
                "project": task.project.title
            }
            for task in Task.all()
        ]
    }

    try:
        os.makedirs("data", exist_ok=True)
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print("Data saved successfully.")
    except Exception as e:
        print(f"Error saving data: {e}")


def load_data():
    """Load users, projects, and tasks from JSON file."""
    if not os.path.exists(DATA_FILE):
        return  # no data yet, start fresh

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        # Re-create users
        for u in data.get("users", []):
            user = User(u["name"], u["email"])
            user.id = u["id"]

        # Update ID counter to avoid duplicates
        if User.all():
            User._id_counter = max(u.id for u in User.all()) + 1

        # Re-create projects
        for p in data.get("projects", []):
            owner = User.find_by_name(p["owner"])
            if owner:
                project = Project(p["title"], p["description"], p["due_date"], owner)
                project.id = p["id"]

        # Update ID counter
        if Project.all():
            Project._id_counter = max(p.id for p in Project.all()) + 1

        # Re-create tasks
        for t in data.get("tasks", []):
            project = Project.find_by_title(t["project"])
            if project:
                task = Task(t["title"], t["assigned_to"], project)
                task.id = t["id"]
                task.status = t["status"]

        # Update ID counter
        if Task.all():
            Task._id_counter = max(t.id for t in Task.all()) + 1

    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error loading data: {e}")