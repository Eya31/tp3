"""API FastAPI du TP3 : opérations arithmétiques et gestion d'items."""
import socket

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

DEVELOPER = "Dev2"  # remplacez par votre nom

# Stock de données en mémoire (utilisé par PUT /update/{item_id})
items = {1: {"name": "item1"}, 2: {"name": "item2"}}


class Operands(BaseModel):
    """Deux opérandes pour les opérations arithmétiques."""

    a: float
    b: float


class ItemUpdate(BaseModel):
    """Corps de la requête de mise à jour d'un item."""

    name: str


def get_ip() -> str:
    """IP de l'interface réseau utilisée pour sortir sur internet."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))  # aucun paquet n'est envoyé
        return sock.getsockname()[0]
    except OSError:
        return "unknown"
    finally:
        sock.close()


def compute_multiply(a: float, b: float) -> dict:
    """Retourne le produit de a et b."""
    return {"result a*b": a * b, "developer": "Dev1"}


def compute_divide(a: float, b: float) -> dict:
    """Retourne le quotient de a par b (erreur 400 si b vaut 0)."""
    if b == 0:
        raise HTTPException(status_code=400, detail="Division par zéro impossible")
    return {"result a/b": a / b, "developer": "Dev2"}


def compute_delete(item_id: int) -> dict:
    """Retourne le message de suppression de l'item."""
    return {
        "message": f"Item {item_id} deleted successfully",
        "developer": DEVELOPER,
    }


def apply_update(item_id: int, name: str) -> dict:
    """Met à jour le nom d'un item (erreur 404 s'il n'existe pas)."""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item introuvable")
    items[item_id]["name"] = name
    return {"id": item_id, "item": items[item_id]}


@app.get("/")
def read_root():
    """Page d'accueil."""
    return {"message": "it works !"}


@app.get("/addition")
def addition(a: int, b: int):
    """Additionne a et b."""
    return {"result a+b": a + b, "developer": "Dev1"}


@app.get("/soustraction")
def soustraction(a: int, b: int):
    """Soustrait b de a."""
    return {"resultat": a - b}


@app.get("/greeting")
def greeting(name: str):
    """Salue l'utilisateur et retourne des infos sur la machine."""
    return {
        "message": f"Hello, {name}",
        "developer": DEVELOPER,
        "hostname": socket.gethostname(),
        "IP": get_ip(),
    }


@app.get("/multiply")
def multiply_get(a: float, b: float):
    """Multiplication via GET."""
    return compute_multiply(a, b)


@app.post("/multiply")
def multiply_post(op: Operands):
    """Multiplication via POST."""
    return compute_multiply(op.a, op.b)


@app.get("/divide")
def divide_get(a: float, b: float):
    """Division via GET."""
    return compute_divide(a, b)


@app.post("/divide")
def divide_post(op: Operands):
    """Division via POST."""
    return compute_divide(op.a, op.b)


@app.get("/items")
def list_items():
    """Liste tous les items."""
    return items


@app.put("/update/{item_id}")
def update_item(item_id: int, item: ItemUpdate):
    """Met à jour un item via PUT."""
    return apply_update(item_id, item.name)


@app.get("/update/{item_id}")
def update_item_get(item_id: int, name: str):
    """Met à jour un item via GET."""
    return apply_update(item_id, name)


@app.get("/remove/{item_id}")
def delete_get(item_id: int):
    """Suppression via GET."""
    return compute_delete(item_id)


@app.post("/remove/{item_id}")
def delete_post(item_id: int):
    """Suppression via POST."""
    return compute_delete(item_id)


@app.delete("/remove/{item_id}")
def delete_item(item_id: int):
    """Suppression via DELETE."""
    return compute_delete(item_id)
