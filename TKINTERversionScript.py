#Imports
import time
import tkinter as tk


#Initialize Variables
MIN_IN_HOUR = 60 #MIN
SEC_IN_MIN = 60 #SEC

TIME_BLOCK = 10 #MIN
THREE_HOURS_OF_BLOCKS = 18

FILE_PATH = "times_for_timer.txt"

# TKINTER window
window = tk.Tk()
current_subject = None


# PRINTS TIMES THAT ARE IN TIMERS and RESPECTIVE TIME BLOCKS
def viewTimes(timers):
    importTimes()

    # Loops through each item in TIMERS
    for subject, time in timers.items():

        # Loops for each block printed
        bar = ''
        for i in range(THREE_HOURS_OF_BLOCKS):
            # Calculate how many blocks to fill
            blocks_filled = calculateBlocks(time)
            if i < blocks_filled:
                bar += '▮'
            else:
                bar += '▯'

        l3 = tk.Label(window, text=f"   {subject:<12}  {time:<3}mins    {bar}")
        l3.pack()
#STOPWATCH
class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.is_running = False

    def startWatch(self):
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True
            print("Stopwatch started.")
        else:
            print("Stopwatch is already running.")

    def stopWatch(self):
        if self.is_running:
            self.elapsed_time += time.time() - self.start_time
            self.is_running = False
            print(f"Stopwatch stopped. Total time: {self.elapsed_time:.2f} seconds.")
        else:
            print("Stopwatch is not running.")

    def resetWatch(self):
        self.start_time = None
        self.elapsed_time = 0
        self.is_running = False
        print("Stopwatch has been reset.")

    def showTime(self):
        if self.is_running:
            current = time.time() - self.start_time + self.elapsed_time
        else:
            current = self.elapsed_time
        print(f"Current time: {current:.2f} seconds.")
stopwatch = Stopwatch()

def start():
    #import file and create timers
    timers = importTimes()

    # Tkinter Functions
    def exit():
        saveFile(timers)

    def reset():
        resetTimer(timers)

    def start_timer():
        global current_subject
        if not timers:
            tk.Label(text="No subjects to start.").pack()
            return

        # Variable to store the selected subject
        selected_subject = tk.StringVar()
        selected_subject.set(list(timers.keys())[0])  # default selection

        # Dropdown for subjects
        tk.Label(text="\nClick to Select from dropdown").pack()
        dropdown = tk.OptionMenu(window, selected_subject, *timers.keys())
        dropdown.pack()

        # Remove button
        start_btn = tk.Button(text="Start")
        start_btn.pack()

        def startSubmit():
            global current_subject
            current_subject = selected_subject.get()
            if current_subject in timers:
                stopwatch.startWatch()
                tk.Label(text=f"Started time for '{current_subject}.'").pack()
            dropdown.destroy()
            start_btn.destroy()

        start_btn.config(command=startSubmit)


    def stop():
        stopwatch.stopWatch()

        # add time to dictionary
        elapsed_time = (stopwatch.elapsed_time / SEC_IN_MIN)
        rounded_elapsed_time = round(elapsed_time, 2)
        timers[current_subject] = rounded_elapsed_time

        #display time
        tk.Label(text= f" {rounded_elapsed_time} minutes added for {current_subject}.").pack()


    def remove():
        if not timers:
            tk.Label(text="No subjects to remove.").pack()
            return

        # Variable to store the selected subject
        selected_subject = tk.StringVar()
        selected_subject.set(list(timers.keys())[0])  # default selection

        # Dropdown for subjects
        tk.Label(text="\nClick to Select from dropdown").pack()
        dropdown = tk.OptionMenu(window, selected_subject, *timers.keys())
        dropdown.pack()

        # Remove button
        remove_btn = tk.Button(text="Remove")
        remove_btn.pack()

        def removeSubmit():
            subject = selected_subject.get()
            if subject in timers:
                timers.pop(subject)  # remove from dictionary
                tk.Label(text=f"Removed '{subject}'").pack()
            dropdown.destroy()
            remove_btn.destroy()

        remove_btn.config(command=removeSubmit)


    def add():
        entry = tk.Entry(width=50, font="Arial")
        entry.pack()

        def submit():
            newSubject = entry.get()  # get the text user typed
            timers[newSubject] = 0

            #Remove Button and entry after
            entry.destroy()
            submit_btn.destroy()

        submit_btn = tk.Button(text="Submit", command=submit)
        submit_btn.pack()



    #Start Tkinter Window
    window.geometry("600x600")

    # Header Label
    tk.Label(window,
        text="WELCOME TO CLOCK TIMER",
        font = ('Arial',30)
    ).pack()
    tk.Label(window, text="Current Timers:").pack()

    #Display current timers
    viewTimes(timers)

    #Button Options
    b1 = tk.Button(window, text = "Add Timer", command= add).pack()
    b2 = tk.Button(window, text="Remove Timer", command=remove).pack()
    b3 = tk.Button(window, text="Start Timer", command=start_timer).pack()
    b4 = tk.Button(window, text="Stop Timer", command=stop).pack()
    b5 = tk.Button(window, text="Reset Timer", command=reset).pack()
    b6 = tk.Button(window, text="Save and Exit", command= exit).pack()



    #Run Tkinter Window
    window.mainloop()


#CALCULATE HOW MUCH LINES TO PRINT
def calculateBlocks(time):
     #assumes time is expressed in minutes

    #divides time by total time of line
    blocks_filled = time / (TIME_BLOCK)

    return blocks_filled

#IMPORTS FILE and BUILDS TIMER DICTIONARY
def importTimes():
    timers = {}
    try:
        with open(FILE_PATH, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                subjectName , subjectTime = line.split()

                #Builds timers dictionary
                timers[subjectName] = float(subjectTime)

    except FileNotFoundError:
        choice = input("File not found. Create new file? (y/n) ")
        if choice.lower() == 'y':
            f = open(FILE_PATH, 'w')
        else:
            print('returning')
            pass

    return timers

def startTimer(timers):
    while True:
        selected_subject = input("Enter which subject's time you want to start: ").strip()
        if selected_subject in timers:
            stopwatch.startWatch()
            break
        else:
            print("Subject not found")

    return selected_subject



#OVERWRITES STORED DATA WITH IN-MEMORY
def saveFile(timers):
    with open(FILE_PATH, "w") as file:
        for class_name, time_str in timers.items():
            try:
                file.write("# Timer Pairs ENTER BELOW VVV\n")
                file.write("# Format: SUBJECT | TIME\n")
                file.write(f"{class_name} {time_str}\n")
                print("File Saved. Exiting...")
            except Exception as e:
                print("FATAL ERROR")
    window.destroy()


def resetTimer(timers):
    while True:
        # display subjects that can be removed:
        print('CURRENT SUBJECTS:')
        for subject in timers:
            print(f'  {subject}')

        selected_subject = input("Enter the subject you want to reset: ").strip()
        if selected_subject in timers:
            timers[selected_subject] = 0
            print("Timer Reset")
            break
        else:
            print("Subject not found")

def addTimer(timers, newSubject):
    timers[newSubject] = 0




#print('▯')
#print('▮')
start()