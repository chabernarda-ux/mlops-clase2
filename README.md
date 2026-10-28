# MLOps – Clase 2: FastAPI + Git

Proyecto que implementa todo lo de la presentación **"2. Aplicaciones Web - 2026"** (rutas de FastAPI y la tarea) versionado con **Git** según **"1.bis.1 GIT"**, dentro de un entorno virtual según **"1.4 VirtualEnvs"**.

## Instalación rápida (Mac)

```bash
cd ~/MLOPs/clase2_fastapi
bash setup_mac.sh
```

El script: verifica Git (y configura nombre/email si falta), crea `.venv`, instala `requirements.txt`, corre los tests, hace `git init` y el primer commit.

## Levantar la API

```bash
source .venv/bin/activate
fastapi dev main.py              # desarrollo, con recarga automática
# fastapi run main.py --port 8000  # "producción"
```

- Navegador: http://localhost:8000 y la documentación automática en http://localhost:8000/docs
- Script con requests (en otra terminal, con el venv activado): `python probar_api.py`
- Tests: `pytest -q`

## Rutas

| Método | Ruta | Qué muestra de la clase |
|---|---|---|
| GET | `/` | Hello world |
| GET | `/items/{item_id}` | Path param tipado (validación automática) |
| GET | `/rand/{max}?min=0` | Query params |
| POST | `/create` | Request body con Pydantic (`name`, `price`) |
| POST | `/predict` | Sirviendo un modelo (`y = 3x + 1`) |
| GET | `/item/{item_id}` | Status codes y `HTTPException` (404) |
| GET | `/jokes/{cantidad}?categoria=` | **Tarea**: chistes de la Official Joke API |

Categorías válidas de chistes: `general`, `programming`, `knock-knock`, `dad`.

## Subir a GitHub (git push)

1. Creá un repo vacío en GitHub (sin README) llamado `mlops-clase2`.
2. Autenticación con clave pública (como pide la clase de SSH):
   ```bash
   ssh-keygen -t ed25519 -C "tu_email"
   cat ~/.ssh/id_ed25519.pub   # copiala en GitHub > Settings > SSH and GPG keys
   ssh -T git@github.com       # debería saludarte con tu usuario
   ```
3. Conectá y subí:
   ```bash
   git remote add origin git@github.com:TU_USUARIO/mlops-clase2.git
   git push -u origin main
   ```

## Ciclo de Git de la clase

`git status` → `git add archivo` → `git commit -m "mensaje"` → `git push` · traer cambios de colegas: `git pull` · repo existente: `git clone URL`
