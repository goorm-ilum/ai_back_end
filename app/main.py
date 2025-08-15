from fastapi import FastAPI
from routes.products import router

app = FastAPI()
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "AI SQL Agent API"}
