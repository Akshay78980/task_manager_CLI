class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()

            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics"""
        )

    def add(self, args):
        task_no = int(args[0])

        if task_no > 0:
            new_task = " ".join(args[1:])
            task_name = new_task #for referencing in the terminal
            
            if task_no not in self.current_items.keys():
                self.current_items[task_no] = new_task
            
            else:
                while(task_no in self.current_items.keys()):
                    final_task = self.current_items[task_no]
                    self.current_items[task_no] = new_task
                    new_task = final_task
                    task_no += 1
                self.current_items[task_no] = new_task

            self.write_current()
            print(f'Added task: "{task_name}" with priority {args[0]}')   

    def done(self, args):
        task_no = int(args[0])
        new_li = [item.strip("\n") for item in self.completed_items if item.strip("\n")]
        self.completed_items = new_li
        
        if task_no in self.current_items.keys():
                res = self.current_items.pop(task_no)
            
                self.write_current()
                self.completed_items.append(f"{res}")
                self.write_completed()
                
                print("Marked item as done.")
        else:
            print(f'Error: no incomplete item with priority {task_no} exists.')
        

    def delete(self, args):
        task_no = int(args[0])
        if task_no in self.current_items.keys():
            res = self.current_items.pop(task_no)
            print(f"Deleted item with priority {task_no}")
            self.write_current()
        else:
            print(f"Error: item with priority {task_no} does not exist. Nothing deleted.")
        

    def ls(self):        
        # completed_list = [int(item.strip("\n")) for item in self.completed_items if item.strip("\n")]
        i=1
        for x in self.current_items:
                print(f"{i}. {self.current_items[x]} [{x}]")
                i+=1
    

    def report(self):
        pending_count = len(self.current_items)
        self.read_completed()
        
        i = 1
        j = 1

        print(f"Pending : {pending_count}")
        for key in self.current_items.keys():
                print(f"{i}. {self.current_items[key]} [{key}]")
                i += 1

        completed_count = len(self.completed_items)

        print("\nCompleted :",completed_count)
        for item in self.completed_items:
                print(f"{j}. {item}")
                j += 1


        
