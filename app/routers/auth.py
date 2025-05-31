from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models import User
from app.database import SessionLocal
from app.auth import verify_password, create_access_token

router = APIRouter(prefix="/auth")
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    access_token = create_access_token({"sub": user.username})
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    return response

@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    from app.auth import get_password_hash
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    hashed_password = get_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/auth/login", status_code=302)