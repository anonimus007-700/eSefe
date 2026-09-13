from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

import database


class User(BaseModel):
    username: str
    email: str
    password: str
    is_admin: bool = False

db = database.Database('database', 'admin', '12341')
db.check_if_exits()
db.open_database_connection()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/user_register")
def user_register(user: User):
    db.add_user(user.username, user.email, user.password, user.is_admin)
    return user

@app.get("/user_register")
def get_users():
    all_users = db.write_test_command("SELECT * FROM users;")
    return {i for i in all_users.fetchall()}

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.0.102", port=5000)

