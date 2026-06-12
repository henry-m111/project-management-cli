# main.py

import argparse
from models import User, Project, Task
from utils.file_io import save_data, load_data
from utils.display import display_users, display_projects, display_tasks, success, error, info


def handle_add_user(args):
    """Add a new user."""
    if User.find_by_name(args.name):
        error(f"User '{args.name}' already exists.")
        return
    user = User(args.name, args.email)
    save_data()
    success(f"User '{user.name}' created successfully!")


def handle_list_users(args):
    """List all users."""
    display_users(User.all())


def handle_add_project(args):
    """Add a project to a user."""
    user = User.find_by_name(args.user)
    if not user:
        error(f"User '{args.user}' not found.")
        return
    if Project.find_by_title(args.title):
        error(f"Project '{args.title}' already exists.")
        return
    project = Project(args.title, args.description, args.due_date, user)
    save_data()
    success(f"Project '{project.title}' created and assigned to '{user.name}'!")


def handle_list_projects(args):
    """List all projects or filter by user."""
    if args.user:
        user = User.find_by_name(args.user)
        if not user:
            error(f"User '{args.user}' not found.")
            return
        projects = Project.find_by_owner(user)
        info(f"Projects for {user.name}:")
        display_projects(projects)
    else:
        display_projects(Project.all())


def handle_add_task(args):
    """Add a task to a project."""
    project = Project.find_by_title(args.project)
    if not project:
        error(f"Project '{args.project}' not found.")
        return
    task = Task(args.title, args.assigned_to, project)
    save_data()
    success(f"Task '{task.title}' added to project '{project.title}'!")


def handle_list_tasks(args):
    """List all tasks or filter by project."""
    if args.project:
        project = Project.find_by_title(args.project)
        if not project:
            error(f"Project '{args.project}' not found.")
            return
        tasks = Task.find_by_project(project)
        info(f"Tasks for project '{project.title}':")
        display_tasks(tasks)
    else:
        display_tasks(Task.all())


def handle_complete_task(args):
    """Mark a task as complete."""
    for task in Task.all():
        if task.title.lower() == args.title.lower():
            task.complete()
            save_data()
            success(f"Task '{task.title}' marked as complete!")
            return
    error(f"Task '{args.title}' not found.")


def handle_update_task(args):
    """Update task status."""
    for task in Task.all():
        if task.title.lower() == args.title.lower():
            try:
                task.status = args.status
                save_data()
                success(f"Task '{task.title}' status updated to '{args.status}'!")
            except ValueError as e:
                error(str(e))
            return
    error(f"Task '{args.title}' not found.")


def main():
    # Load existing data on startup
    load_data()

    parser = argparse.ArgumentParser(
        prog="project-management-cli",
        description="A CLI tool to manage users, projects, and tasks."
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- add-user ---
    p_add_user = subparsers.add_parser("add-user", help="Add a new user")
    p_add_user.add_argument("--name", required=True, help="User's name")
    p_add_user.add_argument("--email", required=True, help="User's email")

    # --- list-users ---
    subparsers.add_parser("list-users", help="List all users")

    # --- add-project ---
    p_add_project = subparsers.add_parser("add-project", help="Add a project to a user")
    p_add_project.add_argument("--user", required=True, help="Owner's name")
    p_add_project.add_argument("--title", required=True, help="Project title")
    p_add_project.add_argument("--description", required=True, help="Project description")
    p_add_project.add_argument("--due-date", required=True, dest="due_date", help="Due date (YYYY-MM-DD)")

    # --- list-projects ---
    p_list_projects = subparsers.add_parser("list-projects", help="List all projects")
    p_list_projects.add_argument("--user", help="Filter by user name")

    # --- add-task ---
    p_add_task = subparsers.add_parser("add-task", help="Add a task to a project")
    p_add_task.add_argument("--project", required=True, help="Project title")
    p_add_task.add_argument("--title", required=True, help="Task title")
    p_add_task.add_argument("--assigned-to", required=True, dest="assigned_to", help="Assigned to")

    # --- list-tasks ---
    p_list_tasks = subparsers.add_parser("list-tasks", help="List all tasks")
    p_list_tasks.add_argument("--project", help="Filter by project title")

    # --- complete-task ---
    p_complete_task = subparsers.add_parser("complete-task", help="Mark a task as complete")
    p_complete_task.add_argument("--title", required=True, help="Task title")

    # --- update-task ---
    p_update_task = subparsers.add_parser("update-task", help="Update task status")
    p_update_task.add_argument("--title", required=True, help="Task title")
    p_update_task.add_argument("--status", required=True, help="New status (pending/in-progress/complete)")

    args = parser.parse_args()

    # Route to correct handler
    commands = {
        "add-user": handle_add_user,
        "list-users": handle_list_users,
        "add-project": handle_add_project,
        "list-projects": handle_list_projects,
        "add-task": handle_add_task,
        "list-tasks": handle_list_tasks,
        "complete-task": handle_complete_task,
        "update-task": handle_update_task,
    }

      # Handle no command given
    if args.command is None:
        parser.print_help()
        return

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()