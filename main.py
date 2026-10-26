import socket

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

DEVELOPER = "Dev1"  # Remplacer par votre nom ou rôle

# Stock de données en mémoire (simulant une base de données)
items = {1: {"name": "item1"}, 2: {"name": "item2"}}


class ItemUpdate(BaseModel):
  name: str


def get_ip() -> str:
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
  except OSError:
    return "unknown"
  finally:
    s.close()


# --- Logique de suppression similaire à apply_update ---
def apply_delete(id: int) -> dict:
  if id not in items:
    raise HTTPException(status_code=404, detail="Item introuvable")
  deleted_item = items.pop(id)
  return {
      "message": f"Item {id} deleted successfully",
      "deleted": deleted_item,
      "developer": DEVELOPER,
  }


@app.get("/")
def read_root():
  return {"message": "it works !"}


@app.get("/items")
def list_items():
  return items


# --- Routes pour PUT (Mise à jour) ---
@app.put("/update/{id}")
def update_item(id: int, item: ItemUpdate):
  if id not in items:
    raise HTTPException(status_code=404, detail="Item introuvable")
  items[id]["name"] = item.name
  return {"id": id, "item": items[id]}


@app.get("/update/{id}")
def update_item_get(id: int, name: str):
  if id not in items:
    raise HTTPException(status_code=404, detail="Item introuvable")
  items[id]["name"] = name
  return {"id": id, "item": items[id]}


# --- Routes pour DELETE (Suppression) ---
@app.delete("/remove/{id}")
def delete_item(id: int):
  return apply_delete(id)


@app.get("/remove/{id}")
def delete_item_get(id: int):
  return apply_delete(id)