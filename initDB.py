import MySQLdb
import sys

#TODO: See https://stackoverflow.com/questions/43663130/python-mysqldb-how-do-you-access-the-exception-error-code-in-operationalerror for specifying mySQLdb error code for try/catches.


"""
Database class. Supports simple functions regarding adding and deleting from table.
"""
class myDB:
    db = MySQLdb.connect(host="aerostatic.mysql.pythonanywhere-services.com",user="aerostatic",password="mydatabasepassword",database="aerostatic$TemperatureDB")

    """
    Ctor
    """
    def __init__(self):
        pass

    """
    Dtor. Used for closing DB connection.
    """
    def __del__(self):
        print("DB Dtor", file=sys.stderr)
        self.db.close()

    """
    Used to add temperature to the database.

    Args:
        time: Datetime string
        temp: Temperature int

    Return:
        None
    """
    def addTemp(self, mcuID : str, time : str, temp : int) -> None:
        try:
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO temps (mcuID, time, temp) VALUES ('{}','{}',{});".format(mcuID,time,temp))
        except MySQLdb.OperationalError:
            self.db = MySQLdb.connect(host="aerostatic.mysql.pythonanywhere-services.com",user="aerostatic",password="mydatabasepassword",database="aerostatic$TemperatureDB")
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO temps (mcuID, time, temp) VALUES ('{}','{}',{});".format(mcuID,time,temp))
        self.db.commit()

    """
    Used to delete entries in table.

    Args:
        mcuID: Unique mcuID string

    Return:
        None
    """
    def deleteTemps(self, mcuID : str) -> None:
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM temps WHERE mcuID = '{}';".format(mcuID))
        except MySQLdb.OperationalError:
            self.db = MySQLdb.connect(host="aerostatic.mysql.pythonanywhere-services.com",user="aerostatic",password="mydatabasepassword",database="aerostatic$TemperatureDB")
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM temps WHERE mcuID = '{}';".format(mcuID))
        self.db.commit()

    """
    Used to get entries in table.

    Args:
        mcuID: Unique mcuID string

    Return:
        List of tuples (datetime, temp)
    """
    def getTemps(self, mcuID : str) -> []:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT time,temp FROM temps WHERE mcuID = '{}';".format(mcuID))
        except MySQLdb.OperationalError:
            self.db = MySQLdb.connect(host="aerostatic.mysql.pythonanywhere-services.com",user="aerostatic",password="mydatabasepassword",database="aerostatic$TemperatureDB")
            cursor = self.db.cursor()
            cursor.execute("SELECT time,temp FROM temps WHERE mcuID = '{}';".format(mcuID))
        return cursor.fetchall()

    """
    Used to get probe status.

    Args:
        mcuID: Unique mcuID string

    Return:
        probeStatus
    """
    def getProbeStatus(self, mcuID : str) -> []:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT probeStatus FROM probe WHERE mcuID = '{}';".format(mcuID))
        except MySQLdb.OperationalError:
            self.db = MySQLdb.connect(host="aerostatic.mysql.pythonanywhere-services.com",user="aerostatic",password="mydatabasepassword",database="aerostatic$TemperatureDB")
            cursor = self.db.cursor()
            cursor.execute("SELECT probeStatus FROM probe WHERE mcuID = '{}';".format(mcuID))
        return cursor.fetchone()

    """
    Used to set probe status. If the mcuID does not exist, it will be added along with it's set value.

    Args:
        mcuID: Unique mcuID string
        probeStatus: Enabled or disabled bool

    Return:
        None
    """
    def setProbeStatus(self, mcuID : str, setStatus : bool) -> None:
        cursor = self.db.cursor()
        if self.getProbeStatus(mcuID) is None:
            try:
                cursor.execute("INSERT INTO probe (mcuID, probeStatus) VALUES ('{}',{});".format(mcuID, setStatus))
            except MySQLdb.OperationalError:
                self.db = MySQLdb.connect(host="aerostatic.mysql.pythonanywhere-services.com",user="aerostatic",password="mydatabasepassword",database="aerostatic$TemperatureDB")
                cursor.execute("INSERT INTO probe (mcuID, probeStatus) VALUES ('{}',{});".format(mcuID, setStatus))
            self.db.commit()
        else:
            try:
                cursor.execute("UPDATE probe SET probeStatus = {} WHERE mcuID = '{}';".format(setStatus, mcuID))
            except MySQLdb.OperationalError:
                self.db = MySQLdb.connect(host="aerostatic.mysql.pythonanywhere-services.com",user="aerostatic",password="mydatabasepassword",database="aerostatic$TemperatureDB")
                cursor.execute("UPDATE probe SET probeStatus = {} WHERE mcuID = '{}';".format(setStatus, mcuID))
            self.db.commit()
        return

    def startDosage(self, mcuID : str) -> None:
        try:
            cursor = self.db.cursor()
            cursor.execute("UPDATE dosing SET enabled = true WHERE mcuID = '{}';".format(mcuID))
        except MySQLdb.OperationalError:
            self.db = MySQLdb.connect(host="aerostatic.mysql.pythonanywhere-services.com",user="aerostatic",password="mydatabasepassword",database="aerostatic$TemperatureDB")
            cursor = self.db.cursor()
            cursor.execute("UPDATE dosing SET enabled = true WHERE mcuID = '{}';".format(mcuID))
        self.db.commit()

    def stopDosage(self, mcuID : str) -> None:
        try:
            cursor = self.db.cursor()
            cursor.execute("UPDATE dosing SET enabled = false WHERE mcuID = '{}';".format(mcuID))
        except MySQLdb.OperationalError:
            self.db = MySQLdb.connect(host="aerostatic.mysql.pythonanywhere-services.com",user="aerostatic",password="mydatabasepassword",database="aerostatic$TemperatureDB")
            cursor = self.db.cursor()
            cursor.execute("UPDATE dosing SET enabled = false WHERE mcuID = '{}';".format(mcuID))
        self.db.commit()


    def getDosage(self, mcuID : str) -> []:
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT days, timeMinutesPastMidnight, amount FROM dosing WHERE mcuID = '{}';".format(mcuID))
        except MySQLdb.OperationalError:
            self.db = MySQLdb.connect(host="aerostatic.mysql.pythonanywhere-services.com",user="aerostatic",password="mydatabasepassword",database="aerostatic$TemperatureDB")
            cursor = self.db.cursor()
            cursor.execute("SELECT days, timeMinutesPastMidnight, amount FROM dosing WHERE mcuID = '{}';".format(mcuID))
        return cursor.fetchone()

    def addDosage(self, mcuID : str, amount : int, days : str, time : str) -> None:
        if self.getDosage(mcuID) is None:
            try:
                cursor = self.db.cursor()
                cursor.execute("INSERT INTO dosing (mcuID, days, timeMinutesPastMidnight, amount) VALUES ('{}', '{}', '{}', {});".format(mcuID, days, time, amount))
            except MySQLdb.OperationalError:
                self.db = MySQLdb.connect(host="aerostatic.mysql.pythonanywhere-services.com",user="aerostatic",password="mydatabasepassword",database="aerostatic$TemperatureDB")
                cursor = self.db.cursor()
                cursor.execute("INSERT INTO dosing (mcuID, days, timeMinutesPastMidnight, amount) VALUES ('{}', '{}', '{}', {});".format(mcuID, days, time, amount))
            self.db.commit()
        else:
            try:
                cursor = self.db.cursor()
                cursor.execute("UPDATE dosing SET days = '{}', timeMinutesPastMidnight = '{}', amount = {};".format(days, time, amount))
            except MySQLdb.OperationalError:
                self.db = MySQLdb.connect(host="aerostatic.mysql.pythonanywhere-services.com",user="aerostatic",password="mydatabasepassword",database="aerostatic$TemperatureDB")
                cursor = self.db.cursor()
                cursor.execute("UPDATE dosing SET days = '{}', timeMinutesPastMidnight = '{}', amount = {};".format(days, time, amount))
            self.db.commit()

