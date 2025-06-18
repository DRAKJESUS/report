from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from reportes import router as reportes_router

app = FastAPI()

# ✅ Middleware de CORS para permitir peticiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier dominio, puedes restringir en producción
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# ✅ Incluir el router de reportes
app.include_router(reportes_router)

@app.get("/")
async def root():
    return {"status": "API online"}
