from fastapi import FastAPI

from config import database

database.Database('database', 'admin', '12341').check_if_exits()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

