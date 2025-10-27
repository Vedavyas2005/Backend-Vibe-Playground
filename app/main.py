from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, sessions, code

app = FastAPI(title="Ethercraft Vibe Coding Playground Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(sessions.router)
app.include_router(code.router)
