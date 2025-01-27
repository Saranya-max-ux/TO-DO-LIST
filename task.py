import sqlite3
from tkinter import *
from tkinter import messagebox

conn = sqlite3.connect("todo_advanced.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    due_date DATE,
    status TEXT DEFAULT 'Pending'
)
""")
conn.commit()

def add_task():
    title = title_entry.get()
    description = description_entry.get("1.0", END).strip()
    due_date = due_date_entry.get()

    if not title or not due_date:
        messagebox.showerror("Error", "Title and Due Date are required!")
        return

    cursor.execute("INSERT INTO tasks (title, description, due_date) VALUES (?, ?, ?)", (title, description, due_date))
    conn.commit()
    refresh_tasks()
    clear_fields()

def refresh_tasks():
    task_list.delete(0, END)
    cursor.execute("SELECT id, title, due_date, status FROM tasks")
    for task in cursor.fetchall():
        task_list.insert(END, f"{task[0]}: {task[1]} - {task[2]} ({task[3]})")

def delete_task():
    selected_task = task_list.get(ACTIVE)
    if not selected_task:
        messagebox.showerror("Error", "No task selected!")
        return
    task_id = selected_task.split(":")[0]
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    refresh_tasks()

def mark_complete():
    selected_task = task_list.get(ACTIVE)
    if not selected_task:
        messagebox.showerror("Error", "No task selected!")
        return
    task_id = selected_task.split(":")[0]
    cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
    conn.commit()
    refresh_tasks()

def clear_fields():
    title_entry.delete(0, END)
    description_entry.delete("1.0", END)
    due_date_entry.delete(0, END)

app = Tk()
app.title("Advanced To-Do List")
app.geometry("600x500")
app.resizable(False, False)

Label(app, text="Title:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
title_entry = Entry(app, width=40)
title_entry.grid(row=0, column=1, padx=10, pady=10)

Label(app, text="Description:").grid(row=1, column=0, padx=10, pady=10, sticky=NW)
description_entry = Text(app, width=30, height=5)
description_entry.grid(row=1, column=1, padx=10, pady=10)

Label(app, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10, sticky=W)
due_date_entry = Entry(app, width=20)
due_date_entry.grid(row=2, column=1, padx=10, pady=10, sticky=W)

Button(app, text="Add Task", command=add_task, bg="green", fg="white").grid(row=3, column=0, pady=10, sticky=E)
Button(app, text="Delete Task", command=delete_task, bg="red", fg="white").grid(row=3, column=1, pady=10, sticky=W)
Button(app, text="Mark Completed", command=mark_complete, bg="blue", fg="white").grid(row=3, column=1, pady=10)

Label(app, text="Tasks:").grid(row=4, column=0, padx=10, pady=10, sticky=W)
task_list = Listbox(app, width=70, height=15)
task_list.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

refresh_tasks()
app.mainloop()
conn.close()
