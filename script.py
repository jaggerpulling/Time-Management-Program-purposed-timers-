#Imports
import time

#Initialize Variables
MIN_IN_HOUR = 60 #MIN
SEC_IN_MIN = 60 #SEC

TIME_BLOCK = 10 #MIN
THREE_HOURS_OF_BLOCKS = 18

file_path = "times_for_timer.txt"


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

    running = True
    while running:

        print("----------------------------------")
        print("------WELCOME TO CLOCK TIMER------")
        print("----------------------------------")
        print("Current Timers:")
        viewTimes(timers)

        user_input = input("Select Option:\n "
                           "(1) Add Timer\n "
                           "(2) Remove Timer\n "
                           "(3) Start Timer\n "
                           "(4) Stop Timer\n "
                           "(5) Reset Timer\n "
                           "(6) Save and Exit\n\n>")

        if user_input == '1':
           addTimer(timers)
        if user_input == '2':
            removeTimer(timers)
        if user_input == '3':
            selected_subject = startTimer(timers)
        if user_input == '4':
            stopTimer(timers, selected_subject)
        if user_input == '5':
            resetTimer(timers)
        if user_input == '6':
            saveFile(timers)
            break


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
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                subjectName , subjectTime = line.split()

                #Builds timers dictionary
                timers[subjectName] = int(subjectTime)

    except FileNotFoundError:
        print("File not found. Please run script again.")

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

def stopTimer(timers, selected_subject):
    stopwatch.stopWatch()

    #add time to dictionary
    elapsed_time = (stopwatch.elapsed_time / SEC_IN_MIN)
    timers[selected_subject] = round(elapsed_time, 2)


#OVERWRITES STORED DATA WITH IN-MEMORY
def saveFile(timers):
    with open(file_path, "w") as file:
        for class_name, time_str in timers.items():
            try:
                file.write("# Timer Pairs ENTER BELOW VVV\n")
                file.write("# Format: SUBJECT | TIME\n")
                file.write(f"{class_name} {time_str}\n")
            except Exception as e:
                print("FATAL ERROR")


# PRINTS TIMES THAT ARE IN TIMERS and RESPECTIVE TIME BLOCKS
def viewTimes(timers):
    importTimes()

    #Loops through each item in TIMERS
    for subject, time in timers.items():

        #Loops for each block printed
        bar = ''
        for i in range(THREE_HOURS_OF_BLOCKS):
            #Calculate how many blocks to fill
            blocks_filled = calculateBlocks(time)
            if i < blocks_filled:
                bar += '▮'
            else:
                bar += '▯'

        print(f"   {subject:<12}  {time:<3}mins    {bar}")

def resetTimer(timers):
    while True:
        # display subjects that can be removed:
        print('CURRENT SUBJECTS:')
        for subject in timers:
            print(f'  {subject}')

        selected_subject = input("Enter the subject you want to reset: ").strip()
        if selected_subject in timers:
            timers[selected_subject] = 0
            break
        else:
            print("Subject not found")

def addTimer(timers):
    while True:
        new_subject = input("Enter the subject you want to add: ").strip()
        break

    timers[new_subject] = 0

def removeTimer(timers):
    while True:
        #display subjects that can be removed:
        print('CURRENT SUBJECTS:')
        for subject in timers:
            print(f'  {subject}')

        selected_subject = input("Enter the subject you want to remove: ").strip()
        if selected_subject in timers:
            timers.pop(selected_subject)
            break
        else:
            print("Subject not found")



#print('▯')
#print('▮')
start()