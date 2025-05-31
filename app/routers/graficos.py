
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import matplotlib.pyplot as plt
import io
import base64

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/graficos", response_class=HTMLResponse)
def mostrar_grafico(request: Request):
    # Datos de ejemplo
    meses = ["Ene", "Feb", "Mar", "Abr", "May"]
    consumo = [20, 30, 25, 35, 40]

    fig, ax = plt.subplots()
    ax.plot(meses, consumo)
    ax.set_title("Consumo de Agua")
    ax.set_ylabel("m³")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()

    return templates.TemplateResponse("grafico.html", {"request": request, "grafico": image_base64})
