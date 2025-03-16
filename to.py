import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Functions
def add_task():
    task = entry.get().strip()
    if task:
        timestamp = datetime.now().strftime("%m/%d/%Y, %I:%M %p")
        full_task = f"[!] {task} - {timestamp}" if priority_var.get() else f"{task} - {timestamp}"
        base_tasks = [t.split(" - ")[0].replace("[!] ", "").replace("[Done] ", "") for t in task_listbox.get(0, tk.END)]
        if task not in base_tasks:
            task_listbox.insert(tk.END, full_task)
            entry.delete(0, tk.END)
            task_count.config(text=f"Tasks: {task_listbox.size()}")
        else:
            messagebox.showinfo("Info", "Task already exists!")
    else:
        messagebox.showwarning("Warning", "Please enter a task!")

def show_tasks():
    global task_window, task_listbox  # Make task_listbox accessible globally
    if 'task_window' not in globals() or not task_window.winfo_exists():
        # Create collapsible window
        task_window = tk.Toplevel(window)
        task_window.title("Tasks")
        task_window.geometry("400x400")
        task_window.configure(bg="#F0F0F0")

        # Task Listbox sorted by timestamp
        task_listbox = tk.Listbox(task_window, height=20, width=40, font=("Helvetica", 11), bg="#FFFFFF", fg="#333333")
        task_listbox.place(x=20, y=20)
        load_tasks()  # Load existing tasks
        sort_by_timestamp()  # Sort initially

        # Sidebar Buttons
        edit_button = tk.Button(task_window, text="Edit", command=edit_task, font=("Helvetica", 10), bg="#B48EAD", fg="white", relief="raised", width=10)
        edit_button.place(x=300, y=20)
        mark_button = tk.Button(task_window, text="Mark Done", command=mark_complete, font=("Helvetica", 10), bg="#88C0D0", fg="white", relief="raised", width=10)
        mark_button.place(x=300, y=60)
        clear_button = tk.Button(task_window, text="Clear All", command=clear_tasks, font=("Helvetica", 10), bg="#BF616A", fg="white", relief="raised", width=10)
        clear_button.place(x=300, y=100)

def sort_by_timestamp():
    tasks = list(task_listbox.get(0, tk.END))
    # Sort by timestamp (last part after " - ")
    tasks.sort(key=lambda x: datetime.strptime(x.split(" - ")[1], "%m/%d/%Y, %I:%M %p"), reverse=True)
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, task)
    task_count.config(text=f"Tasks: {task_listbox.size()}")

def edit_task():
    try:
        index = task_listbox.curselection()[0]
        full_task = task_listbox.get(index)
        base_task = full_task.replace("[Done] ", "").replace("[!] ", "").split(" - ")[0]
        entry.delete(0, tk.END)
        entry.insert(0, base_task)
        task_listbox.delete(index)
        task_count.config(text=f"Tasks: {task_listbox.size()}")
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to edit!")

def mark_complete():
    try:
        index = task_listbox.curselection()[0]
        task = task_listbox.get(index)
        if not task.startswith("[Done]"):
            new_task = f"[Done] {task}"
            task_listbox.delete(index)
            task_listbox.insert(index, new_task)
        else:
            new_task = task.replace("[Done] ", "")
            task_listbox.delete(index)
            task_listbox.insert(index, new_task)
        task_count.config(text=f"Tasks: {task_listbox.size()}")
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to mark!")

def clear_tasks():
    if task_listbox.size() > 0:
        response = messagebox.askyesno("Confirm", "Clear all tasks?")
        if response:
            task_listbox.delete(0, tk.END)
            task_count.config(text=f"Tasks: {task_listbox.size()}")
    else:
        messagebox.showinfo("Info", "No tasks to clear!")

def load_tasks():
    try:
        with open("tasks.txt", "r") as file:
            tasks = file.readlines()
            for task in tasks:
                task_listbox.insert(tk.END, task.strip())
        sort_by_timestamp()  # Sort after loading
    except FileNotFoundError:
        pass

def save_tasks():
    with open("tasks.txt", "w") as file:
        tasks = task_listbox.get(0, tk.END)
        for task in tasks:
            file.write(task + "\n")

# GUI Setup
window = tk.Tk()
window.title("To-Do List Manager")
window.geometry("200x400")  # Smaller main window
window.configure(bg="#F0F0F0")

# Left Side Elements
label = tk.Label(window, text="Enter Task", font=("Helvetica", 12), bg="#F0F0F0", fg="#333333")
label.place(x=20, y=20)

entry = tk.Entry(window, width=20, font=("Helvetica", 11), relief="flat", bg="#FFFFFF", fg="#333333")
entry.place(x=20, y=50)

priority_var = tk.IntVar()
priority_check = tk.Checkbutton(window, text="Priority", variable=priority_var, bg="#F0F0F0", fg="#666666", font=("Helvetica", 10))
priority_check.place(x=20, y=80)

add_button = tk.Button(window, text="Add", command=add_task, font=("Helvetica", 10), bg="#A3BE8C", fg="white", relief="raised", width=10)
add_button.place(x=20, y=110)

show_button = tk.Button(window, text="Show", command=show_tasks, font=("Helvetica", 10), bg="#81A1C1", fg="white", relief="raised", width=10)
show_button.place(x=20, y=150)

# Task Counter (optional, placed at bottom of main window)
task_count = tk.Label(window, text="Tasks: 0", font=("Helvetica", 10, "italic"), bg="#F0F0F0", fg="#666666")
task_count.place(x=20, y=350)

# Key Bindings
window.bind('<Return>', lambda event: add_task())

# Save on close
window.protocol("WM_DELETE_WINDOW", lambda: [save_tasks(), window.destroy()])

window.mainloop()
