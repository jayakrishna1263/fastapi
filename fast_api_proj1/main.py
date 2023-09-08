from fastapi import FastAPI
from enum import Enum
from typing import Union
from pydantic import BaseModel

app=FastAPI()

class ModelName(str,Enum):
    alexnet="alexnet"
    resnet="resnet"
    lenet="lenet"


fake_items_db=[{"item_name":"Foo"},{"item_name":"Bar"},{"item_name":"Baz"}]


@app.get("/items/me")
async def read_user_me():
    return {"user_id": "The current user"}

# Path parameters
# http://127.0.0.1:8000/items/2

@app.get("/items/{item_id}")
async def read_user(item_id:int):
    return {"Item_Id":item_id}

@app.get("/models/{model_name}")
async def get_model(model_name:ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name":model_name,"message":"Deep Learning FTW!"}
    if model_name.value=="lenet":
        return {"model_name":model_name,"message":"LeCNN all the images"}
    return {"model_name":model_name,"message":"Have some residuals"}

@app.get("/files/{file_path:path}")
async def read_file(file_path:str):
    return {"file_path":file_path}



# Query parameters
# http://127.0.0.1:8000/items/?skip=1&limit=5
# http://127.0.0.1:8000/items/?skip=2
# http://127.0.0.1:8000/items/?limit=3

@app.get("/items/")
async def read_items(skip:int=0,limit:int=10):
    return fake_items_db[skip:skip+limit]


# Optional Parameters
# http://127.0.0.1:8000/teams/jk?teampk=123
# http://127.0.0.1:8000/teams/jk

@app.get("/teams/{team_id}")
# async def read_item(team_id:str,team_pk=None):
async def read_team(team_id:str,teampk=None):
    if teampk:
        return {"team_id":team_id,"team_pk":teampk}
    return {"team_id":team_id}

# Query parameter type conversion
# http://127.0.0.1:8000/items2/foo?q=[jk]
# http://127.0.0.1:8000/items2/foo?q=[jk]&short=True


@app.get("/items2/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# Multiple path and query parameters
# http://127.0.0.1:8000/users/12/items/jk1
# http://127.0.0.1:8000/users/12/items/jk1?q=123
# http://127.0.0.1:8000/users/12/items/jk1?q=123&short=False

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# Required query parameters
# http://127.0.0.1:8000/items3/foo?item_name=mac
# http://127.0.0.1:8000/items3/foo    ---  gives error

@app.get("/items3/{item_id}")
async def read_user_item(item_id: str, item_name: str):
    item = {"item_id": item_id, "item_name": item_name}
    return item




