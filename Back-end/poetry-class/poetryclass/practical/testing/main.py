from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def greet():
    return 'Hello'


@app.get('/{name}')
def greet(name:str):
    return f'Hello {name}'