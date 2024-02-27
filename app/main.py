from fastapi.params import Body
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

class po(BaseModel):
    title:str
    content:str
    rating: Optional[int] = None


db = [
    {"title":"title 1","content":"content 1","id":1},
    {"title":"title 2","content":"content 2","id":2},
    {"title":"title 3","content":"content 3","id":3}
]

def find_id(id):
    for i in db:
        if i["id"] == id:
            return i

def find_index_post(id):
    for i, p in enumerate(db):
        if p["id"] == id:
            return i 


app = FastAPI()


@app.get("/post")
async def all_post():
    return {"message": db}

@app.post("/post", status_code=status.HTTP_201_CREATED)
async def creat_post(Post:po):
    post_dict = Post.dict()
    post_dict['id'] = randrange(0,999999)
    db.append(post_dict)
    return {"New Post": post_dict}

@app.get("/post/latests")
async def latests_post():
    post = db[len(db)-1]
    return {"Message": post}


@app.get("/post/{id}")
async def id_post(id: int, res: Response):
    post = find_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found.")
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {"Massage": f"Post with id {id} was not found."}
    return {"Message": post}

@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    db.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/post/{id}")
async def update_post(id: int, post:po):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    
    post_dict = post.dict()
    post_dict['id'] = id
    db[index] = post_dict
    return {"Data":db[index]}

# venv\Scripts\activate.bat
# python -m uvicorn app.main:app --reload