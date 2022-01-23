import typer
from rich.console import Console
from rich.table import Table

console = Console()
app = typer.Typer()


@app.command(short_help="Adds the Task to the list")
def add(task: str, category: str):
    typer.echo(f"Adding task: {task} in category: {category}")
    show()


@app.command(short_help="Removes the Task from the list")
def remove(position: int):
    typer.echo(f"Removing task: {position}")
    show()


@app.command(short_help="Updates the task in the list")
def update(position: int, task: str, category: str):
    typer.echo(f"Updating task: {position} to {task} in category: {category}")
    show()


@app.command()
def complete(position: int):
    typer.echo(f"Marking completing task: {position} as completed")
    show()


@app.command()
def show():
    tasks = [
        ("Task 1", "Category 1"),
        ("Task 2", "Category 2"),
        ("Task 3", "Category 3"),
    ]

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
        clr = get_category_color(task[1])
        is_done_str = "✅" if True == 2 else "❌"
        table.add_row(str(idx), task[0], f"[{clr}]{task[1]}[/{clr}]", is_done_str)
    console.print(table)


if __name__ == "__main__":
    app()
