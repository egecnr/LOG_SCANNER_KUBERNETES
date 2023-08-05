#import cx_Oracle
import oracledb
from datetime import datetime, timezone
import pytz
from zoneinfo import ZoneInfo
import json


class DbConnection:

    username="system"
    password="root"
    dsnInformation=""
    connectionDB=""
    lastChecked="sysdate"
    cursor = ""

    def __init__(self):
        self.username= "system"
        self.password="root"
        self.dsnInformation="10.42.0.78:1521/ORCLCDB"
        self.connectDB()


    def connectDB(self):
            #self.connectionDB = cx_Oracle.connect(user= "system", password= "root", dsn="10.42.0.50:1521/ORCLCDB" ,encoding="UTF-8")
            self.connectionDB = oracledb.connect(user= self.username, password= self.password, dsn=self.dsnInformation ,encoding="UTF-8")
            self.setLatestTime()
            self.cursor = self.connectionDB.cursor()


    def getLogonFailures(self):
         cursor = self.connectionDB.cursor()
         query = """SELECT to_char(event_timestamp,'dd.mm.yy hh24:mi:ss') event_timestamp, sessionid, dbusername, action_name, return_code, unified_audit_policies, USERHOST FROM unified_audit_trail WHERE event_timestamp > TO_DATE('"""+  str(self.lastChecked) +"""','DD.MM.YY HH24:MI:SS') AND  UNIFIED_AUDIT_POLICIES ='ORA_LOGON_FAILURES' ORDER BY event_timestamp"""
           # "SELECT to_char(event_timestamp,'dd.mm.yy hh24:mi:ss') event_timestamp, sessionid, dbusername, action_name, return_code, unified_audit_policies FROM unified_audit_trail WHERE event_timestamp > TO_DATE('13.07.2023 13:21:03','DD.MM.YY HH24:MI:SS') AND UNIFIED_AUDIT_POLICIES = 'SYSTEM_ALL_POLICIES' OR UNIFIED_AUDIT_POLICIES ='ORA_LOGON_FAILURES' ORDER BY event_timestamp
         print(query)
         
         cursor.execute(query)
         values = cursor.fetchall()
         self.setLatestTime()
         self.jsonConversion(values)     
         return values
    

    def filterLogonFailures(self, values):

         for v in values:
              old_time=""
              updated_time=""
              userhost=""
              query = """SELECT COUNT (*) FROM unified_audit_trail WHERE event_timestamp > TO_DATE('"""+  str(updated_time) +"""','DD.MM.YY HH24:MI:SS') AND  UNIFIED_AUDIT_POLICIES ='ORA_LOGON_FAILURES' AND USERHOST= '"""+  str(userhost) +"""' ORDER BY event_timestamp"""

              
    

    def setLatestTime(self):
         tz = pytz.timezone('Europe/Amsterdam')
         now = datetime.now(ZoneInfo('Europe/Amsterdam'))
         self.lastChecked=now.strftime("%d.%m.%Y %H:%M:%S") 


    def jsonConversion(self,values):
        listOfJsonObjects= []
        for v in values:
            print(v)
            newObject = {
                "event_timestamp" : str(v[0]),
                "sessionid" : str(v[1]),
                "dbusername": str(v[2]),
                "action_name": str(v[3]),
                "return_code": str(v[4]),
                "unified_audit_policies": (v[5]),
                "USERHOST" : str(v[6])
            }
            print(newObject)
            listOfJsonObjects.append(newObject)
        return listOfJsonObjects
        
            

        
