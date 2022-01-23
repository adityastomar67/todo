import typer
from rich.console import Console
from rich.table import Table

from database import complete_todo, delete_todo, get_all_todos, insert_todo, update_todo
from model import Todo

console = Console()
app = typer.Typer()


@app.command(short_help="Adds the Task to the list")
def add(task: str, category: str):
    typer.echo(f"Adding task: {task} in category: {category}")
    todo = Todo(task, category)
    insert_todo(todo)
    show()


@app.command(short_help="Removes the Task from the list")
def remove(position: int):
    typer.echo(f"Removing task: {position}")
    delete_todo(position - 1)
    show()


@app.command(short_help="Updates the task in the list")
def update(position: int, task: str, category: str):
    typer.echo(f"Updating task: {position} to {task} in category: {category}")
    update_todo(position - 1, task, category)
    show()


@app.command()
def complete(position: int):
    typer.echo(f"Marking completing task: {position} as completed")
    complete_todo(position - 1)
    show()


@app.command()
def show():
    tasks = get_all_todos()

    console.print("[bold magenta]Showing all tasks[/bold magenta]")
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Task", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Completed", min_width=12, justify="right")

    def get_category_color(category):
        COLORS = {"Learn": "cyan", "Work": "yellow", "Home": "green", "Other": "red"}
        if category in COLORS:
            return COLORS[category]
        return "white"

    for idx, task in enumerate(tasks, start=1):
        clr = get_category_color(task.category)
        is_done_str = "✅" if task.status == 2 else "❌"
        table.add_row(
            str(idx), task.task, f"[{clr}]{task.category}[/{clr}]", is_done_str
        )
    console.print(table)


if __name__ == "__main__":
    app()
