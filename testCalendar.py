import datetime
import icalendar
import os
import pytz
import time
data = open('testUVAhackathon.ics','rb').read()
cal = icalendar.Calendar.from_ical(data)

events = [1,2,3]  # placeholder for events
tasks = [1,2,3] #placeholder for tasks

def sort_Events():
        for i in range(0,len(events)-1,1):          #lame bubblesort.py
            for k in range(i,len(events)-1,1):
                if events[k] < events[k-1]:
                    temp = events[k]
                    events[k] = events[k-1]
                    events[k-1] = temp              #events are now sorted

def free_Time_Until(dueDate):
    currentDate = datetime.datetime.now();
    totalTime =  dueDate - currentDate;
    i = 0
    while i < len(events)-2 and events[i][2] < dueDate:
        if events[i+1][1] > dueDate:
            if  dueDate - events[i][2] <= 30:
                totalTime = totalTime - dueDate - events[i][2]
            else:
                totalTime = totalTime - datetime.timedelta(minutes=30)
        else:
            if events[i+1][1] - events[i][2] <= 30:
                totalTime = totalTime -  (events[i+1][1] - events[i][2])
            else:
                totalTime = totalTime - datetime.timedelta(minutes=30)
        totalTime = totalTime - (events[i][2] - events[i][1])
        i+=1
    return totalTime #turn this into an int?? calc an int the whole time??



def calculate_Priority():
    for task in tasks:
        task[4] = task[1]/free_Time_Until(task[2])*task[3]





