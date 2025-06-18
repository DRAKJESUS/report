from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from reportes import router as reportes_router

app = FastAPI()

# ✅ Middleware de CORS para permitir peticiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Incluir el router de reportes
app.include_router(reportes_router)

@app.get("/")
async def root():
    return {"status": "API online"}
