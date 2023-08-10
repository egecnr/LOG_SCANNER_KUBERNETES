import json

class LogonFailure:
   event_timestamp=""
   session_id="" 
   dbusername=""
   action_name=""
   return_code=""
   unified_audit_policies=""
   userhost=""
   number_of_attempts=""
   
   def __init__(self,event_timestamp,session_id,dbusername,action_name,return_code,unified_audit_policies,userhost,number_of_attempts):
        self.event_timestamp= event_timestamp
        self.session_id=session_id
        self.dbusername=dbusername
        self.action_name=action_name
        self.return_code=return_code
        self.unified_audit_policies=unified_audit_policies
        self.userhost=userhost
        self.number_of_attempts=number_of_attempts

   def to_json(self):
         json_input =   {
                "input": {
                     "event_timestamp": self.event_timestamp,
                     "session_id": self.session_id,
                     "dbusername": self.dbusername,
                     "action_name": self.action_name,
                     "return_code": self.return_code,
                     "unified_audit_policies": self.unified_audit_policies,
                     "userhost": self.userhost,
                     "number_of_attempts": self.number_of_attempts
                }
         }
         return json_input
         