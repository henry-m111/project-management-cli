# models/user.py

# Base class using inheritance
class Person:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string.")
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not value or "@" not in value:
            raise ValueError("Invalid email address.")
        self._email = value

    def __str__(self):
        return f"{self._name} ({self._email})"


# User inherits from Person
class User(Person):
    _all = []
    _id_counter = 1

    def __init__(self, name, email):
        super().__init__(name, email)
        self.id = User._id_counter
        User._id_counter += 1
        self.projects = []
        User._all.append(self)

    @classmethod
    def all(cls):
        return cls._all

    @classmethod
    def find_by_name(cls, name):
        for user in cls._all:
            if user.name.lower() == name.lower():
                return user
        return None

    def add_project(self, project):
        self.projects.append(project)

    def __str__(self):
        return (
            f"[User #{self.id}] "
            f"{self._name} | {self._email} | "
            f"Projects: {len(self.projects)}"
        )

    def __repr__(self):
        return f"User(name={self._name!r}, email={self._email!r})"