from fastapi import FastAPI
from reportes import router as reportes_router

app = FastAPI()
app.include_router(reportes_router)

@app.get("/")
async def root():
    return {"status": "API online"}