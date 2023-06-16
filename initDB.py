import MySQLdb

"""
Database class. Supports simple functions regarding adding and deleting from table.
"""
class myDB:
    db = MySQLdb.connect(host="aerostatic.mysql.pythonanywhere-services.com",user="aerostatic",password="mypassword",database="aerostatic$TemperatureDB")

    """
    Ctor
    """
    def __init__(self):
        pass

    """
    Dtor. Used for closing DB connection.
    """
    def __del__(self):
        self.db.close()

    """
    Used to add temperature to the database.

    Args:
        time: Datetime string
        temp: Temperature int

    Return:
        None
    """
    def addTemp(self, time : str, temp : int) -> None:
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO temps (time, temp) VALUES ('{}',{});".format(time,temp))
        self.db.commit()

    """
    Used to delete entries in table.

    Args:
        None

    Return:
        None
    """
    def deleteTemps(self) -> None:
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM temps")
        self.db.commit()
