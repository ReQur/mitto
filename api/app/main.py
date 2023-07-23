from fastapi import FastAPI
from app.routes import account, websocket, chat
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(account.router)
app.include_router(websocket.router)
app.include_router(chat.router)

origins = [
    "http://localhost:4200",
    "http://localhost:4201",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
