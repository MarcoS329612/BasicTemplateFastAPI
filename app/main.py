from fastapi import FastAPI
from config.db import create_db_and_tables
from routers.customer import customer

app = FastAPI(lifespan=create_db_and_tables)
app.include_router(customer)


@app.get("/")
async def root():
    return {"message": "Hello World"}