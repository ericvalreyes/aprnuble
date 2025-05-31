import matplotlib.pyplot as plt
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Cliente, Lectura
from uuid import uuid4
import os

router = APIRouter(prefix="/graficos")
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/consumo", response_class=HTMLResponse)
def mostrar_formulario(request: Request, cliente_id: int = None, db: Session = Depends(get_db)):
    clientes = db.query(Cliente).all()
    img_url = None
    if cliente_id:
        lecturas = db.query(Lectura).filter(Lectura.cliente_id == cliente_id).order_by(Lectura.fecha).all()
        fechas = [l.fecha.strftime("%Y-%m-%d") for l in lecturas]
        consumos = [l.consumo for l in lecturas]
        if fechas and consumos:
            nombre_archivo = f"app/static/{uuid4().hex}.png"
            plt.figure()
            plt.plot(fechas, consumos, marker='o')
            plt.title("Consumo de Agua")
            plt.xlabel("Fecha")
            plt.ylabel("Consumo (m³)")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(nombre_archivo)
            plt.close()
            img_url = "/" + nombre_archivo
    return templates.TemplateResponse("grafico_consumo.html", {"request": request, "clientes": clientes, "img_url": img_url})
@router.get("/mensual", response_class=HTMLResponse)
def grafico_mensual(request: Request, cliente_id: int = None, db: Session = Depends(get_db)):
    clientes = db.query(Cliente).all()
    img_url = None
    if cliente_id:
        lecturas = db.query(Lectura).filter(Lectura.cliente_id == cliente_id).all()
        if lecturas:
            from collections import defaultdict
            import calendar
            data = defaultdict(float)
            for lectura in lecturas:
                key = lectura.fecha.strftime("%Y-%m")
                data[key] += lectura.consumo
            sorted_keys = sorted(data.keys())
            labels = [calendar.month_name[int(k.split("-")[1])] for k in sorted_keys]
            values = [data[k] for k in sorted_keys]
            if labels:
                nombre_archivo = f"app/static/{uuid4().hex}.png"
                plt.figure()
                plt.bar(labels, values)
                plt.title("Consumo Mensual")
                plt.xlabel("Mes")
                plt.ylabel("Consumo (m³)")
                plt.tight_layout()
                plt.savefig(nombre_archivo)
                plt.close()
                img_url = "/" + nombre_archivo
    return templates.TemplateResponse("grafico_mensual.html", {"request": request, "clientes": clientes, "img_url": img_url})
