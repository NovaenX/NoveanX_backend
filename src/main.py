from fastapi import FastAPI
from .database import lifespan
from .routers import food

app = FastAPI(title="Jarvis", lifespan=lifespan)  # type: ignore

# Include routers
app.include_router(food.router)
