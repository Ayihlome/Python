#!/usr/bin/env python3

from datetime import datetime
import os
import json
import argparse


# File management
file_path = "task.json"
# file_path2 = "TASKS.json"

if not os.path.exists(file_path):
    with open(file_path, "x+") as file:
        json.dump({"tasks": []}, file)  # creates file with JSON and empty task list

    

# Testing a function
def showAllTask():
    with open(file_path, "r+") as file:
        try:
           # Attempt to load existing data
           data = json.load(file)
        except json.JSONDecodeError:
           # Handle the case where the file is empty or contains invalid JSON
           data = {"tasks": []}

        tasks = data.get("tasks", [])
        for task in tasks:
            print(f"ID: {task['id']}  Task: {task['name']} status: {task['status']} created at: {task['createdAt']}")

        # Move the file pointer to the beginning before writing
        file.seek(0)
        # Write the updated data back to the file
        json.dump(data, file, indent=4)
        # Truncate the file to the current position to remove any leftover data
        file.truncate()


def addTask(task_name):
    with open(file_path, "r+") as file:
        try:
           # Attempt to load existing data
           data = json.load(file)
        except json.JSONDecodeError:
           # Handle the case where the file is empty or contains invalid JSON
           data = {"tasks": []}
        taskname = str(task_name)
        currentSat = "to do"
        # dynamic indexing
        tasks = data["tasks"]
        if (data == " "):
            Newindex = 1
        else:
           taskLength = len(tasks)
           Newindex = taskLength + 1

        tasks.append(
        {
            "id": Newindex,
            "name": taskname,
            "status": currentSat,
            "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "updatedAt": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    )
        
        # Move the file pointer to the beginning before writing
        file.seek(0)
        # Write the updated data back to the file
        json.dump(data, file, indent=4)
        # Truncate the file to the current position to remove any leftover data
        file.truncate()


    print(f"Task successfully added (ID: {Newindex})")


def markInProgress():
    taskID = int(input("Enter task ID: "))
    newStatus = "in-progress"
    with open(file_path, "r+") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {"tasks": []}
        tasks = data.get("tasks", [])
        if not tasks:
           print("No current tasks")
        if 0 < taskID <= len(tasks):
            if not tasks[taskID - 1]:
                print("Task not found")
            
            tasks[taskID -1].update(
                {"status": newStatus}, #Update status
            )
            tasks[taskID - 1].update(
                {"updatedAT": datetime.now().strftime("%Y-%m-%d %H:%M")} #update time
            )

            print("Status updated")
        else:
            print("Invalid task ID.")
        # Move the file pointer to the beginning before writing
        file.seek(0)
        # Write the updated data back to the file
        json.dump(data, file, indent=4)
        # Truncate the file to the current position to remove any leftover data
        file.truncate()


def markDone(task_id):
    taskID = int(task_id)
    newStatus = "done"
    with open(file_path, "r+") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {"tasks": []}
        
        tasks = data.get("tasks", [])

        if not tasks:
            print("No current tasks")
        
        if 0 < taskID <= len(tasks):
            if not tasks[taskID -1]:
                print("Task not found")
            
            tasks[taskID -1].update(
                {"status": newStatus}
            )

            tasks[taskID - 1].update(
                {"updatedAt": datetime.now().strftime('%Y-%m-%d %H:%M')}
            )

        print("Status updated")
        # Move the file pointer to the beginning before writing
        file.seek(0)
        # Write the updated data back to the file
        json.dump(data, file, indent=4)
        # Truncate the file to the current position to remove any leftover data
        file.truncate()


def deleteTask(task_id):
    taskID = int(task_id)
    with open(file_path, "r+") as file:
        try:
            data = json.load(file)
        except:
            data = {"tasks": []}
        tasks = data.get("tasks", [])
        if not tasks:
            print("No current tasks")
        if 0 < taskID <= len(tasks):
            if not tasks[taskID -1]:
                print("Task not found")

        tasks.pop(taskID -1)
        print("Task successfully removed")

         # Move the file pointer to the beginning before writing
        file.seek(0)
        # Write the updated data back to the file
        json.dump(data, file, indent=4)
        # Truncate the file to the current position to remove any leftover data
        file.truncate()
    


def listDone():
    status = "done"
    with open(file_path, "r+") as file:
        try:
            data=json.load(file)
        except json.JSONDecodeError:
            data = {"tasks": []}
        
        tasks = data.get("tasks", [])

        for task in tasks:
            if task["status"] == status:
                print(f"ID: {task['id']} Task: {task['name']}")
        
        # Move the file pointer to the beginning before writing
        file.seek(0)
        # Write the updated data back to the file
        json.dump(data, file, indent=4)
        # Truncate the file to the current position to remove any leftover data
        file.truncate()

def listInProgress():
    status = "in-progress"
    with open(file_path, "r+") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {"tasks": []}
        tasks = data.get("tasks", [])
        for task in tasks:
            if task["status"] == status:
                print(f"ID: {task['id']} Task: {task['name']}")
                
        # Move the file pointer to the beginning before writing
        file.seek(0)
        # Write the updated data back to the file
        json.dump(data, file, indent=4)
        # Truncate the file to the current position to remove any leftover data
        file.truncate()

def listToDo():
    status ="to do"
    with open(file_path, "r+") as file:
        try:
            data = json.load(file)
        except:
            data = {"tasks": []}
        tasks = data.get("tasks", [])
        for task in tasks:
            if task["status"] == status:
                print(f"ID: {task['id']} Task: {task['name']}")

# Adding arguments
parser = argparse.ArgumentParser(description="Task Tracker Command-Line Interface")
subparsers = parser.add_subparsers(dest='command', help='Available commands')


# ADD TASK  
parser_add = subparsers.add_parser('add', help='Add a new task')
parser_add.add_argument('task_name', type=str, help='Name of the task to add')

# MARK DONE
parser_done = subparsers.add_parser('done', help='Mark a task as done')
parser_done.add_argument('task_id', type=int, help='ID of the task to mark as done')

# DELETE
parser_delete = subparsers.add_parser('delete', help='Delete a task')
parser_delete.add_argument('task_id', type=int, help='ID of the task to delete')

# LISTS
parser_list = subparsers.add_parser('list', help="Lists all tasks")
parser_list.add_argument('--in-progress', action='store_true' , help="List all tasks with a 'in-progress' status")
parser_list.add_argument('--done', action='store_true', help="List all tasks with a 'done' status")
parser_list.add_argument('--todo', action='store_true', help="List all tasks with a 'to do' status")


# MARK IN PROGRESS
parser_inProgress = subparsers.add_parser('mark-in-progress', help="marks a task to 'in progress")
parser_inProgress.add_argument('task_id', type=int, help="enter the task id of deired task")

# 

if __name__ == "__main__":
    args = parser.parse_args()

    if args.command == 'add':
        addTask(args.task_name)
    elif args.command == 'done':
        markDone(args.task_id)
    elif args.command == 'delete':
        deleteTask(args.task_id)
    elif args.command == 'list':
        if args.in_progress:
            listInProgress()
        elif args.todo:
            listToDo()
        elif args.done:
            listDone()
        else:
            showAllTask()
    elif args.command == 'mark-in-progress':
        markInProgress()
    else:
        parser.print_help()
    
