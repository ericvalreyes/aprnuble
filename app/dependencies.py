from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError

SECRET_KEY = "secret"
ALGORITHM = "HS256"

def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="No autenticado")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido")