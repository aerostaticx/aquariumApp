import unittest
from unittest.mock import MagicMock
import sys
sys.path.append("..")
from initDB import myDB

'''
The purpose of this module is to test the DB functions.
'''

class test_InitDB(unittest.TestCase):

    '''
    Testing functionality of addTemp, getTemp, and deleteTemp
    GIVEN: addTemp - testHash ID, dummy timestamp, and temperature
           getTemps - testHash ID
           deleteTemps - testHash ID
    WHEN: functions called
    THEN: Database was populated with testHash, timestamp, and temperature. Get function returns the correct entry. Delete temps deletes from DB.
    '''
    testDB = myDB()
    def test_AddGetDeleteTemps(self):
        self.testDB.addTemp('testHash','Time1', 78)
        self.assertEqual(('Time1',78.0), self.testDB.getTemps('testHash')[0])

        self.testDB.deleteTemps('testHash')
        self.assertEqual((),self.testDB.getTemps('testHash'))

    '''
    Testing functionality of set and get probeStatus
    GIVEN: setProbeStatus - testHash ID, set bool
           getProbeStatus - testHash ID
    WHEN: functions called
    THEN: Database was populated with probe status True, then updated with False. Getter returns correct value from the DB.
    '''
    def test_getSetProbeStatus(self):
        self.testDB.setProbeStatus('testHash',True)
        self.assertTrue(self.testDB.getProbeStatus('testHash')[0])

        self.testDB.setProbeStatus('testHash',False)
        self.assertFalse(bool(self.testDB.getProbeStatus('testHash')[0]))

if __name__ == '__main__':
    unittest.main(exit=False)