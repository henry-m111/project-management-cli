# models/project.py

from datetime import date


class Project:
    _all = []
    _id_counter = 1

    def __init__(self, title, description, due_date, owner):
        self.title = title
        self.description = description
        self.due_date = due_date  # Uses setter validation
        self.owner = owner

        self.id = Project._id_counter
        Project._id_counter += 1

        self.tasks = []

        Project._all.append(self)
        owner.add_project(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Title must be a non-empty string.")
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        try:
            date.fromisoformat(value)
        except ValueError:
            raise ValueError("Due date must be in YYYY-MM-DD format.")

        self._due_date = value

    @classmethod
    def all(cls):
        return cls._all

    @classmethod
    def find_by_title(cls, title):
        for project in cls._all:
            if project.title.lower() == title.lower():
                return project
        return None

    @classmethod
    def find_by_owner(cls, user):
        return [p for p in cls._all if p.owner == user]

    def add_task(self, task):
        self.tasks.append(task)

    def __str__(self):
        return (
            f"[Project #{self.id}] {self._title} | "
            f"Owner: {self.owner.name} | "
            f"Due: {self._due_date} | "
            f"Tasks: {len(self.tasks)}"
        )

    def __repr__(self):
        return f"Project(title={self._title!r}, owner={self.owner.name!r})"