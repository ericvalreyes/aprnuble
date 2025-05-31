from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import Base, engine
from app.routers import graficos, usuarios, auth, clientes, lecturas
from app.dependencies import get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

app.include_router(graficos.router)
app.include_router(usuarios.router)
app.include_router(graficos.router)
app.include_router(auth.router)
app.include_router(graficos.router)
app.include_router(usuarios.router)
app.include_router(graficos.router)
app.include_router(clientes.router)
app.include_router(graficos.router)
app.include_router(usuarios.router)
app.include_router(graficos.router)
app.include_router(lecturas.router)

@app.get("/", response_class=HTMLResponse)
def index(request: Request, user: str = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})