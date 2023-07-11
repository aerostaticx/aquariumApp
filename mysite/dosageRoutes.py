from flask import jsonify, request, render_template, session, redirect, Blueprint
from datetime import datetime
from pytz import timezone
from initDB import myDB
import sys

dosageRouteBP = Blueprint('dosageRouteBP', __name__, template_folder='../templates')
tempDB = myDB()

@dosageRouteBP.route('/dosageHome', methods=['GET'])
def dosageHome() -> None:
    if 'username' in session:
        print("Has DosageUser " + session['username'], file=sys.stderr)
        return render_template('dosage.html')
    else:
        print("No DosageUser\n", file=sys.stderr)
        return render_template('dosage.html')

@dosageRouteBP.route('/dosageStore', methods=['POST'])
def dosageStore() -> None:
    daysString = ""
    req = request.form
    print("Dose {}".format(req['mc']), file=sys.stderr)
    for entry in req:
        if entry != "time" and entry != "amount":
            if req[entry] == "true":
                if entry == "mc":
                    daysString += 'M'
                elif entry == "tc":
                    daysString += 'T'
                elif entry == "wc":
                    daysString += 'W'
                elif entry == "rc":
                    daysString += 'R'
                elif entry == "fc":
                    daysString += 'F'
                elif entry == "sc":
                    daysString += 'S'
                else:
                    daysString += 'X'
    minAfterMid = int(req['time'][:2], 10) + int(req['time'][3:5], 10)
    tempDB.addDosage(session['username'], req['amount'], daysString, minAfterMid)

    return jsonify(response = "Dosing stored."), 200
