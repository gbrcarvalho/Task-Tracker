import sys
import datetime

# status three possible values -> done, not done, in progress
# bonus, add timestamp to the task 

# Task Properties
# Each task should have the following properties:

# id: A unique identifier for the task
# description: A short description of the task
# status: The status of the task (todo, in-progress, done)
# createdAt: The date and time when the task was created
# updatedAt: The date and time when the task was last updated

def write_task(id, description, status, createdAt, updatedAt):
    return f'{{\n"id": {id},\n"description": "{description}",\n"status": "{status}",\n"created at": "{createdAt}",\n"updated at": "{updatedAt}"\n}}\n'

def add_task(args):
    createdAt = datetime.datetime.now()
    updatedAt = datetime.datetime.now()
        
    file = None
    try:
        file = open("tasks.json", "r", encoding="utf-8")
    except FileNotFoundError:
        current_id = 1
    else:
        file_content = file.read()
        current_id = file_content.count("{") + 1
    finally:
        if file is not None:
            file.close()
    with open("tasks.json", "a", encoding="utf-8") as file:
        file.write(write_task(current_id, args[0], "not done", createdAt, updatedAt))
    return

def update_task(args):
    pass

def delete_task(args):
    pass

def mark_in_progress(args):
    file = None
    try:
        file = open("tasks.txt", "r+", encoding="utf-8")
    except FileNotFoundError:
        print("The task doesn't exist!")
        return
    else:
        file_content = file.readlines()
        for i, line in enumerate(file_content):
            if f"id: {args[0]}," in line:
                updatedAt = datetime.datetime.now()
                file_content[i+2] = "status: in progress,\n"
                file_content[i+4] = f"updated at: {updatedAt}\n"
                break
        
        file.seek(0)
        for line in file_content:
            file.writelines(line)
    finally:
        if file is not None:
            file.close()
    

def mark_done(args):
    file = None
    try:
        file = open("tasks.txt", "r+", encoding="utf-8")
    except FileNotFoundError:
        print("The task doesn't exist!")
        return
    else:
        file_content = file.readlines()
        for i, line in enumerate(file_content):
            if f"id: {args[0]}," in line:
                updatedAt = datetime.datetime.now()
                file_content[i+2] = "status: done,\n"
                file_content[i+4] = f"updated at: {updatedAt}\n"
                break
        
        file.seek(0)
        for line in file_content:
            print(line)
            file.writelines(line)
    finally:
        if file is not None:
            file.close()
 
cmd_table = {
    "add": add_task,
    "update": update_task,
    "delete": delete_task,
    "mark-in-progress": mark_in_progress,
    "mark-done": mark_done
}

command = sys.argv[1]
args = sys.argv[2:]

cmd_table[command](args)


    
