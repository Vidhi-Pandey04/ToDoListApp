import tkinter as tk
from tkinter import messagebox
import datetime
import json
import os

data_file="tasks.json"

def load_tasks():
    if os.path.exists(data_file):
        try:
            with open(data_file,"r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return{}
    return{}

def save_tasks_to_file():
    with open(data_file, "w") as f:
        json.dump(all_tasks, f, indent=4)

def auto_save_task(date, task, completed=False):
    if date not in all_tasks:
        all_tasks[date] = []
    all_tasks[date].append({"task": task, "completed": completed})
    save_tasks_to_file()

def add_task():
    task_text = task_entry.get().strip()
    task_date = date_entry.get().strip()

    if not task_text:
        messagebox.showwarning("Warning", "Please enter a task.")
        return

    if not task_date:
        messagebox.showwarning("Warning", "Please enter a date.")
        return

    try:
        datetime.datetime.strptime(task_date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Invalid Date", "Enter date in YYYY-MM-DD format.")
        return

    # Create task checkbox
    task_var = tk.BooleanVar()
    task_check = tk.Checkbutton(task_frame, text=f"{task_text}  ({task_date})", variable=task_var, bg="#ffffff", anchor="w", padx=10)
    task_check.pack(fill="x", pady=2)

    # Append to list
    tasks_displayed.append((task_text, task_date, task_var, task_check))

    # Save to JSON
    auto_save_task(task_date, task_text, completed=task_var.get())

    # Clear the entry box
    task_entry.delete(0, tk.END)


def manual_save():
    # Update JSON with checkbox states
    for task_text, task_date, task_var, _  in tasks_displayed:
        for task in all_tasks.get(task_date, []):
            if task["task"] == task_text:
                task["completed"] = task_var.get()
    save_tasks_to_file()
    messagebox.showinfo("Saved", "All tasks saved successfully.")

def show_completed_tasks():
    for task_text, task_date, task_var, widget in tasks_displayed:
        if task_var.get():
            widget.pack(fill="x", pady=2)
        else:
             widget.pack_forget()

def show_incomplete_tasks():
    for task_text, task_date, task_var, widget in tasks_displayed:
        if not task_var.get():
            widget.pack(fill="x", pady=2)
        else:
            widget.pack_forget()

def display_tasks_by_date():
    for widget in task_frame.winfo_children():
        widget.destroy()
    tasks_displayed.clear()

    selected_date = date_entry.get().strip()
    if selected_date not in all_tasks:
        messagebox.showinfo("No Tasks", f"No tasks found for {selected_date}")
        return

    for task in all_tasks[selected_date]:
        var = tk.BooleanVar(value=task["completed"])
        chk = tk.Checkbutton(task_frame, text=task["task"], variable=var, bg="#ffffff", anchor="w", padx=10)
        chk.pack(fill="x", pady=2)
        tasks_displayed.append((task["task"], selected_date, var,chk))

def show_all_tasks():
    for widget in task_frame.winfo_children():
        widget.destroy()
    tasks_displayed.clear()

    for date in all_tasks:
        for task in all_tasks[date]:
            var = tk.BooleanVar(value=task["completed"])
            chk = tk.Checkbutton(task_frame, text=f"{task['task']}  ({date})", variable=var, bg="#ffffff", anchor="w", padx=10)
            chk.pack(fill="x", pady=2)
            tasks_displayed.append((task["task"], date, var,chk))

def delete_selected_tasks():
    global tasks_displayed
    remaining_tasks = []

    for task_text, task_date, task_var, widget in tasks_displayed:
        if task_var.get():  # If checked (completed)
            widget.destroy()
            # Remove from all_tasks
            if task_date in all_tasks:
                all_tasks[task_date] = [t for t in all_tasks[task_date] if t["task"] != task_text]

            # Clean up empty date
            if not all_tasks[task_date]:
                del all_tasks[task_date]
        else:
            remaining_tasks.append((task_text, task_date, task_var, widget))

    tasks_displayed = remaining_tasks
    save_tasks_to_file()
    messagebox.showinfo("Deleted", "Selected completed tasks have been deleted.")

    task_var = tk.BooleanVar()
    task_check = tk.Checkbutton(task_frame, text=f"{task_text}  ({task_date})", variable=task_var, bg="#ffffff", anchor="w", padx=10)
    task_check.pack(fill="x", pady=2)
    tasks_displayed.append((task_text, task_date, task_var,task_check))

    task_entry.delete(0, tk.END)  # Clear task entry after adding

all_tasks=load_tasks()

# Create the main window
window = tk.Tk()
window.title("To-Do List App")
window.geometry("500x500")
window.configure(bg="#f9f9f9")
default_font = ("Segoe UI", 10)
heading_font = ("Segoe UI", 12, "bold")

# Date Label
date_label = tk.Label(window, text="Enter Date (YYYY-MM-DD):", bg="#ffffff")
date_label.pack(pady=(10, 0))

# Date Entry
date_entry = tk.Entry(window, font=("Segoe UI", 10), bg="#ffffff", bd=1, relief="solid")
date_entry.insert(0, datetime.date.today().isoformat())  # default to today
date_entry.pack(pady=5)

tk.Label(window, text="📝 To-Do List", font=("Segoe UI", 16, "bold"), bg="#f4f6f8", fg="#333333").pack(pady=10)

# Task Entry
task_entry = tk.Entry(window, font=("Segoe UI", 10), width=35, relief="flat", bd=2, highlightthickness=1, highlightcolor="#999", highlightbackground="#ccc")
task_entry.pack(pady=10)


btn_style = {
    "font": ("Segoe UI", 7),        # Smaller font
    "padx": 7,                      # Less horizontal padding
    "pady": 3,                      # Less vertical padding
    "relief": "raised",             # Or "flat" for cleaner look
    "bd": 1                         # Thin border
}



# Create a frame for the button row
button_row = tk.Frame(window, bg="#f9f9f9")
button_row.pack(pady=5)

# Add Task Button
add_task_button = tk.Button(button_row, text="Add Task", command=add_task, bg="#4caf50",**btn_style)
add_task_button.pack(side="left", padx=5)

# Manual Save Button
manual_save_button = tk.Button(button_row, text="Manual Save", command=manual_save, bg="#4caf50", **btn_style)
manual_save_button.pack(side="left", padx=5)


# Frame for "Display Tasks" and "Show All Tasks" buttons
view_buttons_frame = tk.Frame(window, bg="#f9f9f9")
view_buttons_frame.pack(pady=5)

display_button = tk.Button(view_buttons_frame, text="Display Tasks", command=display_tasks_by_date, bg="#a8dadc",**btn_style)
display_button.pack(side="left", padx=10)

show_all_button = tk.Button(view_buttons_frame, text="Show All Tasks", command=show_all_tasks, bg="#a8dadc",**btn_style)
show_all_button.pack(side="left", padx=10)

complete_button_frame=tk.Frame(window,bg="#f9f9f9")
complete_button_frame.pack(pady=5)

show_complete_button=tk.Button(complete_button_frame, text="Show Completed Tasks", command=show_completed_tasks, bg="#f0a0cf",**btn_style).pack(side="left",padx=5)
show_incomplete_button=tk.Button(complete_button_frame, text="Show Incomplete Tasks", command=show_incomplete_tasks, bg="#f0a0cf",**btn_style).pack(side="left",padx=5)

tk.Button(window, text="Delete Selected Tasks", command=delete_selected_tasks, bg="#e63946",**btn_style).pack(pady=5)

# Task Display Frame
task_frame = tk.Frame(window, bg="#FFD1DC", bd=1, relief="sunken", highlightbackground="#dcdcdc", highlightthickness=1)
task_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Placeholder: for displaying tasks later
tasks_displayed = []
# display previously saved tasks
for date in all_tasks:
    for task in all_tasks[date]:
        var = tk.BooleanVar(value=task["completed"])
        chk = tk.Checkbutton(task_frame, text=f"{task['task']}  ({date})", variable=var,font=("Segoe UI", 10), bg="#ffffff", anchor="w", padx=10,
                             relief="flat", highlightthickness=0)
        chk.pack(fill="x", pady=2)
        tasks_displayed.append((task["task"], date, var,chk))

# Run the GUI
window.mainloop()
