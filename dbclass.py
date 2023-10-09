#import cx_Oracle
import oracledb
from datetime import datetime, timedelta
import pytz
from zoneinfo import ZoneInfo
from LogonFailures import LogonFailure
import json
from opa_client.opa import OpaClient


class DbConnection:

    username="system"
    password="root"
    dsnInformation=""
    connectionDB=""
    lastChecked="sysdate"
    cursor = ""
    opaClient=""

    def __init__(self,username,password,dsnInformation):
        self.username= username
        self.password=password
        self.dsnInformation=dsnInformation
        self.connectDB()


    def connectDB(self):
            #self.connectionDB = cx_Oracle.connect(user= self.username, password= self.password, dsn=self.dsnInformation ,encoding="UTF-8")
            self.connectionDB = oracledb.connect(user= self.username, password= self.password, dsn=self.dsnInformation ,encoding="UTF-8")
            self.setLatestTime()
            self.cursor = self.connectionDB.cursor()
            self.opaClient= OpaClient("10.42.0.215",8181,"v1")
            print(self.opaClient.check_connection())
            


    def getLogonFailures(self):
       
         cursor = self.connectionDB.cursor()
         print(self.lastChecked)
         query = """SELECT to_char(event_timestamp,'dd.mm.yyyy hh24:mi:ss') event_timestamp, sessionid, dbusername, action_name, return_code, unified_audit_policies, USERHOST 
         FROM unified_audit_trail WHERE event_timestamp >= TO_DATE('"""+  str(self.lastChecked) +"""','DD.MM.YY HH24:MI:SS') 
         AND unified_audit_policies='ORA_LOGON_FAILURES'  ORDER BY event_timestamp"""
         
           # "SELECT to_char(event_timestamp,'dd.mm.yy hh24:mi:ss') event_timestamp, sessionid, dbusername, action_name, return_code, unified_audit_policies FROM unified_audit_trail WHERE event_timestamp > TO_DATE('13.07.2023 13:21:03','DD.MM.YY HH24:MI:SS') AND UNIFIED_AUDIT_POLICIES = 'SYSTEM_ALL_POLICIES' OR UNIFIED_AUDIT_POLICIES ='ORA_LOGON_FAILURES' ORDER BY event_timestamp
         cursor.execute(query)
         print(query)
         values = cursor.fetchall()
         print(len(values))
         self.setLatestTime()
         print(self.lastChecked)
         return self.filterLogonFailures(values)
        
    

    def filterLogonFailures(self, values):
         print("We arrived here")
         filteredPolicyResponses = []
         print("We also arrived here")

         for v in values:
              old_time=v[0]
              updated_time= datetime.strptime(old_time, '%d.%m.%Y %H:%M:%S') - timedelta(minutes=5)
              formatted_updated_time = updated_time.strftime("%d.%m.%Y %H:%M:%S")
              dbusername=v[2]
              userhost=v[6]
              query = """SELECT COUNT (*) FROM unified_audit_trail WHERE event_timestamp <= TO_DATE('"""+  str(old_time) +"""','DD.MM.YY HH24:MI:SS') 
              AND event_timestamp > TO_DATE('"""+  str(formatted_updated_time) +"""','DD.MM.YY HH24:MI:SS') 
              AND  UNIFIED_AUDIT_POLICIES ='ORA_LOGON_FAILURES' AND USERHOST= '"""+  str(userhost) +"""' 
              AND DBUSERNAME= '"""+  str(dbusername) +"""'ORDER BY event_timestamp"""
              
              self.cursor.execute(query)
              print("We also arrived here too")
              number_of_attempts=self.cursor.fetchone()
              logon_failure= LogonFailure(v[0],v[1],v[2],v[3],v[4],v[5],v[6],number_of_attempts[0]+1)
              
              ## Add each policy to the list to send it as a response
              policy = self.enterPolicy(logon_failure.to_json())
              print(str(policy))
              if(len(str(policy)) > 1):
                filteredPolicyResponses.append(policy)
         return filteredPolicyResponses
         
              

    def enterPolicy(self,jsonvalue):
         self.opaClient.update_opa_policy_fromfile("policies/logon_failure.rego",endpoint="logon-failures")  
         return self.opaClient.check_permission(input_data=jsonvalue,policy_name="logon-failures",rule_name="alert")   
  


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
        
            

        
