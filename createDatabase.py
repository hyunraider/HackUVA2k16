def createDB():
    layerOne = []
    currentDate = eventList[0].start_time.date()
    eventIndex = 0
    while eventIndex < len(eventList)-1:
        layerTwo = {'day': str(currentDate.day), 'Month': currentDate.strftime("%B"), 'Week': currentDate.strftime("%A"), "Data" : []}
        while eventList[eventIndex].start_time.date() == currentDate():
            temp = eventList[eventIndex]
            layerTwo["Data"].append({"event": temp.name, "start": temp.start_time, "end": temp.end_time, "type": temp.givenType})
            eventIndex = eventIndex + 1
        layerOne.append(layerTwo)
        currentDate = eventList[eventIndex].start_time.date()
    return layerOne
