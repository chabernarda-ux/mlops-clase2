#!/bin/bash
# Instala y deja funcionando el proyecto de la Clase 2 (venv + FastAPI + Git).
# Uso:  cd ~/MLOPs/clase2_fastapi && bash setup_mac.sh
set -e
cd "$(dirname "$0")"

echo "==> 1/5 Verificando Git"
if ! command -v git >/dev/null 2>&1; then
  echo "Git no está instalado. Se abre el instalador de herramientas de Apple:"
  xcode-select --install || true
  echo "Cuando termine la instalación, volvé a correr: bash setup_mac.sh"; exit 1
fi
git --version
if [ -z "$(git config --global user.name)" ]; then
  read -p "Tu nombre para los commits: " NOMBRE; git config --global user.name "$NOMBRE"
fi
if [ -z "$(git config --global user.email)" ]; then
  read -p "Tu email para los commits (el mismo de GitHub): " MAIL; git config --global user.email "$MAIL"
fi

echo "==> 2/5 Creando entorno virtual .venv (python -m venv)"
python3 -m venv .venv
source .venv/bin/activate

echo "==> 3/5 Instalando dependencias (pip install -r requirements.txt)"
pip install --upgrade pip -q
pip install -r requirements.txt -q
python -c "import fastapi; print('FastAPI', fastapi.__version__)"

echo "==> 4/5 Corriendo tests"
pytest -q

echo "==> 5/5 Inicializando repo Git y primer commit"
if [ ! -d .git ]; then git init -b main; fi
git add .gitignore README.md requirements.txt main.py probar_api.py test_main.py setup_mac.sh
git commit -m "Clase 2: FastAPI con rutas de la clase y endpoint de chistes" || echo "(nada nuevo para commitear)"
git status

echo
echo "Listo. Para levantar la API:"
echo "  source .venv/bin/activate && fastapi dev main.py"
echo "Y abrí http://localhost:8000/docs"
