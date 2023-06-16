import MySQLdb

class myDB:
    db = MySQLdb.connect(host="aerostatic.mysql.pythonanywhere-services.com",user="aerostatic",password="mypassword",database="aerostatic$TemperatureDB")

    def __init__(self):
        pass

    def __del__(self):
        self.db.close()

    def addTemp(self, time : str, temp : int) -> None:
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO temps (time, temp) VALUES ('{}',{});".format(time,temp))
        self.db.commit()

    def deleteTemps(self) -> None:
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM temps")
        self.db.commit()
