from icalendar import Calendar
import datetime
import pytz
from pytz import timezone



eastern = timezone('US/Eastern')

cal = Calendar.from_ical(open("testUVAhackathon.ics").read())

eventList = []
eventListDelocalized = []
taskList = []
timeList = []
finalDB = []

class Event:
    def __init__(self, name, start, end, boolType):
        self.name = name                                                                                    #string name
        self.start_time = start                                                                             #datetime format
        self.end_time = end                                                                                 #datetime format
        self.givenType = boolType                                                                           #to use in web side coloring

class Tasks:
    def __init__(self, name, hoursToComplete, dueDate, priority):
        self.name = name
        self.hoursToComplete = hoursToComplete
        self.dueDate = dueDate                                                                              #defined
        self.priority = priority                                                                            #user defined priority
        self.calcPriority = 0;                                                                              #to be set by calculatePriority()

class FreeTime:
    def __init__(self, start, end):
        self.start_time =  start                                                                            #datetime format
        self.end_time = end                                                                                 #datetime format
        self.delta = end-start                                                                              #deltatime format defied on creation


for event in cal.walk("vevent"):
        name = event.get("summary").to_ical()
        startTime = event.get("dtstart").from_ical(event.get("dtstart").to_ical(), "US/Eastern")
        endTime = event.get("dtend").from_ical(event.get("dtend").to_ical(), "US/Eastern")
        eventList.append(Event(name, startTime, endTime, True))


def sort_events():
        for i in range(len(eventList)-1,0,-1):                                                              #lame bubblesort.py
            for k in range(i):
                if eventList[k].start_time > eventList[k+1].start_time:
                    temp = eventList[k]                                                                     #swap
                    eventList[k] = eventList[k+1]
                    eventList[k+1] = temp                                                                   #eventList are now sorted by start date

def sort_tasks():
    for i in range(len(taskList) - 1, 0, -1):                                                               # lame bubblesort.py
        for k in range(i):
            if taskList[k].calcPriority < taskList[k + 1].calcPriority:
                temp = taskList[k]                                                                          #swap
                taskList[k] = taskList[k + 1]
                taskList[k + 1] = temp                                                                      #taskList now sorted by priority



def add_Sleep():                                                                                            #Adds Blocks of sleep to the start and ends of each day
    sort_events()
    del eventListDelocalized[:]
    for event in eventList:
        eventListDelocalized.append(Event(event.name, event.start_time.replace(tzinfo=None) + event.start_time.utcoffset(), event.end_time.replace(tzinfo=None) + event.start_time.utcoffset(), event.givenType))
    currentDay = eventListDelocalized[0].start_time
    nextDayIndex = 0
    #MUST CHANGE THIS LATER IN ODER TO HAVE MODULAR FUNCTION (dont be stupid)
    eventList.append(Event("Sleep", eastern.localize(datetime.datetime(currentDay.year, currentDay.month, currentDay.day, 00, 00)) - event.start_time.utcoffset(), eastern.localize(datetime.datetime(currentDay.year, currentDay.month, currentDay.day, 7, 00)) - event.start_time.utcoffset(), True))
    for i in range(0, 4):
        sleepTime = datetime.timedelta(hours=8)
        lastEventTime = datetime.datetime(currentDay.year, currentDay.month, currentDay.day, 0, 0)
        lastMomentInDay = datetime.datetime(currentDay.year, currentDay.month, currentDay.day, 23, 59)
        for nextDayIndex in range(nextDayIndex, len(eventListDelocalized)-1):
            if eventListDelocalized[nextDayIndex].end_time <= lastMomentInDay:
                lastEventTime = eventListDelocalized[nextDayIndex].end_time
            else:
                break
                                                                                                            #Checks how much time is left between last event and midnight
                                                                                                            #If ends after 11, will give 30 minute buffer before putting in sleep
        if lastEventTime.hour * 60 + lastEventTime.minute > 1350:
            if lastEventTime.hour * 60 + lastEventTime.minute < 1410:
                eventList.append(Event("Sleep", eastern.localize(lastEventTime + datetime.timedelta(minutes=30)), eastern.localize(lastMomentInDay)- event.start_time.utcoffset(), True))
                sleepTime = sleepTime - (lastMomentInDay - lastEventTime + datetime.timedelta(minutes=30))
            else:
                eventList.append(Event("Sleep", eastern.localize(lastEventTime), eastern.localize(lastMomentInDay)- event.start_time.utcoffset(), True))
                sleepTime = sleepTime - (lastMomentInDay - lastEventTime)
                                                                                                            #Hardcoded Sleep at 11 if time schedule permits
        else:
            goodSleep = datetime.datetime(currentDay.year, currentDay.month, currentDay.day, 23, 00)
            eventList.append(Event("Sleep", eastern.localize(goodSleep)- event.start_time.utcoffset(), eastern.localize(lastMomentInDay)- event.start_time.utcoffset(), True))
            sleepTime = sleepTime - (lastMomentInDay - goodSleep)

        firstMomentNextDay = datetime.datetime(currentDay.year, currentDay.month, currentDay.day, 00, 00)+datetime.timedelta(days=1)
        if firstMomentNextDay + sleepTime < eventListDelocalized[nextDayIndex].start_time - datetime.timedelta(minutes=30):             #Add variable for prep time in the morening rather than hardcode 30 min
            eventList.append(Event("Sleep", eastern.localize(firstMomentNextDay)- event.start_time.utcoffset(), eastern.localize(firstMomentNextDay + sleepTime)- event.start_time.utcoffset(), True))
        else:
            eventList.append(Event("Sleep", eastern.localize(firstMomentNextDay)- event.start_time.utcoffset(), (eventList[nextDayIndex].start_time - datetime.timedelta(minutes=30)),True))

        currentDay = currentDay + datetime.timedelta(days=1)


        

def free_Time_Until(dueDate):
    #currentDate = datetime.datetime.now(pytz.utc) #using the current time to calculate delta free time until event
    currentDate = eastern.localize(datetime.datetime(2016, 3, 28, hour=8, minute=0, second=0))              # for testing the week
    totalTime =  dueDate - currentDate                                                                      #start assuming all time until due date is availible
    i = 0
    if len(eventList) > 0 and eventList[0].start_time - currentDate > datetime.timedelta(minutes=45):       #if there is more than 15 minutes before the first event
        totalTime = totalTime - datetime.timedelta(minutes=15)                                              #fifteen minute buffer
    else:
        totalTime = totalTime - (eventList[0].start_time - currentDate)                                     #if there is less time then totaltime -= less time

    while i < len(eventList)-2 and dueDate > eventList[i].end_time:                                         #loop while the event ends before the due date
        if eventList[i+1].start_time > dueDate:                                                             #if this is the last event before the due date
            if  dueDate - eventList[i].end_time < datetime.timedelta(minutes=60):                           #if there is less than an hour between the events
                totalTime = totalTime - (dueDate - eventList[i].end_time)                                   #there is no time between those events to work
            else:
                totalTime = totalTime - datetime.timedelta(minutes=30)                                      #otherwise buffer the gap by 15 minutes on both sides
        else:
            if eventList[i+1].start_time - eventList[i].end_time < datetime.timedelta(minutes=60):          #when there is less than an hour between events
                totalTime = totalTime - (eventList[i+1].start_time - eventList[i].end_time)                 #still no time to work between
            else:
                totalTime = totalTime - datetime.timedelta(minutes=30)                                      #buffer after this event and before next event by 15 minutes
        totalTime = totalTime - (eventList[i].end_time - eventList[i].start_time)                           #subtract the time of the actual event
        i+=1
        if eventList[i].start_time < dueDate and eventList[i].end_time > dueDate:                           #if the next event is cut by the due date
            totalTime = totalTime - (dueDate - eventList[i].start_time)                                     #subtract that events time
    return totalTime.total_seconds()/3600 #turn this into an int?? calc an int the whole time??             #return number of hours

def calculate_Priority():                                  #creates the float of the priority for ordering events, based on Priority*hoursToDo/FreeTime
    for task in taskList:
        task.calcPriority = (float)(task.priority*task.hoursToComplete/free_Time_Until(task.dueDate))       #multiply by priority and time to complete, divide by time until due


def prioritize_Time():                                                                                      #this creates a list of free time then distrubutes it between the events based on the priority calculated
    calculate_Priority()                                                                                    #tasks must be in order to run this method
    sort_tasks()                                                                                            #orders the tasks
    #currentDate = datetime.datetime.now(pytz.utc)                                                          #using the current time to calculate delta free time until event
    currentDate = eastern.localize(datetime.datetime(2016, 3, 28, hour=8, minute=0, second=0) + eventList[0].start_time.utcoffset())              # for testing the week
    i = 0
    if len(eventList) > 0 and eventList[0].start_time - currentDate >= datetime.timedelta(minutes=45):      #create an array of free time between events in chronological order accounting for the time
        timeList.append(FreeTime(currentDate, eventList[0].start_time-datetime.timedelta(minutes=15)))      #fifteen minute buffer
    while i < len(eventList) - 2:
        if eventList[i+1].start_time - eventList[i].end_time >= datetime.timedelta(minutes=60):             #by definition no free time blocks under 30 minutes
            timeList.append(FreeTime(eventList[i].end_time + datetime.timedelta(minutes=15), eventList[i+1].start_time - datetime.timedelta(minutes=15)))#fifteen minute buffer to account for travel
        i+=1
    for free in timeList:                                                                                   #for each task add it to the next time slot until it is done
        timeFilled = False
        if len(taskList) == 0:                                                                              #if there are no more tasks to complete
            break
        if free.delta <= datetime.timedelta(minutes = 45):                                                  #if there is only a little bit of time
            for task in taskList:                                                                           #find a task in the list that
                if task.hoursToComplete < free.delta.total_seconds()/3600:                                  #takes less time to complete than the free time
                    task.hoursToComplete = 0                                                                #due to order this will be the highest priority one
                    eventList.append(Event(task.name, free.start_time, free.end_time, False))               #do that task
                    task.calcPriority = 0                                                                   #this event is now done
                    timeFilled = True                                                                       #to break out of the loop
                    break                                                                                   #onto the next task spot
            if not timeFilled:                                                                              #otherwise there is no small event
                eventList.append(Event(taskList[0].name, free.start_time, free.end_time, False))            #so put that time to a larger event
                taskList[0].hoursToComplete = taskList[0].hoursToComplete - free.delta.total_seconds()/3600 #subtract that time
                taskList[0].calcPriority = (float)(taskList[0].priority * taskList[0].hoursToComplete / free_Time_Until(taskList[0].dueDate))#recalculate the priority of this event
                timeFilled = True
        else:                                                                                               #there is a longer period of time
            timeFilled = False
            eventList.append(Event(taskList[0].name, free.start_time, free.end_time, False))                #add event to do work during
            taskList[0].hoursToComplete = taskList[0].hoursToComplete - free.delta.total_seconds()/3600     #reduce tasks to complete
            taskList[0].calcPriority = (float)(taskList[0].priority * taskList[0].hoursToComplete / free_Time_Until(taskList[0].dueDate))
            timeFilled = True                                                                               #in case of multiple cases
        for task in taskList:                                                                               #delete tasks that are done (if priority = 0 or time to complete = 0)
            if task.calcPriority <= 0.0 or task.dueDate-currentDate < datetime.timedelta(hours=0):          #if there is no priority (hrs2complete = 0 or priority = 0) or dueDatePasssed
                taskList.remove(task)                                                                       #remove this event
        sort_tasks()                                                                                        #resort based on removals or priority changes

# def prioritize_Time():                                                                                      #this creates a list of free time then distrubutes it between the events based on the priority calculated
#     sort_tasks()                                                                                            #orders the tasks
#     #currentDate = datetime.datetime.now(pytz.utc)                                                          #using the current time to calculate delta free time until event
#     currentDate = eastern.localize(datetime.datetime(2016, 3, 28, hour=8, minute=0, second=0)) - eventList[0].start_time.utcoffset()              # for testing the week
#     i = 0
#     for event in eventList:
#         if (not event.givenType):
#             eventList.remove(event)
#     tempTasks = []
#     calculate_Priority()  # tasks must be in order to run this method
#     for task in taskList:
#         tempTasks.append(task)
#         print task.name
#     if len(eventList) > 0 and eventList[0].start_time - currentDate >= datetime.timedelta(minutes=45):      #create an array of free time between events in chronological order accounting for the time
#         timeList.append(FreeTime(currentDate, eventList[0].start_time-datetime.timedelta(minutes=15)))      #fifteen minute buffer
#     while i < len(eventList) - 2:
#         if eventList[i+1].start_time - eventList[i].end_time >= datetime.timedelta(minutes=60):             #by definition no free time blocks under 30 minutes
#             timeList.append(FreeTime(eventList[i].end_time + datetime.timedelta(minutes=15), eventList[i+1].start_time - datetime.timedelta(minutes=15)))#fifteen minute buffer to account for travel
#         i+=1
#     for free in timeList:                                                                                   #for each task add it to the next time slot until it is done
#         timeFilled = False
#         if len(tempTasks) == 0:                                                                              #if there are no more tasks to complete
#             break
#         if free.delta <= datetime.timedelta(minutes = 45):                                                  #if there is only a little bit of time
#             for task in tempTasks:                                                                           #find a task in the list that
#                 if task.hoursToComplete < free.delta.total_seconds()/3600:                                  #takes less time to complete than the free time
#                     task.hoursToComplete = task.hoursToComplete - free.delta.total_seconds()/3600   #due to order this will be the highest priority one
#                     eventList.append(Event(task.name, free.start_time, free.end_time, False))               #do that task
#                     task.calcPriority = (float)(task.priority * task.hoursToComplete / free_Time_Until(task.dueDate))#recalculate the priority of this event                                                                   #this event is now done
#                     timeFilled = True                                                                       #to break out of the loop
#                     break                                                                                   #onto the next task spot
#             if not timeFilled:                                                                              #otherwise there is no small event
#                 eventList.append(Event(tempTasks[0].name, free.start_time, free.end_time, False))            #so put that time to a larger event
#                 tempTasks[0].hoursToComplete = tempTasks[0].hoursToComplete - free.delta.total_seconds()/3600 #subtract that time
#                 tempTasks[0].calcPriority = (float)(tempTasks[0].priority * tempTasks[0].hoursToComplete / free_Time_Until(tempTasks[0].dueDate))#recalculate the priority of this event
#                 timeFilled = True
#         else:                                                                                               #there is a longer period of time
#             timeFilled = False
#             eventList.append(Event(tempTasks[0].name, free.start_time, free.end_time, False))                #add event to do work during
#             tempTasks[0].hoursToComplete = tempTasks[0].hoursToComplete - free.delta.total_seconds()/3600     #reduce tasks to complete
#             tempTasks[0].calcPriority = (float)(tempTasks[0].priority * tempTasks[0].hoursToComplete / free_Time_Until(tempTasks[0].dueDate))
#             timeFilled = True                                                                               #in case of multiple cases
#         for task in tempTasks:                                                                               #delete tasks that are done (if priority = 0 or time to complete = 0)
#             if task.calcPriority <= 0.0 or task.dueDate-currentDate < datetime.timedelta(hours=0):          #if there is no priority (hrs2complete = 0 or priority = 0) or dueDatePasssed
#                 tempTasks.remove(task)                                                                       #remove this event
#         sort_tasks()                                                                                        #resort based on removals or priority changes


def createDB():
    del finalDB[:]
    del eventListDelocalized[:]
    for event in eventList:
        eventListDelocalized.append(Event(event.name, event.start_time.replace(tzinfo=None) + event.start_time.utcoffset(), event.end_time.replace(tzinfo=None) + event.start_time.utcoffset(), event.givenType))
    layerOne = []
    currentDate = eventListDelocalized[0].start_time.date()
    eventIndex = 0
    while eventIndex < len(eventListDelocalized)-1:
        layerTwo = {'day': str(currentDate.day), 'Month': currentDate.strftime("%B"), 'Week': currentDate.strftime("%A"), "Data" : []}
        while eventIndex < len(eventListDelocalized)-1 and eventListDelocalized[eventIndex].start_time.date() == currentDate:
            temp = eventListDelocalized[eventIndex]
            layerTwo["Data"].append({"event": temp.name, "start": temp.start_time.hour + temp.start_time.minute/60.0, "end": temp.end_time.hour + temp.end_time.minute/60.0, "type": temp.givenType})
            eventIndex = eventIndex + 1
        layerOne.append(layerTwo)
        currentDate = eventListDelocalized[eventIndex].start_time.date()
    for a in layerOne:
        finalDB.append(a)

def updateAll():
    for i in range(len(eventList)-1, -1, -1):
        if eventList[i].name == "Sleep":
            eventList.remove(eventList[i])
    add_Sleep()
    calculate_Priority()
    for t in taskList:
        print t.name
        print t.calcPriority
    sort_events()
    prioritize_Time()
    sort_events()
    createDB()

taskList.append(Tasks("Fix Laptop", 2, eastern.localize(datetime.datetime(2016, 4, 1, hour=21, minute=0, second = 0)), 3))# test tasks for debugging
taskList.append(Tasks("DLD Studio", 3, eastern.localize(datetime.datetime(2016, 3, 29, hour=13, minute=0, second = 0)), 7))
taskList.append(Tasks("Physics Pre Lab", .5, eastern.localize(datetime.datetime(2016, 3, 30, hour=13, minute=0, second = 0)), 6))
taskList.append(Tasks("Get Grocries", 1, eastern.localize(datetime.datetime(2016, 3, 31, hour=17, minute=0, second = 0)), 4))
taskList.append(Tasks("Nap", 1, eastern.localize(datetime.datetime(2016, 4, 1, hour=12, minute=0, second = 0)), 2))
taskList.append(Tasks("CS Post Lab", 10, eastern.localize(datetime.datetime(2016, 4, 1, hour=12, minute=0, second = 0)), 8))
taskList.append(Tasks("Copy notes", 1, eastern.localize(datetime.datetime(2016, 3,31, hour=17, minute=0, second = 0)), 9))
taskList.append(Tasks("Clean Room", 1, eastern.localize(datetime.datetime(2016, 4, 1, hour=23, minute=0, second = 0)), 5))
taskList.append(Tasks("Get Mail", .5, eastern.localize(datetime.datetime(2016, 3, 30, hour=12, minute=0, second = 0)), 6))
taskList.append(Tasks("Clean Fridge", .5, eastern.localize(datetime.datetime(2016, 4, 1, hour=23, minute=0, second = 0)), 4))
taskList.append(Tasks("Physics Lab Report", .5, eastern.localize(datetime.datetime(2016, 3, 30, hour=16, minute=0, second = 0)), 5))
taskList.append(Tasks("ACM planning", .5, eastern.localize(datetime.datetime(2016, 4, 1, hour=23, minute=0, second = 0)), 7))
taskList.append(Tasks("Watch news", 1, eastern.localize(datetime.datetime(2016, 4, 1, hour=23, minute=0, second = 0)), 2))
taskList.append(Tasks("Do Laundry", 2, eastern.localize(datetime.datetime(2016, 4, 1, hour=23, minute=0, second = 0)), 3))

calculate_Priority()
for t in taskList:
    print t.name
    print t.calcPriority
