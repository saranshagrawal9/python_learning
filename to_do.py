# Simple To-Do List App (no external libraries)

tasks = []  # each task is a dict: {"title": str, "done": bool}


def show_menu():
    print("\n=== TO-DO LIST APP ===")
    print("1. Add task")
    print("2. List tasks")
    print("3. Mark task as done")
    print("4. Delete task")
    print("5. Clear all tasks")
    print("0. Exit")


def add_task():
    title = input("Enter task title: ").strip()
    if not title:
        print("Task title cannot be empty.")
        return
    tasks.append({"title": title, "done": False})
    print(f"Task added: {title}")


def list_tasks():
    if not tasks:
        print("No tasks yet. Add some!")
        return
    print("\nYour tasks:")
    for i, task in enumerate(tasks, start=1):
        status = "✓" if task["done"] else " "
        print(f"{i}. [{status}] {task['title']}")


def mark_done():
    if not tasks:
        print("No tasks to mark.")
        return
    list_tasks()
    try:
        idx = int(input("Enter task number to mark as done: "))
        if 1 <= idx <= len(tasks):
            tasks[idx - 1]["done"] = True
            print(f"Marked as done: {tasks[idx - 1]['title']}")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


def delete_task():
    if not tasks:
        print("No tasks to delete.")
        return
    list_tasks()
    try:
        idx = int(input("Enter task number to delete: "))
        if 1 <= idx <= len(tasks):
            removed = tasks.pop(idx - 1)
            print(f"Deleted: {removed['title']}")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


def clear_all():
    if not tasks:
        print("No tasks to clear.")
        return
    confirm = input("Are you sure you want to clear all tasks? (y/n): ").strip().lower()
    if confirm == "y":
        tasks.clear()
        print("All tasks cleared.")
    else:
        print("Cancelled.")


def main():
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            mark_done()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            clear_all()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
