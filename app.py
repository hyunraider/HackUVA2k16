from flask import Flask, url_for, render_template, jsonify, request, json
from testCalendar import *
from pytz import timezone
import datetime

app = Flask(__name__)

#Dummy DB that I've been testing on. Replace it with the real one!
emptydb = []

#Dummy DB That I've been using so far.
dbs = [
        {
                'day': "21",
                "Month": "March",
                "Week": "Monday",
                "Data": [
                        {
                                'event': "CS225",
                                'start': 8,
                                'end': 9,
                                'type': True
                        },
                        {
                                'event': "Math Homework",
                                'start': 10,
                                'end': 14,
                                'type': False
                        }
                ]
        },
        {
                'day': "22",
                "Month": "March",
                "Week": "Tuesday",
                "Data": [
                ]
        },
        {
                'day': "23",
                "Month": "March",
                "Week": "Wednesday",
                "Data": []
        },
        {
                'day': "24",
                "Month": "March",
                "Week": "Thursday",
                "Data": []
        },
        {
                'day': "25",
                "Month": "March",
                "Week": "Friday",
                "Data": []
        }
]

#Just a testing route for in case you want to print out something for testing
@app.route('/testing')
def test():
        return str(emptydb);

#Our main route. You can connect the db here using parameters
@app.route('/')
def index():
        return render_template("index.html", dbs = dbs)

#This Method is just a helper function so that you can take
#a string of Date in MM/DD/YYYY/HH/MM format and convert it into
#an array with arr[0]=day, arr[1]=Month (got lazy we're only doing one week)
#and arr[4]=Hour, arr[5]=Month, so you can access the array elsewhere
def deserializedate(date):
        quickdate = [int(date[3,5]), "March", int(date[11,13]), int(date[14,16])]
        return quickdate

#This is a post URL where the magic happens, AKA when we process the AJAX call
#This is the way we can send frontend information (the event form) to the backend
#so you can add to the existing Database. 
@app.route('/addevent', methods=['POST'])
def addevent():
        name = request.form.get('name')
        start = request.form.get('start')
        end = request.form.get('end')
        #You will need to do python magic here to insert the necessary data
        #by first searching for the appropriate 2nd DB layer based on the month and day
        #then inserting the day, Month, Week, and the Data into the db
        #A lot of searching/inserting is taking place, use the deserializedate() helper
        #function to your advantage.
        #Collin you know this python stuff better than i do
        #Declaring an index variable may be helpful
        
        #this is where you insert it into the db. Remember it is incomplete because its automatically
        #inserting into the FIRST LAYER OF DB! Which is NOT what we want.
        dbs.append({'name': name, 'start': start, 'end': end})
        
        est = timezone("US/Eastern")
        eventList.append(Event(name, est.localize(datetime.datetime(int(start[6:10]), int(start[:2]), int(start[3:5]), int(start[11:13]), int(start[14:16]))),
                               est.localize(datetime.datetime(int(end[6:10]), int(end[:2]), int(end[3:5]), int(end[11:13]), int(end[14:16]))), True))

        updateAll()
        #leave this line to be as it is
        return json.dumps({'status':'OK','name':name})

#This is the post URL for Adding Assignments -> Same shit as before
@app.route('/addassign', methods=['POST'])
def addassign():
        name = request.form.get('name')
        start = request.form.get('start')
        end = request.form.get('end')
        priority = request.form.get('priority')
        #Same thing here as the comments above
        
        #this is where you insert it into the db. Remember it is incomplete because its automatically
        #inserting into the FIRST LAYER OF DB! Which is NOT what we want.
        dbs.append({'name': name, 'start': start, 'end': end, 'priority': priority})

        est = timezone("US/Eastern")
        eventList.append(Event(name, est.localize(datetime.datetime(int(start[6:10]), int(start[:2]), int(start[3:5]), int(start[11:13]), int(start[14:16]))),
                               est.localize(datetime.datetime(int(end[6:10]), int(end[:2]), int(end[3:5]), int(end[11:13]), int(end[14:16]))), False))
        updateAll()
        #leave this line to be as it is
        return json.dumps({'status':'OK','name':name})

#Friendly reminder that your db will erase if there is a change in the 
#system because debug is on-> during the demo it shouldn't happen.
app.run(debug=True, port=8000, host='0.0.0.0')
