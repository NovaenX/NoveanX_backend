from fastapi import FastAPI
from .db import lifespan
from .api import foods

app = FastAPI(lifespan=lifespan)
app.include_router(foods.router)
