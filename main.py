import sys
import datetime
import os

# Estudar manipulação de arquivos a fundo

def write_task(id, description, status, createdAt, updatedAt):
    return f'{{{newline}{tab}"id": {id},{newline}{tab}"description": "{description}",{newline}{tab}"status": "{status}",{newline}{tab}"created at": "{createdAt}",{newline}{tab}"updated at": "{updatedAt}"{newline}}}{newline}]'

def add_task(args):
    global file

    createdAt = datetime.datetime.now()
    updatedAt = datetime.datetime.now()
    
    file.seek(0)

    current_id = 1
    while True:
        index = file.tell()
        char = file.read(1)
        if char == '{':
            current_id += 1
        if char == "]":
            break
    
    file.truncate()

    if current_id == 1:
        file.seek(index)
    
    if current_id > 1:
        file.seek(index - 1)
        file.write(f",{newline}")

    file.write(write_task(current_id, args[0], "todo", createdAt, updatedAt))
    return

def update_task(args):
    global file

    updatedAt = datetime.datetime.now()

    file.seek(0)

    current_id = args[0]
    new_description = args[1]

    file_content = file.readlines()
    file.seek(0)
    
    i = 0
    while i < len(file_content):
        file.write(file_content[i])
        if f'"id": {current_id}' in file_content[i]: # id line
            file.write(f'{tab}"description": "{new_description}",{newline}')
            file.write(file_content[i+2]) # status line
            file.write(file_content[i+3]) # createdAt line
            file.write(f'{tab}"updated at": "{updatedAt}"{newline}')
            i += 4
        i += 1  

    file.truncate()
    return        

def delete_task(args):
    global file

    file.seek(0)

    current_id = args[0]

    file_content = file.readlines()
    file.seek(0)
    
    number_of_lines = len(file_content)

    i = 0
    while i < number_of_lines:
        try:
            line = file_content[i+2]
        except IndexError:
            file.write(file_content[i])
            file.write(file_content[i+1])
            break
        try:
            line = file_content[i+3]
        except IndexError:
            file.write(file_content[i])
            file.write(file_content[i+1])
            file.write(file_content[i+2])
            break
        if f'"id": {current_id}' in file_content[i+2]: # id line
            file.write(file_content[i])
            i += 8
        if i + 1 >= number_of_lines - 9:
            if f'"id": {current_id}' in file_content[i+3]: # id line
                file.write(file_content[i])
                file.write(f"}}{newline}")
                i += 9
        file.write(file_content[i])
        i += 1  

    file.truncate()
    return        

def mark_in_progress(args):
    pass

def mark_done(args):
    pass
 
cmd_table = {
    "add": add_task,
    "update": update_task,
    "delete": delete_task,
    "mark-in-progress": mark_in_progress,
    "mark-done": mark_done
}

command = sys.argv[1]
args = sys.argv[2:]
newline = "\n"
tab = "    "

file = None
try:
    file = open("tasks.json", "r+", newline=newline)
except FileNotFoundError:
    print("Creating the file tasks.json...")
    file = open("tasks.json", "w+", newline=newline)
    file.write(f"[{newline}]")
finally:
    if file is not None:
        cmd_table[command](args)
        file.close()