from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import productos

app =  FastAPI(
    title = "API exclusiva de productos",
    version = "1.0",
    descripcion= "API de gestion exclusivamente de productos usando DB oracle"
) 

# Configuración de CORS
origins = [
    "http://localhost:8000",  # Para Django en desarrollo
    "http://127.0.0.1:8000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(productos.router)