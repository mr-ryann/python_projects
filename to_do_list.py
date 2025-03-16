import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Function to add a task to the list
def add_task():
    task = entry.get().strip()
    if task:
        tasks = task_listbox.get(0, tk.END)
        timestamp = datetime.now().strftime("%m/%d/%Y, %I:%M %p")
        # Build full task with priority if checked
        full_task = f"[!] {task} - {timestamp}" if priority_var.get() else f"{task} - {timestamp}"
        # Check for duplicates by stripping prefixes and timestamp
        base_tasks = [t.split(" - ")[0].replace("[!] ", "").replace("[Done] ", "") for t in tasks]
        if task not in base_tasks:
            task_listbox.insert(tk.END, full_task)
            entry.delete(0, tk.END)
            task_count.config(text=f"Tasks: {task_listbox.size()}")
        else:
            messagebox.showinfo("Info", "Task already exists!")
    else:
        messagebox.showwarning("Warning", "Please enter a task!")

def edit_task():
    try:
        index = task_listbox.curselection()[0]
        full_task = task_listbox.get(index)
        # Extract base task by removing [Done], [!], and timestamp
        base_task = full_task.replace("[Done] ", "").replace("[!] ", "").split(" - ")[0]
        entry.delete(0, tk.END)
        entry.insert(0, base_task)
        task_listbox.delete(index)
        task_count.config(text=f"Tasks: {task_listbox.size()}")
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to edit!")
        
def load_tasks():
    try:
        with open("to_do_list/tasks.txt", "r") as file:
            tasks = file.readlines()
            for task in tasks:
                task_listbox.insert(tk.END, task.strip())
        task_count.config(text=f"Tasks: {task_listbox.size()}")
    except FileNotFoundError:
        pass  # No file yet, do nothing

def save_tasks():
    with open("to_do_list/tasks.txt", "w") as file:
        tasks = task_listbox.get(0, tk.END)
        for task in tasks:
            file.write(task + "\n")

# Function to remove a selected task
def remove_task():
    try:
        selected_index = task_listbox.curselection()[0]  # Get index of selected task
        task_listbox.delete(selected_index)  # Remove the task from listbox
        task_count.config(text=f"Tasks: {task_listbox.size()}")
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to remove!")

# Function to clear all tasks
def clear_tasks():
    if task_listbox.size() > 0:  # Check if there are tasks
        response = messagebox.askyesno("Confirm", "Clear all tasks?")
        task_count.config(text=f"Tasks: {task_listbox.size()}")
        if response:
            task_listbox.delete(0, tk.END)  # Clear all tasks
            task_count.config(text=f"Tasks: {task_listbox.size()}")
    else:
        messagebox.showinfo("Info", "No tasks to clear!")
        
def mark_complete():
    try:
        index = task_listbox.curselection()[0]
        task = task_listbox.get(index)
        if not task.startswith("[Done]"):
            # Preserve [!] if present
            new_task = f"[Done] {task}"
            task_listbox.delete(index)
            task_listbox.insert(index, new_task)
        else:
            # Remove [Done] but keep [!] and timestamp
            new_task = task.replace("[Done] ", "")
            task_listbox.delete(index)
            task_listbox.insert(index, new_task)
        task_count.config(text=f"Tasks: {task_listbox.size()}")
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to mark!")

# Set up the main window
window = tk.Tk()
window.title("To-Do List Manager")
window.geometry("800x400")

task_count = tk.Label(window, text="Tasks: 0", font=("Arial", 10))
task_count.pack(pady=5)

# Create and pack widgets
label = tk.Label(window, text="Enter a Task:", font=("Arial", 12))
label.pack(pady=10)

entry = tk.Entry(window, width=25)
entry.pack(pady=5)

priority_var = tk.IntVar()
priority_check = tk.Checkbutton(window, text="High Priority", variable=priority_var)
priority_check.pack(pady=5)

add_button = tk.Button(window, text="Add Task", command=add_task)
add_button.pack(pady=5)

remove_button = tk.Button(window, text="Remove Selected", command=remove_task)
remove_button.pack(pady=5)

clear_button = tk.Button(window, text="Clear All", command=clear_tasks)
clear_button.pack(pady=5)

mark_button = tk.Button(window, text="Mark Complete", command=mark_complete)
mark_button.pack(pady=5)

edit_button = tk.Button(window, text="Edit Selected", command=edit_task)
edit_button.pack(pady=5)

task_listbox = tk.Listbox(window, height=15, width=30)
task_listbox.pack(pady=10)
load_tasks()  # Load tasks on startup

# Bind Enter key to add_task function
window.bind('<Return>', lambda event: add_task())
window.protocol("WM_DELETE_WINDOW", lambda: [save_tasks(), window.destroy()])
window.bind('<Delete>', lambda event: remove_task())

# Start the main event loop
window.mainloop()
