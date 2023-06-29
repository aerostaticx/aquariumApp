from flask import jsonify, request, render_template, session, redirect, Blueprint
from datetime import datetime
from pytz import timezone
from initDB import myDB
import sys



routeBP = Blueprint('routeBP', __name__, template_folder='../templates')
tempDB = myDB()

@routeBP.route('/logout', methods=['POST'])
def logout() -> None:
    session.pop('username',None)
    return jsonify(response = "Logged out.", code = 200)

@routeBP.route('/loggedIn')
def loggedIn() -> None:
    if 'username' not in session:
        return "You're not logged in."
    return "You're logged in with user: " + session['username']

@routeBP.route('/login', methods=['POST'])
def login() -> None:
    session['username'] = request.form['username']
    return redirect('/loggedIn')

"""
Routes to the plot page where line graph is plotted of the data. X axis: datetime, Y axis: temperature

Args:
    None

Return:
    None
"""
@routeBP.route('/plotTemps')
def plotPage() -> None:
    if 'username' in session:
        retList = tempDB.getTemps(session['username'])
        return render_template('plots.html',timeList=[time[0] for time in retList],tempList=[temp[1] for temp in retList])
    else:
        return render_template('plots.html',timeList=[],tempList=[])


"""
Stops the data probe on the ESP32. Sets corresponding row in probes table to False

Args:
    None

Return:
    None
"""
@routeBP.route('/stopProbe', methods=["POST"])
def stopProbe() -> None:
    tempDB.setProbeStatus(session['username'],False)
    response = jsonify(response = "Probe disabled.", code = 200)
    return response

"""
Starts the data probe on the ESP32. Sets corresponding row in probes table to True.

Args:
    None

Return:
    None
"""
@routeBP.route('/initiateProbe', methods=["POST"])
def initiateProbe() -> None:
    tempDB.setProbeStatus(session['username'],True)
    response = jsonify(response = "Probe enabled.")
    return response, 200

"""
Used by ESP32 to get probeEnabled status. Requires POST because ESP32 needs to send it's mcuID.

Args:
    None

Return:
    None
"""
@routeBP.route('/getProbeStatus', methods=["POST"])
def getProbeStatus() -> None:
    probeEnabled = False
    mcuID = request.get_json()["mcuID"]
    result = tempDB.getProbeStatus(mcuID)
    if result is not None:
        probeEnabled = bool(result[0])
    response = jsonify(response = {"Probe status" : probeEnabled})
    return response, 200

"""
Clears data from internal lists, as well as the entries in the mySQL table.

Args:
    None

Return:
    None
"""
@routeBP.route('/clearTemperature', methods=["POST"])
def clearTemperature() -> None:
    tempDB.deleteTemps(session['username'])
    response = jsonify(response = "Successfully cleared temperature.")
    return response, 200

"""
Renders the landing page.

Args:
    None

Return:
    None
"""
@routeBP.route("/", methods=["GET"])
def getTemperature() -> None:
    if 'username' in session:
        print("Has user " + session['username'], file=sys.stderr)
        retList = tempDB.getTemps(session['username'])
        print("Has user " + session['username'] + str(len(retList)), file=sys.stderr)
        if retList:
            return render_template('index.html',timeList=[time[0] for time in retList],tempList=[temp[1] for temp in retList],loggedIn=True)
        else:
            return render_template('index.html',timeList=[],tempList=[],loggedIn=False)
    else:
        print("No user\n", file=sys.stderr)
        return render_template('index.html',timeList=[],tempList=[],loggedIn=False)

"""
Used by ESP32 to add data to internal lists as well as mySQL table.

Args:
    None

Return:
    None
"""
@routeBP.route("/", methods=["POST"])
def addTemperature() -> None:
    tz = timezone('EST')

    temp = request.get_json()["temperature"]
    mcuID = request.get_json()["mcuID"]

    tempDB.addTemp(mcuID,datetime.now(tz).strftime('%a %d %b %Y %I:%M%p'),temp)

    response = jsonify(response = "Successfully added temperature.")
    return response, 201