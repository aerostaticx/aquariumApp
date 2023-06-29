import MySQLdb

"""
Database class. Supports simple functions regarding adding and deleting from table.
"""
class myDB:
    db = MySQLdb.connect(host="aerostatic.mysql.pythonanywhere-services.com",user="aerostatic",password="mydatabasepassword",database="aerostatic$TemperatureDB",connect_timeout=31536000)

    """
    Ctor
    """
    def __init__(self):
        pass

    """
    Dtor. Used for closing DB connection.
    """
    def __del__(self):
        pass
        # self.db.close()

    """
    Used to check relog into mySQL incase timeout.

    Args:
        None
    Return:
        None
    """

    def relog(self):
        if(not self.db.open):
            self.db = MySQLdb.connect(host="aerostatic.mysql.pythonanywhere-services.com",user="aerostatic",password="mydatabasepassword",database="aerostatic$TemperatureDB",connect_timeout=31536000)


    """
    Used to add temperature to the database.

    Args:
        time: Datetime string
        temp: Temperature int

    Return:
        None
    """
    def addTemp(self, mcuID : str, time : str, temp : int) -> None:
        self.relog()
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
        self.relog()
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
        self.relog()
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
        self.relog()
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
        self.relog()
        cursor = self.db.cursor()
        if self.getProbeStatus(mcuID) is None:
            cursor.execute("INSERT INTO probe (mcuID, probeStatus) VALUES ('{}',{});".format(mcuID, setStatus))
            self.db.commit()
        else:
            cursor.execute("UPDATE probe SET probeStatus = {} WHERE mcuID = '{}';".format(setStatus, mcuID))
            self.db.commit()
        return