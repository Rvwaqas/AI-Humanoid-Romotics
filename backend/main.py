import uvicorn
from fastapi import FastAPI
from .src.api import auth, features, chat
from .src.models.user import init_db

app = FastAPI()

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(features.router, prefix="/api/features", tags=["features"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

@app.on_event("startup")
def on_startup():
    init_db()
    print("Database initialized and tables created")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI-Humanoid-Robotics Backend!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)