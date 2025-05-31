#!/bin/bash
# Activar entorno virtual y correr la aplicación con Uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 10000