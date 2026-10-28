"""
MLOps - Clase 2: Aplicaciones Web con FastAPI
Incluye todas las rutas vistas en la presentación "2. Aplicaciones Web - 2026"
y la tarea (endpoint de chistes usando la Official Joke API).

Levantar en modo desarrollo:   fastapi dev main.py
Levantar en modo "producción":  fastapi run main.py --port 8000
Documentación automática:       http://localhost:8000/docs
"""
from typing import Optional

import numpy as np
import requests
from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel

app = FastAPI(
    title="MLOps - Clase 2",
    description="Rutas de la clase de Aplicaciones Web + tarea de chistes.",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# 1. Hello world
# ---------------------------------------------------------------------------
@app.get("/", tags=["clase"])
def root():
    return {"message": "Hello World"}


# ---------------------------------------------------------------------------
# 2. Parámetros de ruta (path params)
# ---------------------------------------------------------------------------
@app.get("/items/{item_id}", tags=["clase"])
def item(item_id: int):
    return {"item_id": item_id}


# ---------------------------------------------------------------------------
# 3. Query params (min es query param, max es path param)
#    Ej: /rand/50?min=10
# ---------------------------------------------------------------------------
@app.get("/rand/{max}", tags=["clase"])
def rand(min: int = 0, max: int = 10):
    if min >= max:
        raise HTTPException(status_code=400, detail="min debe ser menor que max")
    return f"Random number: {np.random.randint(min + 1, max + 1)}"


# ---------------------------------------------------------------------------
# 4. Request body con Pydantic
# ---------------------------------------------------------------------------
class Item(BaseModel):
    name: str
    price: float


@app.post("/create", tags=["clase"])
def create_item(item: Item):
    return f"New item created with name {item.name} and price {item.price}."


# ---------------------------------------------------------------------------
# 5. Sirviendo un "modelo"
# ---------------------------------------------------------------------------
def model(x: float) -> float:
    return 3 * x + 1


class Features(BaseModel):
    x: float


@app.post("/predict", tags=["clase"])
def predict(features: Features):
    y = model(features.x)
    return {"prediction": y}


# ---------------------------------------------------------------------------
# 6. Manejo de errores y status codes
#    (la diapositiva usa 201 como ejemplo de status_code personalizado)
# ---------------------------------------------------------------------------
items = {1: "Item nro 1", 3: "Item nro 3"}


@app.get("/item/{item_id}", status_code=status.HTTP_201_CREATED, tags=["clase"])
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


# ---------------------------------------------------------------------------
# 7. TAREA: chistes aleatorios con la Official Joke API
#    Path param  -> cantidad (int)
#    Query param -> categoria (opcional): general, programming, knock-knock, dad
#    Ej: /jokes/3   /jokes/5?categoria=programming
# ---------------------------------------------------------------------------
JOKE_API = "https://official-joke-api.appspot.com"
TIMEOUT = 10


def _get(url: str):
    try:
        r = requests.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error consultando la Joke API: {e}")


@app.get("/jokes/{cantidad}", tags=["tarea"])
def jokes(
    cantidad: int = Path(..., ge=1, le=100, description="Cantidad de chistes (1 a 100)"),
    categoria: Optional[str] = Query(None, description="Categoría del chiste, ej: programming"),
):
    if categoria is None:
        data = _get(f"{JOKE_API}/jokes/random/{cantidad}")
        return {"cantidad": len(data), "categoria": None, "chistes": data}

    tipos = _get(f"{JOKE_API}/types")
    if categoria not in tipos:
        raise HTTPException(
            status_code=404,
            detail=f"Categoría '{categoria}' inexistente. Opciones: {tipos}",
        )

    # La API solo devuelve de a 10 por categoría: pedimos tandas hasta juntar
    # la cantidad pedida sin repetir (o hasta que no aparezcan chistes nuevos).
    juntados = {}
    intentos_sin_nuevos = 0
    while len(juntados) < cantidad and intentos_sin_nuevos < 3:
        antes = len(juntados)
        for joke in _get(f"{JOKE_API}/jokes/{categoria}/ten"):
            juntados[joke["id"]] = joke
        intentos_sin_nuevos = intentos_sin_nuevos + 1 if len(juntados) == antes else 0

    chistes = list(juntados.values())[:cantidad]
    respuesta = {"cantidad": len(chistes), "categoria": categoria, "chistes": chistes}
    if len(chistes) < cantidad:
        respuesta["aviso"] = f"Solo hay {len(chistes)} chistes distintos de '{categoria}'."
    return respuesta
