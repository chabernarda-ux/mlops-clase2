"""Tests con el TestClient de FastAPI (mencionado en la clase). Correr con: pytest -q"""
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root():
    assert client.get("/").json() == {"message": "Hello World"}


def test_item_path_param():
    assert client.get("/items/7").json() == {"item_id": 7}
    assert client.get("/items/abc").status_code == 422


def test_rand():
    r = client.get("/rand/20?min=10")
    n = int(r.json().split(": ")[1])
    assert 11 <= n <= 20


def test_create_and_predict():
    assert "Alice" in client.post("/create", json={"name": "Alice", "price": 5}).json()
    assert client.post("/predict", json={"x": 10}).json() == {"prediction": 31}


def test_errores():
    assert client.get("/item/1").status_code == 201
    assert client.get("/item/2").status_code == 404


FAKE = [{"id": i, "type": "programming", "setup": f"s{i}", "punchline": f"p{i}"} for i in range(10)]


def fake_get(url):
    if url.endswith("/types"):
        return ["general", "programming", "knock-knock", "dad"]
    if "/jokes/random/" in url:
        return FAKE[: int(url.rsplit("/", 1)[1])]
    return FAKE


@patch("main._get", side_effect=fake_get)
def test_jokes(_):
    assert client.get("/jokes/3").json()["cantidad"] == 3
    r = client.get("/jokes/2?categoria=programming").json()
    assert r["cantidad"] == 2 and r["categoria"] == "programming"
    assert client.get("/jokes/1?categoria=futbol").status_code == 404
    assert client.get("/jokes/0").status_code == 422
