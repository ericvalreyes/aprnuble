from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models import Cliente, Lectura
from app.database import SessionLocal
from datetime import datetime
from app.utils import email

router = APIRouter(prefix="/lecturas")
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def listar_lecturas(request: Request, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_active_user)):
    lecturas = db.query(Lectura).all()
    clientes = db.query(Cliente).all()
    return templates.TemplateResponse("gestion_lecturas.html", {"request": request, "lecturas": lecturas, "clientes": clientes})

@router.post("/crear")
def crear_lectura(cliente_id: int = Form(...), fecha: str = Form(...), consumo: float = Form(...), db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_active_user)):
    lectura = Lectura(cliente_id=cliente_id, fecha=datetime.strptime(fecha, "%Y-%m-%d").date(), consumo=consumo)
    db.add(lectura)
    db.commit()
    if consumo > 45:
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        email.enviar_alerta_consumo(cliente.nombre, fecha, consumo)
    return RedirectResponse(url="/lecturas", status_code=303)

@router.post("/eliminar/{lectura_id}")
def eliminar_lectura(
    current_user: Usuario = Depends(get_current_active_user),lectura_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_active_user)):
    lectura = db.query(Lectura).filter(Lectura.id == lectura_id).first()
    if lectura:
        db.delete(lectura)
        db.commit()
    if consumo > 45:
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        email.enviar_alerta_consumo(cliente.nombre, fecha, consumo)
    return RedirectResponse(url="/lecturas", status_code=303)
@router.get("/exportar")
def exportar_excel(cliente_id: int, db: Session = Depends(get_db)):
    from fastapi.responses import FileResponse
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    lecturas = db.query(Lectura).filter(Lectura.cliente_id == cliente_id).all()
    wb = Workbook()
    ws = wb.active
    ws.append(["Cliente", "Fecha", "Consumo (m³)"])
    for lectura in lecturas:
        ws.append([cliente.nombre, lectura.fecha.strftime("%Y-%m-%d"), lectura.consumo])
    file_path = f"app/static/export_{cliente_id}.xlsx"
    wb.save(file_path)
    return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename="lecturas.xlsx")

@router.get("/backup")
def backup_data(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_active_user)):
    from fastapi.responses import FileResponse
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores pueden generar respaldos")

    data = {
        "usuarios": [],
        "clientes": [],
        "lecturas": []
    }

    for u in db.query(Usuario).all():
        data["usuarios"].append({"id": u.id, "username": u.username, "rol": u.rol})

    for c in db.query(Cliente).all():
        data["clientes"].append({"id": c.id, "nombre": c.nombre, "direccion": c.direccion})

    for l in db.query(Lectura).all():
        data["lecturas"].append({
            "id": l.id,
            "cliente_id": l.cliente_id,
            "fecha": l.fecha.isoformat(),
            "consumo": l.consumo
        })

    import json
    file_path = "app/static/backup.json"
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    return FileResponse(file_path, media_type='application/json', filename="backup.json")
