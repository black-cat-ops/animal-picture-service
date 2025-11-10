# Animal Picture Service
A microservice that fetches and stores random pictures of cats, dogs, and bears with built-in monitoring and observability.

## 🎯 Overview
This service provides REST API endpoints to:
- Fetch random animal pictures from external APIs
- Store pictures in a PostgreSQL database
- Retrieve previously stored pictures
- Monitor application metrics with Prometheus and Grafana

## 📋 Prerequisites
**Required:**
- Docker Desktop installed and running

**That's it!** No need to install Python, PostgreSQL, or any other dependencies.

## 🚀 Quick Start

### 1. Clone or Extract the Repository
```bash
# If using Git
git clone https://github.com/black-cat-ops/animal-picture-service.git
cd */animal-picture-service

# If using ZIP
unzip animal-picture-service.zip
cd */animal-picture-service
```

### 2. Start All Services
```bash
docker-compose up --build
```

**Wait approximately 60 seconds** for all services to start. You'll see logs indicating the services are ready.

### 3. Access the Application
- **Web UI**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (interactive Swagger UI)
- **Grafana**: http://localhost:3000 (username: `admin`, password: `admin`)
- **Prometheus**: http://localhost:9090

## 📊 Monitoring 

### Grafana Dashboards
1. Visit http://localhost:3000
2. Login with `admin` / `admin`
3. Navigate to Dashboards to view metrics

### Prometheus Metrics
Visit http://localhost:9090 and query:
- `app_requests_total` - Total number of requests

## 📡 API Endpoints

### Fetch and Store Animal Picture
```bash
POST /api/animal
Content-Type: application/json

{
  "animal_type": "cat",  # Options: cat, dog, bear
  "width": 400,
  "height": 400
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:8000/api/animal \
  -H "Content-Type: application/json" \
  -d '{"animal_type":"cat","width":400,"height":400}'
```

### Get Latest Picture Metadata
```bash
GET /api/animal/latest
```

**Example:**
```bash
curl http://localhost:8000/api/animal/latest
```

### Get Latest Picture Image
```bash
GET /api/animal/latest/image
```

**Example:**
```bash
curl http://localhost:8000/api/animal/latest/image --output latest.jpg
```

### Health Check
```bash
GET /health
```
**Example Health Check**
[Test in Swagger UI](http://localhost:8000/docs#/default/health_check_health_get)

### Metrics (Prometheus)
```bash
GET /metrics
```
**Example Metric**
[Test in Swagger UI](http://localhost:8000/docs#/default/metrics_metrics_get)


## 🧪 Running Tests
```bash
# Run all tests
docker-compose run app poetry run pytest

# Run with coverage
docker-compose run --rm app poetry run pytest --cov=app tests/

# Run with verbose output
docker-compose run app poetry run pytest -v
```

## 🧹 Cleanup
```bash
# Stop all services
docker-compose down

# Remove all data (volumes)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

## 🏗️ Architecture
```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Client    │─────▶│  FastAPI App │─────▶│ PostgreSQL  │
│  (Browser)  │◀─────│   (Port 8000)│◀─────│ (Port 5432) │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            │ /metrics
                            ▼
                     ┌──────────────┐
                     │  Prometheus  │
                     │  (Port 9090) │
                     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │   Grafana    │
                     │  (Port 3000) │
                     └──────────────┘
```

## 🛠️ Technology Stack
- **Language**: Python 3.11
- **Framework**: FastAPI
- **Database**: PostgreSQL 15
- **Build Tool**: Poetry
- **Containerization**: Docker & Docker Compose
- **Monitoring**: Prometheus + Grafana
- **Testing**: pytest (7 automated tests)

## 📦 Project Structure
```
animal-picture-service/
├── app/
│   ├── main.py           # FastAPI application
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic schemas
│   ├── services.py       # Business logic
│   ├── database.py       # Database setup
│   └── config.py         # Configuration
├── tests/
│   ├── test_api.py       # API tests
│   └── test_services.py  # Service tests
├── ui/
│   └── index.html        # Simple web interface
├── monitoring/
│   └── prometheus.yml    # Prometheus config
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml        # Poetry dependencies
└── README.md
```

## 🐛 Troubleshooting

### Port Already in Use
If you see "port is already allocated" error:
```bash
# Stop any existing containers
docker-compose down

# Or change ports in docker-compose.yml
```

### Database Connection Issues
```bash
# Check if database is healthy
docker-compose ps

# View database logs
docker-compose logs db

# Restart services
docker-compose restart
```

### Grafana Shows No Data
1. Verify Prometheus is working: http://localhost:9090
2. In Prometheus, query: `app_requests_total`. Click "Execute" - you should see metrics data.
3. If not, you can try Generating Test Traffic
```bash
# Generate some requests to see in monitoring
for i in {1..10}; do
  curl -X POST http://localhost:8000/api/animal \
    -H "Content-Type: application/json" \
    -d '{"animal_type":"cat","width":400,"height":400}'
  sleep 1
done
```
4. If you see data in Prometheus but not Grafana:
   - Check that data source is configured correctly
   - Verify URL is `http://prometheus:9090` (not localhost)
   - Click "Save & Test" in data source settings


### Clear All Data and Start Fresh
```bash
# Stop and remove all containers and volumes
docker-compose down -v

# Rebuild and start
docker-compose up --build
```

## 📝 Notes
- The application uses external APIs (cataas.com, place.dog, placebear.com) to fetch images
- Images are stored as binary data in PostgreSQL
- The service includes automatic health checks
- All services restart automatically if they crash

## 🤝 AI Assistance
This project was developed with assistance from Claude (Anthropic) for:
- Boilerplate code generation (~30%)
- Docker configuration
- Test structure setup

All architecture decisions, business logic, and integration were implemented independently.

## 📄 License
This is a technical challenge submission.

