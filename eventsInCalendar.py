from icalendar import Calendar
import datetime
import pytz

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
taskList = [1, 2, 3]

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
    currentDate = datetime.datetime.now(pytz.utc)
    totalTime =  dueDate - currentDate
    print totalTime
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
        print totalTime
    return totalTime #turn this into an int?? calc an int the whole time??

def calculate_Priority():
    for task in taskList:
        task.calcPriority = task.hoursToComplete/free_Time_Until(task.dueDate)*task.priority


sort_events()
print free_Time_Until(datetime.datetime.now(pytz.utc)+datetime.timedelta(hours = 60))
