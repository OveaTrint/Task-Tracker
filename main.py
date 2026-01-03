import json
from datetime import datetime
import os
import id_counter

json_file = "database.json"

def load_json() -> list:
    # checks if the JSON file does not exist or is empty
    if not os.path.exists(json_file) or os.path.getsize(json_file) == 0:
        empty_list = []
        with open(json_file, "w") as empty_json:
            json.dump(empty_list, empty_json, indent=4)

    # Loads JSON file for editing from the file object
    with open(json_file) as read_json:
        jobs = json.load(read_json)

    return jobs

def add_task(task_list: list,desc: str) -> None:
    # Opens JSON file to write into it
    with open(json_file, "w") as write_json:
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
    with open(json_file,"w") as update_json:
        for job in task_list:
            if job["id"] == task_id:
                updated_at = datetime.now()
                updated_at = updated_at.strftime("%Y/%m/%d %H:%M:%S")

                job["description"] = desc
                job["updatedAt"] = updated_at
                break
        json.dump(task_list, update_json, indent=4)
        print("Task successfully updated")

def delete_task(task_list: list, task_id: int):
    with open(json_file,"w") as delete_json:
        for job in task_list:
            if job["id"] == task_id:
                task_list.remove(job)
                break
        json.dump(task_list, delete_json, indent=4)
        print("Task successfully deleted")

def mark_in_progress(task_list: list, task_id: int):
    with open(json_file, "w") as mark_json:
        for job in task_list:
            if job["id"] == task_id:
                job["status"] = "in-progress"
                break
        json.dump(task_list, mark_json, indent= 4)
        print("Task status changed successfully")

def mark_done(task_list: list, task_id: int):
    with open(json_file, "w") as mark_json:
        for job in task_list:
            if job["id"] == task_id:
                job["status"] = "done"
                break
        json.dump(task_list, mark_json, indent= 4)
        print("Task status changed successfully")

def list_task(task_list: list, status):
    print("id |  description  | status | createdAt | updatedAt")
    if status is None:
        for job in task_list:
            print(f"{job["id"]} | {job["description"]} | {job["status"]} | {job["createdAt"]} | {job["updatedAt"]}")
    else:
        for job in task_list:
            if job["status"] == status:
                print(f"{job["id"]} | {job["description"]} | {job["status"]} | {job["createdAt"]} | {job["updatedAt"]}")


def helper() -> None:
    print("Commands:")
    print("     *add* {descr} => Adds a task with a description as an argument")
    print("     *update* {id} {descr} => Updates a task with the id of the task and the description you want to change it to.")
    print("     *list* {status} => List all task by default. You can optionally list by the status")
    print("     *delete* {id} => deletes a task")
    print("     *mark-in-progress* {id} => Updates the status of a task to in-progress")
    print("     *exit* => Exits the task manager")
    print("     *help* => Lists all commands")
    print("     POSSIBLE STATUSES => todo(default), in-progress, done")

if __name__ == "__main__":
    print("Welcome to the Task Manager, type help to check the commands")
    print("-" * 60)

    commands = ["add", "update", "delete", "mark-done", "mark-in-progress", "list", "help", "exit"]
    STATUS = ["to-do", "in-progress", "done"]

    while True:
        tasks = load_json()
        instructions = input("task cli ")
        list_of_instructions = instructions.split(" ")
        command = list_of_instructions[0]
        args = []

        # Removes any whitespace
        for arg in list_of_instructions[1:]:
            if arg == "":
                continue
            args.append(arg)

        if command not in commands:
            print("Invalid Command")
            continue

        # checks the argument for each respective command
        if len(args) == 0 and command not in ["list", "exit", "help"]:
            print("No arguments added")
            continue
        elif command in ["exit", "help"] and len(args) > 0:
            print("help and exit take 0 arguments")
            continue
        elif command in ["delete", "mark-done", "mark-in-progress", "list"] and len(args) > 1:
            print("Only one argument needed")
            continue
        elif command == "update" and len(args) < 2:
            print("Not enough arguments provided ")
            continue

        # Error checks for the task_id related commands
        if command in ["delete", "mark-done", "mark-in-progress", "update"]:
            t_id = args[0]
            try:
                t_id = int(t_id)
                if t_id < 0:
                    print("Task ID cannot be less than zero ")
                    continue
                for task in tasks:
                    if t_id == task["id"]:
                        break
                else:
                    print(f"Task with ID {t_id} not found")
                    continue
            except ValueError:
                print("Invalid Task ID")
                continue
        # Error checks for the list command
        elif command == "list":
            item_status = None
            if len(args) == 1:
                item_status = args[0]

            if len(tasks) == 0:
                print("No tasks to list...")
                continue

            if item_status is not None:
                if item_status not in STATUS:
                    print("Invalid status, type help to see valid statuses")
                    continue
                for task in tasks:
                    if item_status == task["status"]:
                        break
                else:
                    print(f"No task has status {item_status}")
                    continue

        if command == "add":
            description = " ".join(args)
            add_task(tasks,description)
        elif command == "update":
            description = " ".join(args[1:])
            update_task(tasks, t_id, description)
        elif command == "delete":
            delete_task(tasks, t_id)
        elif command == "mark-in-progress":
            mark_in_progress(tasks, t_id)
        elif command == "mark-done":
            mark_done(tasks, t_id)
        elif command == "list":
            list_task(tasks, item_status)
        elif command == "help":
            helper()
        elif command == "exit":
            print("Bye Bye👋")
            break