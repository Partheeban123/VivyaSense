# Deployment Guide 🚀

Complete guide for deploying AI Vision Platform to production.

## Prerequisites

- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt recommended)
- Server with:
  - 4+ CPU cores
  - 16GB+ RAM
  - 100GB+ storage
  - GPU (optional, for better performance)

## Deployment Options

### Option 1: Docker Compose (Recommended for Single Server)

#### 1. Prepare Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y

# Add user to docker group
sudo usermod -aG docker $USER
```

#### 2. Clone and Configure

```bash
# Clone repository
git clone <your-repo>
cd ai-vision-platform

# Copy your models
scp your-models/*.pt user@server:/path/to/ai-vision-platform/backend/models/

# Configure environment
cp backend/.env.example backend/.env
nano backend/.env  # Edit with production values
```

#### 3. Production Environment Variables

```env
# backend/.env
APP_NAME="AI Vision Platform"
ENVIRONMENT=production
DEBUG=False

# Database (use strong passwords!)
DATABASE_URL=postgresql://ai_vision_user:STRONG_PASSWORD@postgres:5432/ai_vision_db

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=STRONG_REDIS_PASSWORD

# Security (generate strong secret key)
SECRET_KEY=your-very-long-random-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (add your domain)
CORS_ORIGINS=["https://yourdomain.com", "https://www.yourdomain.com"]

# Models
PPE_MODEL_PATH=./models/ppe_detection.pt
FALL_MODEL_PATH=./models/fall_detection.pt
FIRE_MODEL_PATH=./models/fire_smoke_detection.pt
CONFIDENCE_THRESHOLD=0.5

# Email alerts
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

#### 4. Deploy

```bash
# Build and start services
docker-compose up -d

# Check logs
docker-compose logs -f

# Check status
docker-compose ps
```

#### 5. Setup SSL with Nginx

Create `docker/nginx/nginx.conf`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # Frontend
    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # WebSocket
    location /ws {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Option 2: Cloud Deployment (AWS)

#### AWS Architecture

1. **EC2** - Application servers
2. **RDS** - PostgreSQL database
3. **ElastiCache** - Redis cache
4. **S3** - File storage
5. **CloudFront** - CDN
6. **ALB** - Load balancer

#### Deploy to AWS

```bash
# 1. Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier ai-vision-db \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --master-username admin \
  --master-user-password YOUR_PASSWORD

# 2. Create ElastiCache Redis
aws elasticache create-cache-cluster \
  --cache-cluster-id ai-vision-redis \
  --cache-node-type cache.t3.micro \
  --engine redis

# 3. Create S3 bucket
aws s3 mb s3://ai-vision-storage

# 4. Launch EC2 instance
# Use Ubuntu 22.04 LTS, t3.xlarge or better
# Install Docker and deploy using docker-compose
```

### Option 3: Kubernetes (For Scale)

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-vision-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-vision-backend
  template:
    metadata:
      labels:
        app: ai-vision-backend
    spec:
      containers:
      - name: backend
        image: your-registry/ai-vision-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: ai-vision-secrets
              key: database-url
```

## Post-Deployment

### 1. Database Migration

```bash
# Run migrations
docker-compose exec backend python -c "from database.database import init_db; init_db()"
```

### 2. Create Admin User

```bash
# Access backend container
docker-compose exec backend python

# In Python shell
from database.database import SessionLocal
from database.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])
db = SessionLocal()

admin = User(
    email="admin@yourdomain.com",
    username="admin",
    hashed_password=pwd_context.hash("your-secure-password"),
    full_name="Admin User",
    is_superuser=True
)
db.add(admin)
db.commit()
```

### 3. Setup Monitoring

```bash
# Install monitoring tools
docker-compose -f docker-compose.monitoring.yml up -d

# Access Grafana at http://your-server:3001
```

### 4. Backup Strategy

```bash
# Database backup script
#!/bin/bash
docker-compose exec -T postgres pg_dump -U ai_vision_user ai_vision_db > backup_$(date +%Y%m%d).sql

# Upload to S3
aws s3 cp backup_$(date +%Y%m%d).sql s3://your-backup-bucket/
```

## Security Checklist

- [ ] Change all default passwords
- [ ] Enable SSL/TLS
- [ ] Configure firewall (UFW/Security Groups)
- [ ] Set up fail2ban
- [ ] Enable database encryption
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Enable logging and monitoring
- [ ] Regular security updates
- [ ] Backup strategy in place

## Performance Optimization

### 1. GPU Support

Add to `docker-compose.yml`:

```yaml
backend:
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
```

### 2. Redis Caching

Enable caching for detection results:

```python
# In detection_service.py
import redis
r = redis.Redis(host='redis', port=6379)

# Cache detection results
cache_key = f"detection:{image_hash}"
if r.exists(cache_key):
    return json.loads(r.get(cache_key))
```

### 3. Load Balancing

Use Nginx for load balancing multiple backend instances.

## Monitoring

### Health Checks

```bash
# Backend health
curl https://yourdomain.com/health

# Database connection
docker-compose exec backend python -c "from database.database import engine; engine.connect()"
```

### Logs

```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f backend

# Export logs
docker-compose logs > logs_$(date +%Y%m%d).txt
```

## Troubleshooting

### Issue: Models not loading

```bash
# Check model files
docker-compose exec backend ls -lh models/

# Check permissions
docker-compose exec backend chmod 644 models/*.pt
```

### Issue: Database connection failed

```bash
# Check database status
docker-compose ps postgres

# Check connection
docker-compose exec backend python -c "from database.database import engine; print(engine.url)"
```

### Issue: High memory usage

```bash
# Check resource usage
docker stats

# Limit resources in docker-compose.yml
services:
  backend:
    mem_limit: 4g
    cpus: 2
```

## Maintenance

### Updates

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Scaling

```bash
# Scale backend instances
docker-compose up -d --scale backend=3
```

---

**Need Help?** Check the main README.md or open an issue on GitHub.

