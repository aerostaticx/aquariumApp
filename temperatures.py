
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, jsonify, request, render_template, session
from flask_session import Session
from datetime import datetime
from pytz import timezone
from initDB import myDB

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip) #defines jinja zip function to be same as py zip for HTML use
app.config.update(SECRET_KEY="MyTotallSecreyKey")
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

tempDB = myDB()

#temperatures = []
#times = []
#probeEnabled = False

@app.route('/plotTemps')
def plotPlage() -> None:
    return render_template('plots.html',timeList=session.get('times',[]),tempList=session.get('temperatures',[]))

@app.route('/stopProbe', methods=["POST"])
def stopProbe() -> None:
    session['probeEnabled'] = False
    response = jsonify(response = "Probe disabled.", code = 200)
    return response

@app.route('/initiateProbe', methods=["POST"])
def initiateProbe() -> None:
    session['probeEnabled'] = True
    response = jsonify(response = "Probe enabled.", code = 200)
    return response

@app.route('/getProbeStatus', methods=["GET"]) #to be used by ESP32 to get probeEnabled status
def getProbeStatus() -> None:
    response = jsonify(response = {"Probe status" : session.get('probeEnabled',False)}, code = 200)
    return response

@app.route('/clearTemperature', methods=["POST"])
def clearTemperature() -> None:
    tempDB.deleteTemps()
    session['times'] =  []
    session['temperatures'] =  []
    session.modified = True
    response = jsonify(response = "Successfully cleared temperature.", code = 200)
    return response

@app.route("/", methods=["GET"])
def getTemperature() -> None:
    #session['times'] = []
    #session['temperatures'] = []
    return render_template('index.html',timeList=session.get('times',[]) or [],tempList=session.get('temperatures',[]) or [])

@app.route("/", methods=["POST"])
def addTemperature() -> None:
    tz = timezone('EST')

    time = datetime.now(tz)
    temp = request.get_json()["temperature"]

    timeTemp = session.get('times',[]) or []
    tempTemp = session.get('temperatures',[]) or []
    timeTemp.append(str(time))
    tempTemp.append(int(temp))

    session['times'] = timeTemp
    session['temperatures'] = tempTemp

    session.modified = True
    tempDB.addTemp(datetime.now(tz).strftime('%a %d %b %Y %I:%M%p'),temp)

    response = jsonify(response = "Successfully added temperature.", code = 201)
    return response
