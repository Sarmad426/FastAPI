from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="Path and Query parameters")

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


# Path Parameters
@app.get('/{item_id}')
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
def read_item_by_query(item_id:int = 1):
    try:
        for item in FAKE_DATA:
            if item['id'] == item_id:
                data_item = item
                return data_item
        return JSONResponse(status_code=404,content={"error": {"code": 404, "message": "No item found"}})
    except Exception as e:
        return HTTPException(status_code=404,detail='No item found')
    
# Type a url like that <http://127.0.0.1:8000/?item_id=4>

# For multiple query parameters <http://127.0.0.1:8000/items/?skip=0&limit=10>

# Official docs: 
# - <https://fastapi.tiangolo.com/tutorial/query-params/>
# - <https://fastapi.tiangolo.com/tutorial/path-params/>