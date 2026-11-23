import socket

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

DEVELOPER = "Dev2"  # remplacez par votre nom

# Stock de données en mémoire (utilisé par PUT /update/{id})
items = {1: {"name": "item1"}, 2: {"name": "item2"}}


class Operands(BaseModel):
    a: float
    b: float


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


def compute_multiply(a: float, b: float) -> dict:
    return {"result a*b": a * b, "developer": "Dev1"}


def compute_divide(a: float, b: float) -> dict:
    if b == 0:
        raise HTTPException(status_code=400, detail="Division par zéro impossible")
    return {"result a/b": a / b, "developer": "Dev2"}

def compute_delete(item_id: int) -> dict:
    return {
        "message": f"Item {item_id} deleted successfully",
        "developer": DEVELOPER,
    }


@app.get("/")
def read_root():
    return {"message": "it works !"}


@app.get("/addition")
def addition(a: int, b: int):
    return {"result a+b": a + b, "developer": "Dev1"}


@app.get("/greeting")
def greeting(name: str):
    return {
        "message": f"Hello, {name}",
        "developer": DEVELOPER,
        "hostname": socket.gethostname(),
        "IP": get_ip(),
    }


@app.get("/multiply")
def multiply_get(a: float, b: float):
    return compute_multiply(a, b)


@app.post("/multiply")
def multiply_post(op: Operands):
    return compute_multiply(op.a, op.b)


@app.get("/divide")
def divide_get(a: float, b: float):
    return compute_divide(a, b)


@app.post("/divide")
def divide_post(op: Operands):
    return compute_divide(op.a, op.b)

@app.get("/items")
def list_items():
    return items
class ItemUpdate(BaseModel):
    name: str


def apply_update(id: int, name: str) -> dict:
    if id not in items:
        raise HTTPException(status_code=404, detail="Item introuvable")
    items[id]["name"] = name
    return {"id": id, "item": items[id]}


@app.put("/update/{id}")
def update_item(id: int, item: ItemUpdate):
    return apply_update(id, item.name)


@app.get("/update/{id}")
def update_item_get(id: int, name: str):
    return apply_update(id, name)

@app.get("/remove/{item_id}")
def delete_get(item_id: int):
    return compute_delete(item_id)


@app.post("/remove/{item_id}")
def delete_post(item_id: int):
    return compute_delete(item_id)


@app.delete("/remove/{item_id}")
def delete_item(item_id: int):
    return compute_delete(item_id)
@app.get("/soustraction")
def soustraction(a: int, b: int):
    return {"resultat": a - b}