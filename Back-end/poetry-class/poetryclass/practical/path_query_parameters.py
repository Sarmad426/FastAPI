from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from enum import Enum

FAKE_DATA = [
    {
        'id':1,
        'title':'The Raven',
    },{
        'id':2,
        'title':'The Road Not Taken',
    },
    {
        'id':3,
        'title':'Alternatives to the Self',
    },
    {
        'id':4,
        'title':'Bring the glory',
    },
    {
        'id':5,
        'title':'The viper'
    }
]

app = FastAPI(title="Path and Query parameters")


# Path Parameters
@app.get('/items/{item_id}')
def read_item_by_id(item_id:int):
    try:
        for item in FAKE_DATA:
            if item['id'] == item_id:
                return item
        return JSONResponse(status_code=404,content={"error": {"code": 404, "message": "No item found"}})
    except Exception as e:
        return HTTPException(status_code=404,detail='No item found')

# Query parameters
@app.get('/')
def read_item_by_query(item_id:int):
    try:
        for item in FAKE_DATA:
            if item['id'] == item_id:
                return item
        return JSONResponse(status_code=404,content={"error": {"code": 404, "message": "No item found"}})
    except Exception as e:
        return HTTPException(status_code=404,detail='No item found')
    
# Type a url like that <http://127.0.0.1:8000/?item_id=4>

# For multiple query parameters <http://127.0.0.1:8000/items/?skip=0&limit=10>

# Path parameters example from the docs

class ModelName(str,Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# Official docs: 
# - <https://fastapi.tiangolo.com/tutorial/query-params/>
# - <https://fastapi.tiangolo.com/tutorial/path-params/>
