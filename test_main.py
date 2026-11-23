import pytest
from fastapi.testclient import TestClient

import main
from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_items():
    """Remet les données en mémoire à leur état initial avant chaque test."""
    main.items.clear()
    main.items.update({1: {"name": "item1"}, 2: {"name": "item2"}})


# ---------- racine ----------
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "it works !"}


# ---------- addition / soustraction ----------
def test_addition():
    response = client.get("/addition?a=2&b=3")
    assert response.status_code == 200
    assert response.json() == {"result a+b": 5, "developer": "Dev1"}


def test_soustraction():
    response = client.get("/soustraction?a=5&b=3")
    assert response.status_code == 200
    assert response.json() == {"resultat": 2}


# ---------- greeting ----------
def test_greeting():
    response = client.get("/greeting?name=Aya")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello, Aya"
    assert data["developer"] == "Dev2"
    assert "hostname" in data
    assert "IP" in data


# ---------- get_ip (succès et erreur réseau) ----------
class FakeSocket:
    def __init__(self, *args, **kwargs):
        pass

    def connect(self, address):
        pass

    def getsockname(self):
        return ("192.168.1.10", 12345)

    def close(self):
        pass


class FailingSocket(FakeSocket):
    def connect(self, address):
        raise OSError("réseau indisponible")


def test_get_ip_success(monkeypatch):
    monkeypatch.setattr(main.socket, "socket", FakeSocket)
    assert main.get_ip() == "192.168.1.10"


def test_get_ip_error(monkeypatch):
    monkeypatch.setattr(main.socket, "socket", FailingSocket)
    assert main.get_ip() == "unknown"


# ---------- multiply ----------
def test_multiply_get():
    response = client.get("/multiply?a=2&b=3")
    assert response.status_code == 200
    assert response.json() == {"result a*b": 6, "developer": "Dev1"}


def test_multiply_post():
    response = client.post("/multiply", json={"a": 4, "b": 5})
    assert response.status_code == 200
    assert response.json() == {"result a*b": 20, "developer": "Dev1"}


# ---------- divide ----------
def test_divide_get():
    response = client.get("/divide?a=10&b=2")
    assert response.status_code == 200
    assert response.json() == {"result a/b": 5, "developer": "Dev2"}


def test_divide_post():
    response = client.post("/divide", json={"a": 9, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result a/b": 3, "developer": "Dev2"}


def test_divide_by_zero_get():
    response = client.get("/divide?a=1&b=0")
    assert response.status_code == 400
    assert response.json() == {"detail": "Division par zéro impossible"}


def test_divide_by_zero_post():
    response = client.post("/divide", json={"a": 1, "b": 0})
    assert response.status_code == 400


# ---------- items / update ----------
def test_list_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == {"1": {"name": "item1"}, "2": {"name": "item2"}}


def test_update_put():
    response = client.put("/update/1", json={"name": "nouveau"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "item": {"name": "nouveau"}}
    assert main.items[1]["name"] == "nouveau"


def test_update_get():
    response = client.get("/update/2?name=autre")
    assert response.status_code == 200
    assert response.json() == {"id": 2, "item": {"name": "autre"}}


def test_update_put_not_found():
    response = client.put("/update/99", json={"name": "x"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item introuvable"}


def test_update_get_not_found():
    response = client.get("/update/99?name=x")
    assert response.status_code == 404


# ---------- remove ----------
EXPECTED_DELETE = {"message": "Item 1 deleted successfully", "developer": "Dev2"}


def test_remove_get():
    response = client.get("/remove/1")
    assert response.status_code == 200
    assert response.json() == EXPECTED_DELETE


def test_remove_post():
    response = client.post("/remove/1")
    assert response.status_code == 200
    assert response.json() == EXPECTED_DELETE


def test_remove_delete():
    response = client.delete("/remove/1")
    assert response.status_code == 200
    assert response.json() == EXPECTED_DELETE