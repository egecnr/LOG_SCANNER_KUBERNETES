from fastapi import FastAPI
from dbclass import DbConnection
import time

app = FastAPI()
app.connection=""

@app.get("/api")
async def root():
    app.connection= DbConnection("system","root","10.42.0.87:1521/ORCLCDB")
    print('Connected to Db')
    return "Welcome to the Dam demo!!"




@app.get("/api/logon-failures")   
async def GetLogonFailures():
        print('Listening on database activity')
        for x in range (3):
            response = app.connection.getLogonFailures()
            print("got the results")
            print(response)
            print("waiting for the next audit check")
            time.sleep(20)
    