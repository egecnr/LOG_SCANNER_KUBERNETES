from fastapi import FastAPI
from dbclass import DbConnection
import time

app = FastAPI()
app.connection=""

@app.get("/api")
async def root():
    app.connection= DbConnection("system","root","10.42.0.177:1521/ORCLCDB")
    print('Connected to Db')
    return "Welcome to the Dam demo!!"




@app.get("/api/logon-failures")   
async def GetLogonFailures():
            response = app.connection.getLogonFailures() 
            return response
    