import cx_Oracle
#import oracledb
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

    def __init__(self):
        self.username= "system"
        self.password="root"
        self.dsnInformation="10.42.0.50:1521/ORCLCDB" 
        self.connectDB()


    def connectDB(self):
            self.connectionDB = cx_Oracle.connect(user= "system", password= "root", dsn="10.42.0.50:1521/ORCLCDB" ,encoding="UTF-8")
            #self.connectionDB = cx_Oracle.connect(user= "system", password= "root", dsn="10.42.0.50:1521/ORCLCDB" ,encoding="UTF-8")


    def getAuditLogs(self):
         cursor= self.connectionDB.cursor()
         print(self.lastChecked)
         if(self.lastChecked=="sysdate"):
           query = """SELECT to_char(event_timestamp,'dd.mm.yy hh24:mi:ss') event_timestamp, sessionid, dbusername, action_name, return_code, unified_audit_policies FROM unified_audit_trail WHERE event_timestamp > """+  str(self.lastChecked) +""" AND (UNIFIED_AUDIT_POLICIES = 'SYSTEM_ALL_POLICIES' OR UNIFIED_AUDIT_POLICIES ='ORA_LOGON_FAILURES') ORDER BY event_timestamp"""
         else:
           query = """SELECT to_char(event_timestamp,'dd.mm.yy hh24:mi:ss') event_timestamp, sessionid, dbusername, action_name, return_code, unified_audit_policies FROM unified_audit_trail WHERE event_timestamp > TO_DATE('"""+  str(self.lastChecked) +"""','DD.MM.YY HH24:MI:SS') AND (UNIFIED_AUDIT_POLICIES = 'SYSTEM_ALL_POLICIES' OR UNIFIED_AUDIT_POLICIES ='ORA_LOGON_FAILURES') ORDER BY event_timestamp"""
           # "SELECT to_char(event_timestamp,'dd.mm.yy hh24:mi:ss') event_timestamp, sessionid, dbusername, action_name, return_code, unified_audit_policies FROM unified_audit_trail WHERE event_timestamp > TO_DATE('13.07.2023 13:21:03','DD.MM.YY HH24:MI:SS') AND UNIFIED_AUDIT_POLICIES = 'SYSTEM_ALL_POLICIES' OR UNIFIED_AUDIT_POLICIES ='ORA_LOGON_FAILURES' ORDER BY event_timestamp
         print(query)
         
         cursor.execute(query)
         values = cursor.fetchall()
       

         tz = pytz.timezone('Europe/Amsterdam')
         now = datetime.now(ZoneInfo('Europe/Amsterdam'))
         self.lastChecked=now.strftime("%d.%m.%Y %H:%M:%S") 
         #self.lastChecked = str(datetime.now(tz).day)+ "." + str(datetime.now(tz).month)+"."+ str(datetime.now(tz).year)+" "+ str(datetime.now(tz).hour)+ ":"+str(datetime.now(tz).minute)+":"+str(datetime.now(tz).second)
         print(self.lastChecked)
         print(self.lastChecked)       
         self.jsonConversion(values)     
         return values
    

    def returnTheLatestDate(self,values):
         returnRecord=""
         for record in values:
              returnRecord=record
         return str(returnRecord[0])


    def jsonConversion(self,values):
        listOfJsonObjects= []
        for v in values:
            newObject = {
                "event_timestamp" : str(v[0]),
                "sessionid" : str(v[1]),
                "dbusername": str(v[2]),
                "action_name": str(v[3]),
                "return_code": str(v[4]),
                "unified_audit_policies": (v[5])
            }
            print(newObject)
            listOfJsonObjects.append(newObject)
        return listOfJsonObjects
        
            

        
