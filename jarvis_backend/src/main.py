from fastapi import FastAPI
from .db import lifespan
from .api import foods

app = FastAPI(lifespan=lifespan)

# routers
app.include_router(foods.router)
app.include_router(foods.settings_router)
app.include_router(foods.daily_router)
