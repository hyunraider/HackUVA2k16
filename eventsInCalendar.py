from icalendar import Calendar

class Event:
    def __init__(self, name, start, end, boolType):
        self.name = name
        self.start_time = start
        self.end_time = end
        self.givenType = boolType




cal = Calendar.from_ical(open("testUVAhackathon.ics").read())

eventList = []

for event in cal.walk("vevent"):
        name = event.get("summary")
        startTime = event.get("dtstart").from_ical(event.get("dtstart").to_ical(), "US/Eastern")
        endTime = event.get("dtend").from_ical(event.get("dtend").to_ical(), "US/Eastern")
        eventList.append(Event(name, startTime, endTime, False))
