from flask import Flask, jsonify, request, render_template
from flask_session import Session
from datetime import datetime
from pytz import timezone
from initDB import myDB

"""
Initialize app and configure for sessions (to be implemented in future).

This file defines API endpoints for the webserver, mostly POST and GET.
"""
app = Flask(__name__)
app.jinja_env.globals.update(zip=zip) #defines jinja zip function to be same as py zip for HTML use
app.config.update(SECRET_KEY="MyTotallSecreyKey")
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

"""
Yeah, globals because sessions don't work nice with ESP32.

TODO: Either pass/return relevant variables or use classes.
"""
tempDB = myDB()
temperatures = []
times = []
probeEnabled = False

"""
Routes to the plot page where line graph is plotted of the data. X axis: datetime, Y axis: temperature

Args:
    None

Return:
    None
"""
@app.route('/plotTemps')
def plotPlage() -> None:
    return render_template('plots.html',timeList=times, tempList=temperatures)


"""
Stops the data probe on the ESP32. Simply sets a global variable for the ESP32 to read in.

Args:
    None

Return:
    None
"""
@app.route('/stopProbe', methods=["POST"])
def stopProbe() -> None:
    global probeEnabled
    probeEnabled = False
    response = jsonify(response = "Probe disabled.", code = 200)
    return response

"""
Starts the data probe on the ESP32. Simply sets a global variable for the ESP32 to read in.

Args:
    None

Return:
    None
"""
@app.route('/initiateProbe', methods=["POST"])
def initiateProbe() -> None:
    global probeEnabled
    probeEnabled = True
    response = jsonify(response = "Probe enabled.", code = 200)
    return response

"""
Endpoint used by ESP32 to get probeEnabled status

Args:
    None

Return:
    None
"""
@app.route('/getProbeStatus', methods=["GET"])
def getProbeStatus() -> None:
    response = jsonify(response = {"Probe status" : probeEnabled}, code = 200)
    return response

"""
Clears data from internal lists, as well as the entries in the mySQL table.

Args:
    None

Return:
    None
"""
@app.route('/clearTemperature', methods=["POST"])
def clearTemperature() -> None:
    tempDB.deleteTemps()
    temperatures.clear()
    times.clear()
    response = jsonify(response = "Successfully cleared temperature.", code = 200)
    return response

"""
Renders the landing page.

Args:
    None

Return:
    None
"""
@app.route("/", methods=["GET"])
def getTemperature() -> None:
    return render_template('index.html',timeList=times,tempList=temperatures)

"""
Used by ESP32 to add data to internal lists as well as mySQL table.

Args:
    None

Return:
    None
"""
@app.route("/", methods=["POST"])
def addTemperature() -> None:
    tz = timezone('EST')

    time = datetime.now(tz)
    temp = request.get_json()["temperature"]

    temperatures.append(int(temp))
    times.append(str(time))

    tempDB.addTemp(datetime.now(tz).strftime('%a %d %b %Y %I:%M%p'),temp)

    response = jsonify(response = "Successfully added temperature.", code = 201)
    return response
