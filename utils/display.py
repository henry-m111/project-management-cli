# utils/display.py

from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


def display_users(users):
    """Display all users in a rich table."""
    if not users:
        console.print("[yellow]No users found.[/yellow]")
        return

    table = Table(title="Users", box=box.ROUNDED, style="cyan")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Name", style="bold green")
    table.add_column("Email", style="blue")
    table.add_column("Projects", justify="center")

    for user in users:
        table.add_row(
            str(user.id),
            user.name,
            user.email,
            str(len(user.projects))
        )

    console.print(table)


def display_projects(projects):
    """Display all projects in a rich table."""
    if not projects:
        console.print("[yellow]No projects found.[/yellow]")
        return

    table = Table(title="Projects", box=box.ROUNDED, style="magenta")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Title", style="bold green")
    table.add_column("Owner", style="cyan")
    table.add_column("Due Date", style="yellow")
    table.add_column("Tasks", justify="center")
    table.add_column("Description")

    for project in projects:
        table.add_row(
            str(project.id),
            project.title,
            project.owner.name,
            project.due_date,
            str(len(project.tasks)),
            project.description
        )

    console.print(table)


def display_tasks(tasks):
    """Display all tasks in a rich table."""
    if not tasks:
        console.print("[yellow]No tasks found.[/yellow]")
        return

    table = Table(title="Tasks", box=box.ROUNDED, style="blue")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Title", style="bold green")
    table.add_column("Assigned To", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Project", style="magenta")

    for task in tasks:
        status = task.status
        if status == "complete":
            status_display = f"[green]{status}[/green]"
        elif status == "in-progress":
            status_display = f"[yellow]{status}[/yellow]"
        else:
            status_display = f"[red]{status}[/red]"

        table.add_row(
            str(task.id),
            task.title,
            task.assigned_to,
            status_display,
            task.project.title
        )

    console.print(table)


def success(message):
    """Print a success message."""
    console.print(f"[bold green]✔ {message}[/bold green]")


def error(message):
    """Print an error message."""
    console.print(f"[bold red]✘ {message}[/bold red]")


def info(message):
    """Print an info message."""
    console.print(f"[bold cyan]ℹ {message}[/bold cyan]")