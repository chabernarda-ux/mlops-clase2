"""
Prueba todas las rutas de main.py usando requests (parte de la tarea).
Primero levantá el server en otra terminal:  fastapi dev main.py
Después corré:                               python probar_api.py
"""
import json

import requests

BASE = "http://127.0.0.1:8000"


def mostrar(titulo, r):
    print(f"\n=== {titulo} -> {r.request.method} {r.url}")
    print(f"Status: {r.status_code}")
    try:
        print(json.dumps(r.json(), indent=2, ensure_ascii=False))
    except ValueError:
        print(r.text)


mostrar("Hello world", requests.get(f"{BASE}/"))
mostrar("Path param", requests.get(f"{BASE}/items/42"))
mostrar("Path param inválido (422)", requests.get(f"{BASE}/items/hola"))
mostrar("Query params", requests.get(f"{BASE}/rand/100", params={"min": 50}))
mostrar("Request body", requests.post(f"{BASE}/create", json={"name": "Alice", "price": 5}))
mostrar("Modelo", requests.post(f"{BASE}/predict", json={"x": 10}))
mostrar("Item existente (201)", requests.get(f"{BASE}/item/1"))
mostrar("Item inexistente (404)", requests.get(f"{BASE}/item/2"))
mostrar("TAREA: 3 chistes", requests.get(f"{BASE}/jokes/3"))
mostrar("TAREA: 2 chistes de programación",
        requests.get(f"{BASE}/jokes/2", params={"categoria": "programming"}))
mostrar("TAREA: categoría inválida (404)",
        requests.get(f"{BASE}/jokes/1", params={"categoria": "futbol"}))
