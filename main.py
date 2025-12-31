import json
from datetime import datetime
import os
import itertools


STATUS = ["todo", "in-progress", "done"]
key = itertools.count()

def load_json() -> list:
    # checks if the JSON file does not exist or is empty
    if not os.path.exists("database.json") or os.path.getsize("database.json") == 0:
        empty_list = []
        with open("database.json", "w") as empty_json:
            json.dump(empty_list, empty_json, indent=4)

    # Loads JSON file for editing from the file object
    with open("database.json") as read_json:
        tasks = json.load(read_json)

    return tasks

def task_id_is_invalid(task_id) -> bool:
    try:
        int(task_id)
    except ValueError:
        return True
    return False

def add_task(desc: str) -> None:
    tasks = load_json()

    # Opens JSON file to write into it
    with open("database.json", "w") as write_json:
        created_at = datetime.now()
        created_at = created_at.strftime("%Y/%m/%d %H:%M:%S")

        task = {
            "id": next(key),
            "description": desc,
            "status": "to-do",
            "createdAt": created_at,
            "updatedAt": "-"
        }
        # Adds tasks to a loaded JSON file
        tasks.append(task)

        # write the JSON file back into a file object
        json.dump(tasks, write_json, indent=4)
    print(f"Task added successfully ID: {task["id"]}")


def update_task(task_id: str, desc: str):
    if task_id_is_invalid(task_id):
        raise ValueError("Invalid Task ID")

    tasks = load_json()
    for task in tasks:
        if task_id == task["id"]:
            break
    else:
        raise ValueError(f"Task with ID {task_id} not found")

    with open("database.json","w") as update_json:
        for task in tasks:
            if task["id"] == int(task_id):
                updated_at = datetime.now()
                updated_at = updated_at.strftime("%Y/%m/%d %H:%M:%S")

                task["description"] = desc
                task["updatedAt"] = updated_at
                print("Task Successfully Updated")
        json.dump(tasks, update_json, indent=4)


def delete_task(task_id: int):
    if task_id_is_invalid(task_id):
        raise ValueError("Invalid User ID")

    tasks = load_json()
    with open("database.json","w") as delete_json:
        for task in tasks:
            if task["id"] == int(task_id):
                tasks.remove(task)
                print("Task successfully deleted")
                break
        else:
            raise ValueError(f"Task with ID {task_id} not found")

        json.dump(tasks, delete_json, indent=4)

def mark_in_progress(task_id: str):
    if task_id_is_invalid(task_id):
        raise ValueError("Invalid Task ID")

    tasks = load_json()
    with open("database.json", "w") as mark_json:
        for task in tasks:
            if task["id"] == int(task_id):
                task["status"] = "in-progress"
                break
        else:
            raise ValueError(f"Task with ID {task_id} not found")

        json.dump(tasks, mark_json, indent= 4)


def mark_done(task_id: str):
    if task_id_is_invalid(task_id):
        raise ValueError("Invalid Task ID")

    tasks = load_json()
    for task in tasks:
        if task

    with open("database.json", "w") as mark_json:
        for task in tasks:
            if task["id"] == int(task_id):
                task["status"] = "done"
        json.dump(tasks, mark_json, indent= 4)


def list_task(status = None) -> None:
    if status is not None and status not in STATUS:
        raise ValueError("Invalid Status, type **help** to see available statuses")

    if json_is_empty():
        print("No tasks found...")
        return None

    tasks = load_json()
    print("=" * 115)
    print(f"{"ID":5} ¦{"DESCRIPTION":^50} ¦{"STATUS":^15} ¦{"TIME CREATED":^19} ¦{"TIME UPDATED":^15}")
    print("=" * 115)

    if status is None:
        for task in tasks:
            print(f"{task["id"]:<5} ¦{task["description"]:^50} ¦{task["status"]:^15} ¦{task["createdAt"]:^15} ¦{task["updatedAt"]:^15}")
            print("-" * 115)
    elif status is not None:
        count = True
        for task in tasks:
            if status == task["status"]:
                count = False
                break
        if count:
            print(f"Task with {status} not present")
            return None

        for task in tasks:
            if task["status"] == status:
                print(f"{task["id"]:<5} ¦{task["description"]:^50} ¦{task["status"]:^15} ¦{task["createdAt"]:15} ¦{task["updatedAt"]:^15}")
                print("-" * 115)


def helper() -> None:
    print("Commands:")
    print("     *add* {descr} => Adds a task with a description as an argument")
    print("     *update* {id} {descr} => Updates a task with the id of the task and the description you want to change it to.")
    print("     *list* {status} => List all task by default. You can optionally list by the status")
    print("     *delete* {id} => deletes a task")
    print("     *mark-in-progress* => Updates the status of a task to in-progress")
    print("     *mark-done* => Updates the status of a task to done")
    print("     *exit* => Exits the task manager")
    print("     *help* => Lists all commands")
    print("     POSSIBLE STATUSES => todo (default), in-progress, done")


def check_instruction_valid(line: list) -> bool:
    commands = ["add", "update", "list", "delete", "mark-in-progress", "mark-done", "exit", "help"]
    operand = line[0]

    if operand not in commands:
        raise ValueError("Invalid command")

    if operand  == "add" and len(line) < 2:
        raise
    if operand == "update":
        if len(line) < 3:
            print("Invalid argument")

def main():
    pass

if __name__ == "__main__":
    print("Welcome to the Task Manager, type help to check the commands")
    print("-" * 60)

    while True:
        instruction = input("task-cli ")
        parts = instruction.split(" ")
        command = parts[0].lower()



        if command == "add" :
            description = " ".join(parts[1:])
            add_task(description)

        elif command == "update":
            t_id = parts[1]
            description =  " ".join(parts[2:])
            update_task(t_id, description)

        elif command == "delete":
            if len(parts) != 2:
                print("Invalid argument")
                continue
            t_id = parts[1]
            delete_task(t_id)

        elif command == "list":
            if len(parts) == 2:
                t_id = parts[1]
                list_task(t_id)
            elif len(parts) == 1:
                list_task()
            else:
                print("Invalid argument")

        elif command == "mark-in-progress":
            if len(parts) != 2:
                print("Invalid Argument")

            mark_in_progress(parts[1])

        elif command == "mark-done":
            mark_done(parts[1])

        elif command == "help":
            helper()
        elif command == "exit":
            print("Bye, See you later")
            break
