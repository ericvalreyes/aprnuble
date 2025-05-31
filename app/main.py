from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import web  # Importamos el router del panel de control

app = FastAPI()

# Montamos los archivos estáticos (si tienes CSS/JS en app/static)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Incluir rutas del panel de control
app.include_router(web.router)
