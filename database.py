import datetime
import sqlite3
from typing import List

from model import Todo

conn = sqlite3.connect("todo.db")
c = conn.cursor()


def create_table():
    c.execute(
        """CREATE TABLE IF NOT EXISTS todo (
            task text,
            category text,
            date_added text,
            date_completed text,
            status integer,
            position integer
        )"""
    )


create_table()


def insert_todo(todo: Todo):
    c.execute("SELECT count(*) FROM todo")
    count = c.fetchone()[0]
    todo.positon = count if count else 0
    with conn:
        c.execute(
            "INSERT INTO todo VALUES (:task, :category, :date_added, :date_completed, :status, :position)",
            {
                "task": todo.task,
                "category": todo.category,
                "date_added": todo.date_added,
                "date_completed": todo.date_completed,
                "status": todo.status,
                "position": todo.position,
            },
        )


def get_all_todos() -> List[Todo]:
    c.execute("SELECT * FROM todo")
    results = c.fetchall()
    todos = []
    for result in results:
        todos.append(Todo(*result))
    return todos


def delete_todo(position):
    c.execute("SELECT count(*) FROM todo")
    count = c.fetchone()[0]

    with conn:
        c.execute("DELETE FROM todo WHERE position=:position", {"position": position})
        for pos in range(position + 1, count):
            change_position(pos, pos - 1, False)


def change_position(old_position: int, new_position: int, commit: True):
    c.execute(
        "Update todo SET position=:new_position WHERE position=:old_position",
        {"position": old_position, "new_position": new_position},
    )
    if commit:
        conn.commit()


def update_todo(psoition: int, task: str, category: str):
    with conn:
        if task is not None and category is not None:
            c.execute(
                "UPDATE todo SET task=:task, category=:category WHERE position=:position",
                {"task": task, "category": category, "position": psoition},
            )
        elif task is not None:
            c.execute(
                "UPDATE todo SET task=:task WHERE position=:position",
                {"task": task, "position": psoition},
            )
        elif category is not None:
            c.execute(
                "UPDATE todo SET category=:category WHERE position=:position",
                {"category": category, "position": psoition},
            )


def complete_todo(position: int):
    with conn:
        c.execute(
            "UPDATE todo SET status=2, date_completed=:date_completed WHERE position=:position",
            {
                "date_completed": datetime.datetime.now().isoformat(),
                "position": position,
            },
        )
