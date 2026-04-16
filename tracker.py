import customtkinter as ctk
import json
import os

# Set the visual theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DailyTracker(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Daily Life Tracker")
        self.geometry("450x600")

        self.tasks = self.load_data()
        self.checkboxes = []

        # --- UI LAYOUT ---
        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text="My Daily Progress", font=("Helvetica", 24, "bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        # Progress Bar
        self.progress = ctk.CTkProgressBar(self, width=350)
        self.progress.grid(row=1, column=0, padx=20, pady=10)
        self.progress.set(0)

        # Scrollable Frame for Tasks
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Tasks for Today")
        self.scroll_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.grid_rowconfigure(2, weight=1)

        # Input Area
        self.entry = ctk.CTkEntry(self, placeholder_text="Enter a new habit/task...")
        self.entry.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.add_button = ctk.CTkButton(self, text="Add Task", command=self.add_task)
        self.add_button.grid(row=4, column=0, padx=20, pady=10)

        self.refresh_tasks()

    def load_data(self):
        if os.path.exists("data.json"):
            with open("data.json", "r") as f:
                return json.load(f)
        return []

    def save_data(self):
        with open("data.json", "w") as f:
            json.dump(self.tasks, f)

    def update_progress(self):
        if not self.tasks:
            self.progress.set(0)
            return
        completed = sum(1 for t in self.tasks if t["done"])
        self.progress.set(completed / len(self.tasks))

    def refresh_tasks(self):
        # Clear existing widgets
        for cb in self.checkboxes:
            cb.destroy()
        self.checkboxes = []

        # Re-build list
        for index, task in enumerate(self.tasks):
            cb = ctk.CTkCheckBox(
                self.scroll_frame,
                text=task["name"],
                command=lambda i=index: self.toggle_task(i)
            )
            if task["done"]:
                cb.select()
            cb.grid(row=index, column=0, padx=10, pady=5, sticky="w")
            self.checkboxes.append(cb)

        self.update_progress()
        self.save_data()

    def add_task(self):
        name = self.entry.get()
        if name:
            self.tasks.append({"name": name, "done": False})
            self.entry.delete(0, 'end')
            self.refresh_tasks()

    def toggle_task(self, index):
        # Update the boolean in our list
        self.tasks[index]["done"] = not self.tasks[index]["done"]
        self.update_progress()
        self.save_data()

if __name__ == "__main__":
    app = DailyTracker()
    app.mainloop()