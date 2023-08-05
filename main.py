from fastapi import FastAPI
from dbclass import DbConnection
import time

app = FastAPI()

@app.get("/api")
async def root():
    return "Welcome to the Dam demo!!"



@app.get("/api/logon-failures")   
async def GetLogonFailures():
        connection=  DbConnection()
        print('Connected to Db')
        print('Listening on database activity')
        for x in range (3):
            response = connection.getLogonFailures()
            print("got the results")
            print(response)
            print("waiting for the next audit check")
            time.sleep(20)
    