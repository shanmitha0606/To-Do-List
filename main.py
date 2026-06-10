import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NAME = "tasks.json"


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Task Manager")
        self.root.geometry("650x900")
        self.root.configure(bg="#0D0C43")
        self.root.resizable(False, False)

        self.tasks = []
        self.load_tasks()

        title = tk.Label(
            root,
            text="✨ Task Manager",
            font=("Segoe UI", 24, "bold"),
            fg="white",
            bg="#1E1E2F"
        )
        title.pack(pady=15)

        input_frame = tk.Frame(root, bg="#1E1E2F")
        input_frame.pack(pady=10)

        self.task_entry = tk.Entry(
            input_frame,
            width=30,
            font=("Segoe UI", 13),
            bd=0
        )
        self.task_entry.grid(row=0, column=0, padx=10)

        add_btn = tk.Button(
            input_frame,
            text="➕ Add Task",
            command=self.add_task,
            bg="#4CAF50",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=15,
            pady=5
        )
        add_btn.grid(row=0, column=1)

        list_frame = tk.Frame(root, bg="#1E1E2F")
        list_frame.pack(pady=15)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox = tk.Listbox(
            list_frame,
            width=50,
            height=18,
            font=("Segoe UI", 12),
            bg="white",
            fg="#333333",
            selectbackground="#6A5ACD",
            activestyle="none",
            yscrollcommand=scrollbar.set
        )
        self.task_listbox.pack()

        scrollbar.config(command=self.task_listbox.yview)

        button_frame = tk.Frame(root, bg="#1E1E2F")
        button_frame.pack(pady=10)

        complete_btn = tk.Button(
            button_frame,
            text="✅ Complete",
            command=self.complete_task,
            bg="#2196F3",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=15,
            pady=5
        )
        complete_btn.grid(row=0, column=0, padx=8)

        undo_btn = tk.Button(
            button_frame,
            text="↩ Undo",
            command=self.undo_task,
            bg="#FF9800",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=15,
            pady=5
        )
        undo_btn.grid(row=0, column=1, padx=8)

        delete_btn = tk.Button(
            button_frame,
            text="🗑 Delete",
            command=self.delete_task,
            bg="#F44336",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=15,
            pady=5
        )
        delete_btn.grid(row=0, column=2, padx=8)

        self.counter_label = tk.Label(
            root,
            text="📋 Total: 0 | ✅ Completed: 0",
            font=("Segoe UI", 12, "bold"),
            fg="white",
            bg="#1E1E2F"
        )
        self.counter_label.pack(pady=10)

        footer = tk.Label(
            root,
            text="Built with Python & Tkinter",
            font=("Segoe UI", 9),
            fg="lightgray",
            bg="#1E1E2F"
        )
        footer.pack(side="bottom", pady=10)

        self.refresh_listbox()

    def add_task(self):
        task = self.task_entry.get().strip()

        if not task:
            messagebox.showwarning(
                "Warning",
                "Please enter a task!"
            )
            return

        self.tasks.append({
            "task": task,
            "completed": False
        })

        self.task_entry.delete(0, tk.END)
        self.save_tasks()
        self.refresh_listbox()

    def complete_task(self):
        try:
            selected = self.task_listbox.curselection()[0]
            self.tasks[selected]["completed"] = True

            self.save_tasks()
            self.refresh_listbox()

        except IndexError:
            messagebox.showwarning(
                "Warning",
                "Select a task first!"
            )

    def undo_task(self):
        try:
            selected = self.task_listbox.curselection()[0]
            self.tasks[selected]["completed"] = False

            self.save_tasks()
            self.refresh_listbox()

        except IndexError:
            messagebox.showwarning(
                "Warning",
                "Select a task first!"
            )

    def delete_task(self):
        try:
            selected = self.task_listbox.curselection()[0]

            del self.tasks[selected]

            self.save_tasks()
            self.refresh_listbox()

        except IndexError:
            messagebox.showwarning(
                "Warning",
                "Select a task first!"
            )

    def refresh_listbox(self):
        self.task_listbox.delete(0, tk.END)

        completed_count = 0

        for task in self.tasks:
            if task["completed"]:
                self.task_listbox.insert(
                    tk.END,
                    f"✅ {task['task']}"
                )
                completed_count += 1
            else:
                self.task_listbox.insert(
                    tk.END,
                    f"📝 {task['task']}"
                )

        self.counter_label.config(
            text=f"📋 Total: {len(self.tasks)} | ✅ Completed: {completed_count}"
        )

    def save_tasks(self):
        with open(FILE_NAME, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def load_tasks(self):
        if os.path.exists(FILE_NAME):
            try:
                with open(FILE_NAME, "r") as file:
                    self.tasks = json.load(file)
            except:
                self.tasks = []


root = tk.Tk()
app = TodoApp(root)
root.mainloop()