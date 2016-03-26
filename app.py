from flask import Flask, url_for, render_template, jsonify


app = Flask(__name__)

dbs = [
	{
		'day': "21",
		"Month": "March",
		"Week": "Monday",
		"Data": [
			{
				'event': "Event 1",
				'start': 0300,
				'end': 0500,
				'type': True
			},
			{
				'event': "Event 2",
				'start': 0700,
				'end': 1000,
				'type': True
			}
		]
	},
	{
		'day': "22",
		"Month": "March",
		"Week": "Tuesday",
		"Data": []
	}
]

db2 = [
	["21", "March", "Monday",
		[
			[
				"Waking up",
				600,
				700,
				True
			],
			[
				"Class 1",
				800,
				1000,
				True
			],
			[
				"Math Assignment",
				1200,
				1400,
				False
			]
		] 	
	],
	["22", "March", "Tuesday",
		[
			[
				"Waking up",
				600,
				700,
				True
			],
			[
				"Class 3",
				1100,
				1200,
				True
			],
			[
				"Science Assignment",
				1600,
				1800,
				False
			]
		] 	
	]
]

@app.route('/testing')
def test():
	return str(len(dbs));

@app.route('/')
def index():
	return render_template("index.html", dbs = dbs, test=True)


app.run(debug=True, port=8000, host='0.0.0.0')