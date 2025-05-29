from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

app = FastAPI(title="Security Service")
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "CAMBIA_ESTA_SECRETO"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Usuario de ejemplo
fake_db = {
    "alice": {
        "username": "alice",
        "hashed_pw": pwd_ctx.hash("secret123"),
        "roles": ["student"]
    }
}

def verify_pw(plain, hashed):
    return pwd_ctx.verify(plain, hashed)

def authenticate(u, p):
    user = fake_db.get(u)
    if not user or not verify_pw(p, user["hashed_pw"]):
        return None
    return user

def create_token(data: dict, exp_minutes=30):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=exp_minutes)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/auth/token")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate(form.username, form.password)
    if not user:
        raise HTTPException(400, "Usuario o contraseña incorrectos")
    token = create_token({"sub": user["username"], "roles": user["roles"]})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/auth/verify")
def verify(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"user": payload["sub"], "roles": payload["roles"]}
    except jwt.PyJWTError:
        raise HTTPException(401, "Token inválido")
