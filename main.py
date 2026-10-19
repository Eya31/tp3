import socket

from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

class Numbers(BaseModel):
    a: float
    b: float

@app.post("/multiply")
def multiply_numbers(nums: Numbers):
    result = nums.a * nums.b
    return {
        "result a*b=": result,
        "developer": "Dev1"
    }

def get_ip() -> str:
    """IP de l'interface réseau utilisée pour sortir sur internet."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # aucun paquet n'est envoyé
        return s.getsockname()[0]
    except OSError:
        return "unknown"
    finally:
        s.close()


@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/addition")
def addition(a: int, b: int):
    return {"result a+b": a + b, "developer": "Dev1"}
    return {"message": "it works !"}


@app.get("/greeting")
def greeting(name: str):
    return {
        "message": f"Hello, {name}",
        "developer": DEVELOPER,
        "hostname": socket.gethostname(),
        "IP": get_ip(),
    }
