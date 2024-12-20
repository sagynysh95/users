from fastapi import FastAPI
from routes import router
from mongo_file import setup_mongo

app = FastAPI()

setup_mongo()
app.include_router(router=router)