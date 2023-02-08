from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()  # Main application instance


class Post(BaseModel):  # Pydantic Data Model
    title: str
    content: str
    draft: bool = False


while True:  # Database Connection
    try:
        conn = psycopg2.connect(
            host='localhost', database='fastapi', user='postgres', password="password", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected succesfully!")
        break
    except Exception as error:
        print("Database connection failed.")
        print(error)
        time.sleep(5)


@app.get("/")  # Index Endpoint
def index():
    return {"message": "hello"}


# *** API endpoints ***


""" Retrive all of the posts """


@app.get("/posts")
def get_all_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"posts": posts}


""" Retrive a single post from the database """


@app.get("/posts/{id}")
def get_single_post(id: int, response: Response):

    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This post doesn't exist!")
    return post
    # try:
    #     return my_posts[id-1]
    # except IndexError:
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # rsp = {"msg": "The data you requested doesn't exist"}
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail="The data you requested doesn't exist")


"""--- Create a new post ---"""


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    cursor.execute(
        """INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *""", (payload.title, payload.content))
    new_post = cursor.fetchone()
    conn.commit()
    return new_post


"""--- Delete an existing post ---"""


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int):
    # try:
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    deleted_post = cursor.fetchone()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This post doesn't exist")
    conn.commit()
    return deleted_post
    # except IndexError:
    #     return Response(status_code=status.HTTP_404_NOT_FOUND)


"""--- Update an existing post ---"""


@app.put("/posts/{id}")
def update(id: int, payload: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *",
                   (payload.title, payload.content, id))
    updated_post = cursor.fetchone()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This post doesn't exist!")
    conn.commit()
    return updated_post
