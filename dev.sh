#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "🚀 Démarrage dev depuis: $ROOT_DIR"

# --- MySQL
echo "🐬 Lancement MySQL (Docker)..."
cd "$ROOT_DIR"
docker compose up -d

# --- API
echo "⚡ Lancement API FastAPI..."
cd "$ROOT_DIR/services/api"

if [ ! -d ".venv" ]; then
  echo "❌ .venv introuvable dans services/api"
  exit 1
fi

source .venv/Scripts/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000 &
API_PID=$!

# --- Web (PHP)
echo "🌐 Lancement site PHP..."

# Mets ici le BON chemin quand tu l’as trouvé avec find
WEB_DIR="$ROOT_DIR/apps/web"

if [ ! -d "$WEB_DIR" ]; then
  echo "❌ Dossier web introuvable: $WEB_DIR"
  echo "➡️ Trouve-le avec: find . -maxdepth 4 -name index.php"
  kill $API_PID 2>/dev/null || true
  exit 1
fi

cd "$WEB_DIR"
php -S 127.0.0.1:8080 &
PHP_PID=$!

echo ""
echo "✅ Tout est lancé"
echo "➡️ API : http://127.0.0.1:8000/docs"
echo "➡️ Site : http://127.0.0.1:8080"
echo "🛑 CTRL+C pour arrêter"
echo ""

trap 'kill $API_PID $PHP_PID 2>/dev/null || true' INT TERM
wait
