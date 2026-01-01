import json
from datetime import datetime
import os

import id_counter

STATUS = ["in-progress", "done"]

def load_json() -> list:
    # checks if the JSON file does not exist or is empty
    if not os.path.exists("database.json") or os.path.getsize("database.json") == 0:
        empty_list = []
        with open("database.json", "w") as empty_json:
            json.dump(empty_list, empty_json, indent=4)

    # Loads JSON file for editing from the file object
    with open("database.json") as read_json:
        jobs = json.load(read_json)

    return jobs

def add_task(task_list: list,desc: str) -> None:
    # Opens JSON file to write into it
    with open("database.json", "w") as write_json:
        created_at = datetime.now()
        created_at = created_at.strftime("%Y/%m/%d %H:%M:%S")
        task_id = id_counter.get_next_id()

        job = {
            "id": task_id,
            "description": desc,
            "status": "to-do",
            "createdAt": created_at,
            "updatedAt": "-"
        }
        # Adds tasks to a loaded JSON file
        task_list.append(job)

        # write the JSON file back into a file object
        json.dump(task_list, write_json, indent=4)
    print(f"Task added successfully ID: {job["id"]}")

def update_task(task_list: list,task_id: int, desc: str):
    with open("database.json","w") as update_json:
        for job in task_list:
            if job["id"] == task_id:
                updated_at = datetime.now()
                updated_at = updated_at.strftime("%Y/%m/%d %H:%M:%S")

                job["description"] = desc
                job["updatedAt"] = updated_at
                break
        print("Task Successfully Updated")
        json.dump(task_list, update_json, indent=4)

def delete_task(task_list: list, task_id: int):
    with open("database.json","w") as delete_json:
        for job in task_list:
            if job["id"] == task_id:
                task_list.remove(job)
                print("Task successfully deleted")
                break
        json.dump(task_list, delete_json, indent=4)

def mark_in_progress(task_list: list, task_id: int):
    with open("database.json", "w") as mark_json:
        for job in task_list:
            if job["id"] == task_id:
                job["status"] = "in-progress"
                break
        json.dump(task_list, mark_json, indent= 4)

def mark_done(task_list: list, task_id: int):
    with open("database.json", "w") as mark_json:
        for job in task_list:
            if job["id"] == task_id:
                job["status"] = "done"
                break
        json.dump(task_list, mark_json, indent= 4)


def list_task(task_list: list, status = None):
    if status is None:
        for job in task_list:
            print(f"{job["id"]}-{job["description"]}-{job["status"]}-{job["createdAt"]}-{job["updatedAt"]}")
    else:
        for job in task_list:
            if job["status"] == status:
                print(f"{job["id"]}-{job["description"]}-{job["status"]}-{job["createdAt"]}-{job["updatedAt"]}")


def helper() -> None:
    print("Commands:")
    print("     *add* {descr} => Adds a task with a description as an argument")
    print("     *update* {id} {descr} => Updates a task with the id of the task and the description you want to change it to.")
    print("     *list* {status} => List all task by default. You can optionally list by the status")
    print("     *delete* {id} => deletes a task")
    print("     *mark-in-progress* {id} => Updates the status of a task to in-progress")
    print("     *exit* => Exits the task manager")
    print("     *help* => Lists all commands")
    print("     POSSIBLE STATUSES => in-progress, done")

if __name__ == "__main__":
    print("Welcome to the Task Manager, type help to check the commands")
    print("-" * 60)

    while True:
        tasks = load_json()
        instructions = input("task cli ")

        list_of_instructions = instructions.split(" ")
        command = list_of_instructions[0]
        args = list_of_instructions[1:]

        if command == "add":
            description = " ".join(args).lstrip().rstrip()
            if len(description) == 0:
                print("No description added")
                continue
            add_task(tasks,description)
        elif command == "update":
            if len(args) < 2:
                print("Not enough arguments provided")
                continue

            try:
                t_id = int(args[0])
            except ValueError:
                print("Invalid Task ID")
                continue

            for task in tasks:
                if task["id"] == t_id:
                    break
            else:
                print(f"Task with ID {t_id} not found")
                continue

            description = " ".join(args[1:]).lstrip().rstrip()
            if len(description) == 0:
                print("No description added")
                continue
            update_task(tasks, t_id, description)

        elif command == "delete":
            if len(args) > 1:
                print("Only one argument (ID) needed")
                continue
            elif len(args) < 1:
                print("No argument found")
                continue

            try:
                t_id = int(args[0].lstrip())
            except ValueError:
                print("Invalid Task ID")
                continue

            for task in tasks:
                if t_id == task["id"]:
                    break
            else:
                print(f"Task with ID {t_id} not found")
                continue
            delete_task(tasks, t_id)
        elif command == "mark-in-progress":
            if len(args) > 1:
                print("Only one argument (ID) needed")
                continue
            elif len(args) < 1:
                print("No argument found")
                continue

            try:
                t_id = int(args[0].lstrip())
            except ValueError:
                print("Invalid Task ID")
                continue

            for task in tasks:
                if t_id == task["id"]:
                    break
            else:
                print(f"Task with ID {t_id} not found")
                continue
            mark_in_progress(tasks, t_id)
        elif command == "mark-done":
            if len(args) > 1:
                print("Only one argument (ID) needed")
                continue
            elif len(args) < 1:
                print("No argument found")
                continue
            try:
                t_id = int(args[0].lstrip())
            except ValueError:
                print("Invalid Task ID")
                continue

            for task in tasks:
                if t_id == task["id"]:
                    break
            else:
                print(f"Task with ID {t_id} not found")
                continue

            mark_done(tasks, t_id)
        elif command == "list":
            status_present = False
            if len(args) == 1:
                status_present = True
                status__ = args[0].lstrip()
            elif len(args) > 1:
                print("Invalid Argument")
                continue

            if status_present:
                if status__ not in STATUS:
                    print("Invalid status, only todo and in-progress are valid")
                    continue

                for task in tasks:
                    if status__ == task["status"]:
                        break
                else:
                    print(f"Task with {status__} is not available")
                    continue

                list_task(tasks, status__)
            else:
                list_task(tasks)
        elif command == "help":
            helper()
        elif command == "exit":
            print("Bye Bye👋")
            break
        else:
            print("Invalid command")