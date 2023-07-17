from fastapi import FastAPI
from app.routes import account, websocket, chat

app = FastAPI()

app.include_router(account.router)
app.include_router(websocket.router)
app.include_router(chat.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
