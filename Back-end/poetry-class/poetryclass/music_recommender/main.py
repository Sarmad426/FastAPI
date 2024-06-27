from typing import Union

from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
from sklearn.tree import DecisionTreeClassifier


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

music_data = pd.read_csv("./music_data_set.csv")

# input set
X = music_data.drop(columns=["genre"])

# output set
y = music_data["genre"]

model = DecisionTreeClassifier()
model.fit(X.values, y)

prediction = model.predict([[21, 1], [22, 0]])


@app.get("/")
def read_root():
    return {"Hello": {prediction[0]}}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# @app.post("/recommend")
# def recommend_music(age: int, gender: int):
#     """
#     Recommends music
#     """
#     predict = model.predict([[age, gender]])
#     return predict[0]


class RecommendationRequest(SQLModel):
    age: int
    gender: int


@app.post("/recommend")
def recommend_music(request: RecommendationRequest):
    """
    Recommends music
    """
    predict = model.predict([[request.age, request.gender]])
    return predict[0]
