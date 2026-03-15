# AIOPS ISP LITE

FastAPI-based AIOPS agent for ISP automation (provisioning, monitoring, orchestration).

## Local development

`ash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
`

## Deployment to Production

### Single Docker container

`ash
# Build image
docker build -t aiops-isp-lite:latest .

# Run with environment file
docker run -d \
  --name aiops-isp-lite \
  -p 8000:8000 \
  --env-file .env \
  aiops-isp-lite:latest
`

- Health check: GET /health debe devolver { "status": "ok" }.
- Variables de entorno: ver y copiar desde .env.example.

### Using docker-compose (staging/production)

`ash
# Build and start services in background
docker-compose up -d --build

# Ver logs
docker-compose logs -f api
`

Comandos alineados con la skill /deploy-to-prod:

`ash
# Skill /deploy-to-prod (staging)
docker build -t aiops-agent-v2 .
docker-compose up -d
`

Asegúrate de:
- Tener una base de datos PostgreSQL accesible (ver docker-compose.yml).
- Configurar correctamente DATABASE_URL y credenciales.
- Ejecutar tests (pytest -q) y uff check . antes de desplegar.
