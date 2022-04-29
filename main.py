import uvicorn
from fastapi import (
    FastAPI,
    Body,
    Depends
)
from app.model import (
    PostSchema,
    UserSchema,
    UserLoginSchema
)
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import JWTBearer

posts = {
    1: {
        "id": 1,
        "title": "penguins",
        "text": "Penguins are birds"
    }, 2:
    {
        "id": 2,
        "title": "Tigers",
        "text": "Tigers are cats"
    }, 3:
    {
        "id": 3,
        "title": "Hyenas",
        "text": "Hyenas are dogs"
    }
}

users = []

app = FastAPI()


@app.get("/", tags=["test"])
def greet():
    return {"Hello": "World!"}
# Simple test GET request


@app.get("/posts", tags=["posts"])
def get_posts():
    return {"data": posts}
# Get Posts


@app.get("/posts/{id}", tags=["posts"])
def get_one_post(id: int):
    if id not in posts:
        return {
            "error": "Post with this ID does not exist"
        }
    return {"data": posts[id]}
# Get Posts by id


@app.post('/posts', dependencies=[Depends(JWTBearer())], tags=["posts"])
def add_post(post: PostSchema):
    post.id = len(posts.keys()) + 1
    posts[post.id] = post.dict()
    return {
        "info": "Post Added!"
    }
# Add a blog post


@app.post("/user/signup", tags=["user"])
def user_signup(user: UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)
# User Signup


def check_user(data: UserLoginSchema):
    for user in users:
        if (user.email == data.email and
                user.password == data.password):
            return True
    return False


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {
            "error": "Invalid login details! "
        }


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=9000,
        reload=True
    )
