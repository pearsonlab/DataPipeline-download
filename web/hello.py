from __future__ import print_function

from flask import Flask, render_template, flash, Markup
from flask import request, redirect
from datetime import datetime
import database
import queryDynamo

app = Flask(__name__)
app.secret_key = '123'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/datepicker', methods=['GET', 'POST'])
def datepicker():
    if request.method == 'POST':
        startTime = request.form['start']
        # startTime is str type
        stopTime = request.form['stop']
        start = datetime.strptime(startTime, "%Y/%m/%d %H:%M")
        stop = datetime.strptime(stopTime, "%Y/%m/%d %H:%M")
        print("You entered the start time as: ", start)
        print("You entered the stop time as: ", stop)
        database.timeRange(start, stop)
        return redirect('/')
    return render_template('datepicker.html')

@app.route('/participant', methods=['GET', 'POST'])
def participant():
    if request.method == 'POST':
        patientId = request.form['participantId']
        print("You entered the participant ID as: ", patientId)
        database.patientID(patientId)
        return redirect('/')

    return render_template('participant.html')


@app.route('/task', methods=['GET', 'POST'])
def task():
    if request.method == 'POST':
        task = request.form['task']
        print("You entered this task: '" + task + "'")
        queryDynamo.experimentName(task)
        return redirect('/')

    return render_template('task.html')

def dateConverter(dateTime):
    return datetime.datetime.strptime(datetime, "%Y/%m/%d %H:%M")

if __name__ == "__main__":
    app.debug = True
    app.run()