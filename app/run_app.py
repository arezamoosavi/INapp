import json
from fastapi import FastAPI
from db.handler import pgQuery
from pydantic import BaseModel

app = FastAPI()

pg = pgQuery()


@app.get("/")
async def read_root():

    dict_Values = await pg.getAll(database="userstatus")

    return {"Hello": "World", "all users are": json.dumps(dict_Values)}


class User(BaseModel):
    username: str
    password: str


@app.post("/post_user/")
async def create_item(sent_data: User):
    saved = await pg.saveData(
        database="userstatus", username=sent_data.username, password=sent_data.password
    )

    return {"messege": "Successfully Done!", "response": "Saved!"}
