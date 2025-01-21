import sys
import datetime

# Estudar manipulação de arquivos a fundo

def write_task(id, description, status, createdAt, updatedAt):
    return f'{{\n{tab}"id": {id},\n{tab}"description": "{description}",\n{tab}"status": "{status}",\n{tab}"created at": "{createdAt}",\n{tab}"updated at": "{updatedAt}"\n}}\n]'

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
        file.seek(index - 2)
        file.write(",\n")

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
            file.write(f'{tab}"description": "{new_description}",\n')
            file.write(file_content[i+2]) # status line
            file.write(file_content[i+3]) # createdAt line
            file.write(f'{tab}"updated at": "{updatedAt}"\n')
            i += 4
        i += 1  

    file.truncate()
    return        

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
tab = "    "

file = None
try:
    file = open("tasks.json", "r+", encoding="utf-8")
except FileNotFoundError:
    print("Creating the file tasks.json...")
    file = open("tasks.json", "w+", encoding="utf-8")
    file.write("[\n]")
finally:
    if file is not None:
        cmd_table[command](args)
        file.close()