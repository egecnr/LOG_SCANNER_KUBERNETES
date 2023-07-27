from fastapi import FastAPI
from dbclass import DbConnection
import time

app = FastAPI()

@app.get("/api")
async def root():
    connection=  DbConnection()
    print('Connected to Db')
    print('Listening on database activity')
    for x in range (3):
     response = connection.getAuditLogs()
     print("got the results")
     print(response)
     print("waiting for the next audit check")
     time.sleep(5)
     
    
    

      
