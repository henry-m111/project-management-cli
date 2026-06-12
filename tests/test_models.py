# tests/test_models.py

import pytest
from models.user import User, Person
from models.project import Project
from models.task import Task


# --- Fixtures ---

@pytest.fixture(autouse=True)
def clear_all():
    """Reset all class-level data before each test."""
    User._all.clear()
    User._id_counter = 1
    Project._all.clear()
    Project._id_counter = 1
    Task._all.clear()
    Task._id_counter = 1


@pytest.fixture
def sample_user():
    return User("Mbugo", "mbugo@moringa.com")


@pytest.fixture
def sample_project(sample_user):
    return Project("CLI Tool", "A project tracker", "2025-12-31", sample_user)


@pytest.fixture
def sample_task(sample_project):
    return Task("Write tests", "Mbugo", sample_project)


# --- User Tests ---

class TestUser:
    def test_user_creation(self, sample_user):
        assert sample_user.name == "Mbugo"
        assert sample_user.email == "mbugo@moringa.com"
        assert sample_user.id == 1

    def test_user_added_to_all(self, sample_user):
        assert sample_user in User.all()

    def test_user_find_by_name(self, sample_user):
        found = User.find_by_name("Mbugo")
        assert found == sample_user

    def test_user_find_by_name_not_found(self):
        assert User.find_by_name("Ghost") is None

    def test_invalid_email_raises(self):
        with pytest.raises(ValueError):
            User("Bad Email", "notanemail")

    def test_invalid_name_raises(self):
        u = User("Mbugo", "mbugo@moringa.com")
        with pytest.raises(ValueError):
            u.name = ""

    def test_user_inherits_from_person(self, sample_user):
        assert isinstance(sample_user, Person)


# --- Project Tests ---

class TestProject:
    def test_project_creation(self, sample_project, sample_user):
        assert sample_project.title == "CLI Tool"
        assert sample_project.owner == sample_user
        assert sample_project.id == 1

    def test_project_linked_to_user(self, sample_project, sample_user):
        assert sample_project in sample_user.projects

    def test_project_added_to_all(self, sample_project):
        assert sample_project in Project.all()

    def test_find_by_title(self, sample_project):
        found = Project.find_by_title("CLI Tool")
        assert found == sample_project

    def test_find_by_owner(self, sample_project, sample_user):
        results = Project.find_by_owner(sample_user)
        assert sample_project in results

    def test_invalid_due_date_raises(self, sample_user):
        with pytest.raises(ValueError):
            Project("Bad Date", "desc", "not-a-date", sample_user)


# --- Task Tests ---

class TestTask:
    def test_task_creation(self, sample_task, sample_project):
        assert sample_task.title == "Write tests"
        assert sample_task.assigned_to == "Mbugo"
        assert sample_task.status == "pending"
        assert sample_task.project == sample_project

    def test_task_linked_to_project(self, sample_task, sample_project):
        assert sample_task in sample_project.tasks

    def test_task_complete(self, sample_task):
        sample_task.complete()
        assert sample_task.status == "complete"

    def test_invalid_status_raises(self, sample_task):
        with pytest.raises(ValueError):
            sample_task.status = "flying"

    def test_find_by_project(self, sample_task, sample_project):
        results = Task.find_by_project(sample_project)
        assert sample_task in results

    def test_task_added_to_all(self, sample_task):
        assert sample_task in Task.all()