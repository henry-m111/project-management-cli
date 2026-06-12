# Project Management CLI Tool

A command-line interface (CLI) tool for managing users, projects, and tasks. Built with Python using OOP principles, JSON persistence, and the `rich` library for styled terminal output.

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/henry-m111/project-management-cli.git
cd project-management-cli
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

---

## How to Run CLI Commands

### Users
```bash
python main.py add-user --name "Alex" --email "alex@example.com"
python main.py list-users
```

### Projects
```bash
python main.py add-project --user "Alex" --title "CLI Tool" --description "Build a CLI app" --due-date "2025-12-31"
python main.py list-projects
python main.py list-projects --user "Alex"
```

### Tasks
```bash
python main.py add-task --project "CLI Tool" --title "Implement add-task" --assigned-to "Alex"
python main.py list-tasks
python main.py list-tasks --project "CLI Tool"
python main.py complete-task --title "Implement add-task"
python main.py update-task --title "Implement add-task" --status "in-progress"
```

---

## Features

- Add and list users, projects, and tasks via CLI
- One-to-many relationships: User → Projects → Tasks
- JSON file persistence (auto-saves to `data/data.json`)
- Styled terminal output using `rich`
- Input validation with descriptive error messages
- Unit tests with `pytest`

## Running Tests

```bash
pytest tests/
```

---

## Known Issues

- Task lookup by title is case-insensitive but project/user lookup is not fully consistent
- No delete commands implemented yet