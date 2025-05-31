from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
def get_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.get("/clientes", response_class=HTMLResponse)
def get_clientes(request: Request):
    return templates.TemplateResponse("clientes.html", {"request": request})

@router.get("/lecturas", response_class=HTMLResponse)
def get_lecturas(request: Request):
    return templates.TemplateResponse("lecturas.html", {"request": request})

@router.get("/usuarios", response_class=HTMLResponse)
def get_usuarios(request: Request):
    return templates.TemplateResponse("usuarios.html", {"request": request})

@router.get("/graficos", response_class=HTMLResponse)
def get_graficos(request: Request):
    return templates.TemplateResponse("graficos.html", {"request": request})
