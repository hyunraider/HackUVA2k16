from icalendar import Calendar
import datetime
import pytz
from pytz import timezone
eastern = timezone('US/Eastern')

cal = Calendar.from_ical(open("testUVAhackathon.ics").read())

eventList = []
taskList = []
timeList = []

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
        self.delta = start-end                                                                              #deltatime format defied on creation


for event in cal.walk("vevent"):
        name = event.get("summary")
        startTime = event.get("dtstart").from_ical(event.get("dtstart").to_ical(), "US/Eastern")
        endTime = event.get("dtend").from_ical(event.get("dtend").to_ical(), "US/Eastern")
        eventList.append(Event(name, startTime, endTime, False))


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
            if taskList[k].calcPriority > taskList[k + 1].calcPiority:
                temp = taskList[k]                                                                          #swap
                taskList[k] = taskList[k + 1]
                taskList[k + 1] = temp                                                                      #taskList now sorted by priority

def add_Sleep():                                                                                            #Adds Blocks of sleep to the start and ends of each day
    sort_events()
    currentDay = eventList[0].start_time
    nextDayIndex = 0
    for i in range(0, 6):
        lastMomentInDay = datetime.datetime(currentDay.year, currentDay.month, currentDay.day, 23, 5

        '''        lastMomentInDay = datetime.datetime(currentDay.year, currentDay.month, currentDay.day, 23, 5
        sleepTime = datetime.timedelta(hours=8)
        lastEventTime = 0
        lastMomentInDay = datetime.datetime(currentDay.year, currentDay.month, currentDay.day, 23, 59)
        for nextDayIndex in range(nextDayIndex, len(eventList)-1):
            print eventList[nextDayIndex].name
            print eventList[nextDayIndex].end_time.day - currentDay.day

            if eventList[nextDayIndex].end_time.day <= currentDay.day:
                lastEventTime = eventList[nextDayIndex].end_time
            else:
                break
                                                                                                            #Checks how much time is left between last event and midnight
                                                                                                            #If ends after 11, will give 30 minute buffer before putting in sleep
        if lastEventTime.hour > 22 and lastEventTime.minute > 30:
            if lastEventTime.hour < 23 and lastEventTime.minute < 30:
                eventList.append(Event("Sleep", lastEventTime + datetime.timedelta(minutes=30), lastMomentInDay, False))
                sleepTime = sleepTime - (lastMomentInDay - lastEventTime + datetime.timedelta(minutes=30))
            else:
                eventList.append(Event("Sleep", lastEventTime, lastMomentInDay, False))
                sleepTime = sleepTime - (lastMomentInDay - lastEventTime)
                                                                                                            #Hardcoded Sleep at 11 if time schedule permits
        else:
            goodSleep = datetime.datetime(currentDay.year, currentDay.month, currentDay.day, 23, 00)
            eventList.append(Event("Sleep", goodSleep, lastMomentInDay, False))
            sleepTime = sleepTime - (lastMomentInDay - goodSleep)

        firstMomentNextDay = eastern.localize(datetime.datetime(currentDay.year, currentDay.month, currentDay.day, 00, 00)+datetime.timedelta(days=1))
        # print firstMomentNextDay
        # print firstMomentNextDay.day
        # print eventList[nextDayIndex].name
        # print (eventList[nextDayIndex].start_time - datetime.timedelta(minutes=30)).tzinfo
        # print (firstMomentNextDay + sleepTime).tzinfo
        if firstMomentNextDay + sleepTime < eventList[nextDayIndex].start_time - datetime.timedelta(minutes=30):
            eventList.append(Event("Sleep", firstMomentNextDay, firstMomentNextDay + sleepTime, False))
        else:
            eventList.append(Event("Sleep", firstMomentNextDay, eventList[nextDayIndex].start_time - datetime.timedelta(minutes=30),False))

        currentDay = currentDay + datetime.timedelta(days=1)
'''
def free_Time_Until(dueDate):
    #currentDate = datetime.datetime.now(pytz.utc) #using the current time to calculate delta free time until event
    currentDate = eastern.localize(datetime.datetime(2016, 3, 28, hour=0, minute=0, second=0))# for testing the week
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

def calculate_Priority():#creates the float of the priority for ordering events, based on Priority*hoursToDo/FreeTime
    for task in taskList:
        task.calcPriority = (float)(task.priority*task.hoursToComplete/free_Time_Until(task.dueDate))       #multiply by priority and time to complete, divide by time until due
        print task.name#prints for debugging
        print task.priority
        print task.hoursToComplete
        print free_Time_Until(task.dueDate)
        print task.calcPriority

def prioritize_Time():                                                                                      #this creates a list of free time then distrubutes it between the events based on the priority calculated
    calculate_Priority()                                                                                    #tasks must be in order to run this method
    #currentDate = datetime.datetime.now(pytz.utc)                                                          #using the current time to calculate delta free time until event
    currentDate = eastern.localize(datetime.datetime(2016, 3, 28, hour=0, minute=0, second=0))              # for testing the week
    i = 0
    if len(eventList) > 0 and eventList[0].start_time - currentDate > datetime.timedelta(minutes=45):       #create an array of free time between events in chronological order accounting for the time
        timeList.append(FreeTime(currentDate, eventList[0].start_time-datetime.timedelta(minutes=15)))      #fifteen minute buffer
    while i < len(eventList) - 2:
        if eventList[i+1].start_time - eventList[i].end_time >= datetime.timedelta(minutes=60):             #by definition no free time blocks under 30 minutes
            timeList.append(FreeTime(eventList[i].end_time + datetime.timedelta(minutes=15), eventList[i+1].start_time - datetime.timedelta(minutes=15)))#fifteen minute buffer to account for travel
    for task in taskList:                                                                                   #for each task add it to the next time slot until it is done
        task

add_Sleep()

taskList.append(Tasks("Fix Laptop", 2, eastern.localize(datetime.datetime(2016, 4, 1, hour=21, minute=0, second = 0)), 3))# test tasks for debugging
taskList.append(Tasks("DLD Studio", 3, eastern.localize(datetime.datetime(2016, 3, 29, hour=13, minute=0, second = 0)), 7))
taskList.append(Tasks("Physics Pre Lab", .5, eastern.localize(datetime.datetime(2016, 3, 30, hour=13, minute=0, second = 0)), 6))
taskList.append(Tasks("Get Grocries", 1, eastern.localize(datetime.datetime(2016, 3, 31, hour=17, minute=0, second = 0)), 4))
taskList.append(Tasks("Nap", 1, eastern.localize(datetime.datetime(2016, 4, 1, hour=12, minute=0, second = 0)), 2))
taskList.append(Tasks("CS Post Lab", 6, eastern.localize(datetime.datetime(2016, 4, 1, hour=12, minute=0, second = 0)), 8))

calculate_Priority()
#dueDate = eastern.localize(datetime.datetime(2016, 3, 29, hour=12, minute=0, second = 0))
#print free_Time_Until(dueDate)
