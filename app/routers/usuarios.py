from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models import User
from app.auth import get_password_hash
from app.database import SessionLocal

router = APIRouter(prefix="/usuarios")
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def listar_usuarios(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("gestion_usuarios.html", {"request": request, "users": users})

@router.post("/crear")
def crear_usuario(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        return RedirectResponse(url="/usuarios", status_code=303)
    hashed_password = get_password_hash(password)
    nuevo = User(username=username, hashed_password=hashed_password)
    db.add(nuevo)
    db.commit()
    return RedirectResponse(url="/usuarios", status_code=303)

@router.post("/eliminar/{user_id}")
def eliminar_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.id == user_id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
    return RedirectResponse(url="/usuarios", status_code=303)