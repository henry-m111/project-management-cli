# models/task.py

class Task:
    _all = []  # class attribute to track all tasks
    _id_counter = 1  # auto-incrementing ID

    VALID_STATUSES = ["pending", "in-progress", "complete"]

    def __init__(self, title, assigned_to, project):
        self._title = title
        self._assigned_to = assigned_to  # name of person responsible
        self._status = "pending"         # default status
        self.project = project           # Project object (many-to-one)
        self.id = Task._id_counter
        Task._id_counter += 1
        Task._all.append(self)
        project.add_task(self)           # link task to project

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Title must be a non-empty string.")
        self._title = value

    @property
    def assigned_to(self):
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Assigned to must be a non-empty string.")
        self._assigned_to = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of: {self.VALID_STATUSES}")
        self._status = value

    def complete(self):
        self._status = "complete"

    @classmethod
    def all(cls):
        return cls._all

    @classmethod
    def find_by_project(cls, project):
        return [t for t in cls._all if t.project == project]

    def __str__(self):
        return (f"[Task #{self.id}] {self._title} | "
                f"Assigned to: {self._assigned_to} | "
                f"Status: {self._status} | "
                f"Project: {self.project.title}")

    def __repr__(self):
        return f"Task(title={self._title!r}, status={self._status!r})"