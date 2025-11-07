# Architecture Overview

## System Design

### High-Level Architecture
```
External APIs          Application Layer         Data Layer          Monitoring
─────────────          ──────────────────        ──────────          ──────────

placekitten.com ─┐
place.dog ───────┼───▶ FastAPI ────────────────▶ PostgreSQL ◀──── Prometheus
placebear.com ───┘         │                                            │
                           │                                            │
                           └──────────────────────────────────────────▶ Grafana
```

### Components

#### 1. Application (FastAPI)
- **Port**: 8000
- **Responsibilities**:
  - REST API endpoints
  - Request validation (Pydantic)
  - Business logic orchestration
  - Prometheus metrics exposition
  
#### 2. Database (PostgreSQL)
- **Port**: 5432
- **Schema**:
```sql
  CREATE TABLE animal_pictures (
      id SERIAL PRIMARY KEY,
      animal_type VARCHAR(50),
      image_data BYTEA,
      image_url VARCHAR(500),
      width INTEGER,
      height INTEGER,
      created_at TIMESTAMP DEFAULT NOW()
  );
```

#### 3. Monitoring (Prometheus + Grafana)
- **Prometheus Port**: 9090
- **Grafana Port**: 3000
- Scrapes `/metrics` endpoint every 15 seconds

### Data Flow

1. **Fetch Animal Picture**:
```
   Client → POST /api/animal → Service Layer → External API
                                      ↓
                              Store in Database
                                      ↓
                              Return Metadata
```

2. **Retrieve Latest Picture**:
```
   Client → GET /api/animal/latest → Query Database
                                           ↓
                                    Return Image Data
```

### Design Decisions

#### Why FastAPI?
- Automatic API documentation (OpenAPI/Swagger)
- Built-in data validation (Pydantic)
- High performance (ASGI)
- Native async support

#### Why PostgreSQL?
- ACID compliance
- Binary data support (BYTEA)
- Production-ready
- Wide adoption

#### Why Docker Compose?
- Single command deployment
- No local dependencies required
- Consistent across environments
- Built-in networking

### Scalability Considerations

For production deployment:

1. **Application Layer**:
   - Deploy multiple app containers behind load balancer
   - Use Kubernetes for orchestration
   - Implement rate limiting

2. **Database Layer**:
   - Use managed PostgreSQL (RDS, Cloud SQL)
   - Implement connection pooling
   - Add read replicas for scaling reads

3. **Storage**:
   - Move images to object storage (S3, GCS)
   - Store only URLs in database
   - Implement CDN for image delivery

4. **Monitoring**:
   - Add application logging (ELK stack)
   - Implement distributed tracing (Jaeger)
   - Set up alerting rules

### Security Considerations

Current implementation is for development. Production would need:

- HTTPS/TLS encryption
- Authentication/Authorization
- Input sanitization
- Rate limiting
- Database credentials in secrets manager
- Network policies

### Testing Strategy

1. **Unit Tests**: Service layer logic
2. **Integration Tests**: API endpoints with test database
3. **Contract Tests**: External API mocking

### Performance Characteristics

- **Image Fetch**: ~500ms (network dependent)
- **Database Write**: ~10ms
- **Latest Image Retrieval**: ~5ms
- **Health Check**: ~2ms

### Deployment Options

1. **Local Development**: Docker Compose (current)
2. **Cloud VM**: Docker Compose on EC2/Compute Engine
3. **Kubernetes**: Helm chart deployment
4. **Serverless**: AWS Lambda + API Gateway + RDS

