from icalendar import Calendar
import datetime
import pytz
from pytz import timezone
eastern = timezone('US/Eastern')
class Event:
    def __init__(self, name, start, end, boolType):
        self.name = name
        self.start_time = start
        self.end_time = end
        self.givenType = boolType

class Tasks:
    def __init__(self, name, hoursToComplete, dueDate, priority):
        self.name = name
        self.hoursToComplete = hoursToComplete
        self.dueDate = dueDate
        self.priority = priority
        self.calcPriority = 0;




cal = Calendar.from_ical(open("testUVAhackathon.ics").read())

eventList = []
taskList = []

for event in cal.walk("vevent"):
        name = event.get("summary")
        startTime = event.get("dtstart").from_ical(event.get("dtstart").to_ical(), "US/Eastern")
        endTime = event.get("dtend").from_ical(event.get("dtend").to_ical(), "US/Eastern")
        eventList.append(Event(name, startTime, endTime, False))


def sort_events():
        for i in range(len(eventList)-1,0,-1):          #lame bubblesort.py
            for k in range(i):
                if eventList[k].start_time > eventList[k+1].start_time:
                    temp = eventList[k]
                    eventList[k] = eventList[k+1]
                    eventList[k+1] = temp              #eventList are now sorted


def free_Time_Until(dueDate):
    #currentDate = datetime.datetime.now(pytz.utc) #using the current time to calculate delta free time until event
    currentDate = eastern.localize(datetime.datetime(2016, 3, 28, hour=0, minute=0, second=0))# for testing the week
    totalTime =  dueDate - currentDate
    i = 0
    if len(eventList) > 1 and eventList[0].start_time - currentDate > datetime.timedelta(minutes=45):
        totalTime = totalTime - datetime.timedelta(minutes=15)
    else:
        totalTime = totalTime - (eventList[0].start_time - currentDate)

    while i < len(eventList)-2 and dueDate > eventList[i].end_time:

        if eventList[i+1].start_time > dueDate:
            if  dueDate - eventList[i].end_time < datetime.timedelta(minutes=60):
                totalTime = totalTime - (dueDate - eventList[i].end_time)
            else:
                totalTime = totalTime - datetime.timedelta(minutes=30)
        else:
            if eventList[i+1].start_time - eventList[i].end_time < datetime.timedelta(minutes=60):
                totalTime = totalTime - (eventList[i+1].start_time - eventList[i].end_time)
            else:
                totalTime = totalTime - datetime.timedelta(minutes=30)
        totalTime = totalTime - (eventList[i].end_time - eventList[i].start_time)
        i+=1
        if eventList[i].start_time < dueDate and eventList[i].end_time > dueDate:
            totalTime = totalTime - (dueDate - eventList[i].start_time)
    return totalTime.total_seconds()/3600 #turn this into an int?? calc an int the whole time??

def calculate_Priority():
    for task in taskList:
        #currentDate = pytz.timezone('US/Eastern').localize(datetime(2016, 3, 28, hour=0, minute=0))
        task.calcPriority = (float)(task.priority*task.hoursToComplete/free_Time_Until(task.dueDate))
        print task.name
        print task.priority
        print task.hoursToComplete
        print free_Time_Until(task.dueDate)
        print task.calcPriority

sort_events()

taskList.append(Tasks("Fix Laptop", 2, eastern.localize(datetime.datetime(2016, 4, 1, hour=21, minute=0, second = 0)), 3))
taskList.append(Tasks("DLD Studio", 3, eastern.localize(datetime.datetime(2016, 3, 29, hour=13, minute=0, second = 0)), 7))
taskList.append(Tasks("Physics Pre Lab", .5, eastern.localize(datetime.datetime(2016, 3, 30, hour=13, minute=0, second = 0)), 6))
taskList.append(Tasks("Get Grocries", 1, eastern.localize(datetime.datetime(2016, 3, 31, hour=17, minute=0, second = 0)), 4))
taskList.append(Tasks("Nap", 1, eastern.localize(datetime.datetime(2016, 4, 1, hour=12, minute=0, second = 0)), 2))
taskList.append(Tasks("CS Post Lab", 6, eastern.localize(datetime.datetime(2016, 4, 1, hour=12, minute=0, second = 0)), 8))

calculate_Priority()
#dueDate = eastern.localize(datetime.datetime(2016, 3, 29, hour=12, minute=0, second = 0))
#print free_Time_Until(dueDate)
