from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models import Cliente
from app.database import SessionLocal

router = APIRouter(prefix="/clientes")
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def listar_clientes(request: Request, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_active_user)):
    clientes = db.query(Cliente).all()
    return templates.TemplateResponse("gestion_clientes.html", {"request": request, "clientes": clientes})

@router.post("/crear")
def crear_cliente(
    current_user: Usuario = Depends(get_current_active_user),nombre: str = Form(...), direccion: str = Form(...), db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_active_user)):
    cliente = Cliente(nombre=nombre, direccion=direccion)
    db.add(cliente)
    db.commit()
    return RedirectResponse(url="/clientes", status_code=303)

@router.post("/eliminar/{cliente_id}")
def eliminar_cliente(
    current_user: Usuario = Depends(get_current_active_user),cliente_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_active_user)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente:
        db.delete(cliente)
        db.commit()
    return RedirectResponse(url="/clientes", status_code=303)