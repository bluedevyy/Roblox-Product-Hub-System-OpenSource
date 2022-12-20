from fastapi import FastAPI
import pymongo
from ..main import MONGOURI
import uvicorn

client3 = pymongo.MongoClient(MONGOURI)
db3 = client3.data
collection3 = db3.users

app = FastAPI()

@app.route("/v1/status", methods=["GET"])
async def status():
    return {"Message": "OK"}

@app.route("/v1/users/status", methods=["GET"])
async def users():
    return {"UsersAPI": "OK"}