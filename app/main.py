from fastapi import FastAPI
from app.routers import productos

app =  FastAPI(
    title = "API exclusiva de productos",
    version = "1.0",
    descripcion= "API de gestion exclusivamente de productos usando DB oracle"
) 

app.include_router(productos.router)