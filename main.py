import json
from datetime import datetime
import os
import itertools

STATUS = ["in-progress", "done"]
key = itertools.count()

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

        job = {
            "id": next(key),
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

def mark_done(task_list: list, task_id: str):
    with open("database.json", "w") as mark_json:
        for job in task_list:
            if job["id"] == task_id:
                job["status"] = "done"
                break
        json.dump(task_list, mark_json, indent= 4)


def list_task(task_list: list, status = None):
    if status is not None and status not in STATUS:
        raise ValueError("Invalid Status, type **help** to see available statuses")

    print("=" * 115)
    print(f"{"ID":5} ¦{"DESCRIPTION":^50} ¦{"STATUS":^15} ¦{"TIME CREATED":^19} ¦{"TIME UPDATED":^15}")
    print("=" * 115)

    if status is None:
        for job in task_list:
            print(f"{job["id"]:<5} ¦{job["description"]:^50} ¦{job["status"]:^15} ¦{job["createdAt"]:^15} ¦{job["updatedAt"]:^15}")
            print("-" * 115)
    elif status is not None:
        count = True
        for job in task_list:
            if status == job["status"]:
                count = False
                break
        if count:
            print(f"Task with {status} not present")
            return None

        for job in task_list:
            if job["status"] == status:
                print(f"{job["id"]:<5} ¦{job["description"]:^50} ¦{job["status"]:^15} ¦{job["createdAt"]:15} ¦{job["updatedAt"]:^15}")
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

        if len(tasks) == 0 and command in ["update", "delete", "mark-in-progress", "mark-done", "list"]:
            print("No tasks available, add a task before using this command")
            continue

        if command in ["update", "delete", "mark-in-progress", "mark-done"]:
            t_id = args[0]
            try:
                t_id = int(t_id)
            except ValueError:
                print("Invalid Task ID")
                continue

            if t_id < 0:
                print("Task ID must be greater than 0")
                continue

            for task in tasks:
                if t_id == task["id"]:
                    break
            else:
                print(f"Task with id {t_id} doesn't exist")
                continue

        if command in ["mark-done","mark-in-progress", "delete", "list"] and len(args) > 1:
            print("Invalid Argument")
            continue

        if command in ["add", "update"]:
            if command == "add":
                description = " ".join(args)
            else:
                description = " ".join(args[2:])


        if command == "add":
            add_task(tasks,description)
        elif command == "update":
            update_task(tasks, t_id, description)
        elif command == "delete":
            delete_task(tasks, t_id)
        elif command == "mark-in-progress":
            mark_in_progress(tasks, t_id)
        elif command == "mark-done":
            mark_done(tasks, t_id)
        elif command == "list":
            list_task(tasks, )
        elif command == "help":
            helper()
        elif command == "exit":
            print("Bye Bye👋")
            break
        else:
            print("Invalid command")