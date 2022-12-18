from fastapi import FastAPI

app = FastAPI()

@app.route("/v1/status", methods=["GET"])
async def status():
    return {"Message": "OK"}