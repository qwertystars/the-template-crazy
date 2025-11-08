# FlexiBase Setup Guide

This guide will walk you through setting up FlexiBase for development and production.

## Table of Contents
1. [Development Setup](#development-setup)
2. [Docker Setup](#docker-setup)
3. [Database Setup](#database-setup)
4. [Environment Configuration](#environment-configuration)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)

## Development Setup

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10 or higher**
- **Node.js 18 or higher**
- **PostgreSQL 15**
- **Git**
- **Docker and Docker Compose** (optional, but recommended)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd the-template-crazy
```

### 2. Backend Setup

#### 2.1 Create Python Virtual Environment

```bash
cd backend
python -m venv venv

# On Linux/macOS
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

#### 2.2 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 2.3 Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and update the following variables:

```env
DATABASE_URL=postgresql+asyncpg://flexibase_user:flexibase_password@localhost:5432/flexibase_db
SECRET_KEY=your-secret-key-here-use-something-secure
DEBUG=True
ENVIRONMENT=development
```

#### 2.4 Set Up Database

Create a PostgreSQL database:

```sql
CREATE DATABASE flexibase_db;
CREATE USER flexibase_user WITH PASSWORD 'flexibase_password';
GRANT ALL PRIVILEGES ON DATABASE flexibase_db TO flexibase_user;
```

Run migrations:

```bash
alembic upgrade head
```

#### 2.5 Start Backend Server

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at http://localhost:8000

### 3. Frontend Setup

#### 3.1 Install Dependencies

```bash
cd frontend
npm install
```

#### 3.2 Configure Environment

```bash
cp .env.local.example .env.local
```

Edit `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

#### 3.3 Start Frontend Server

```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## Docker Setup

Docker is the recommended way to run FlexiBase, especially for production.

### 1. Install Docker

- **macOS**: [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
- **Windows**: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
- **Linux**: [Docker Engine](https://docs.docker.com/engine/install/)

### 2. Start All Services

```bash
# Development environment
docker-compose up -d

# Production environment
docker-compose -f docker-compose.prod.yml up -d
```

### 3. View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 4. Stop Services

```bash
docker-compose down

# With volume cleanup
docker-compose down -v
```

## Database Setup

### Running Migrations

#### Create a New Migration

After making changes to models:

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

Review the generated migration file in `backend/alembic/versions/`

#### Apply Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade <revision>

# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision>
```

### Seeding Initial Data

Create an admin user:

```python
# Using Python shell or create a script
from app.models import User
from app.database import AsyncSessionLocal
from app.utils.security import hash_password

async def create_admin():
    async with AsyncSessionLocal() as db:
        admin = User(
            email="admin@flexibase.com",
            username="admin",
            hashed_password=hash_password("SecurePassword123!"),
            role="admin",
            is_superuser=True,
            is_active=True,
            is_verified=True,
        )
        db.add(admin)
        await db.commit()

# Run with: python -m asyncio create_admin.py
```

## Environment Configuration

### Backend Environment Variables

**Required:**
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Secret key for JWT tokens (use a strong random string)

**Optional:**
- `DEBUG` - Enable debug mode (default: False)
- `ENVIRONMENT` - Environment name (development, staging, production)
- `ALLOWED_ORIGINS` - CORS allowed origins (comma-separated)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - JWT access token expiration (default: 30)
- `STRIPE_SECRET_KEY` - Stripe secret key
- `SENDGRID_API_KEY` - SendGrid API key for emails

### Frontend Environment Variables

**Required:**
- `NEXT_PUBLIC_API_URL` - Backend API URL

**Optional:**
- `NEXT_PUBLIC_APP_NAME` - Application name
- `NEXT_PUBLIC_APP_VERSION` - Application version

## Running the Application

### Development Mode

#### Option 1: Without Docker

Terminal 1 (Backend):
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

#### Option 2: With Docker

```bash
docker-compose up
```

### Production Mode

```bash
# Build and start
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

## Accessing the Application

Once running, access:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Alternative API Docs**: http://localhost:8000/api/redoc

## Troubleshooting

### Database Connection Issues

**Problem**: Cannot connect to database

**Solutions**:
1. Ensure PostgreSQL is running
2. Check database credentials in `.env`
3. Verify database exists
4. Check firewall settings

### Port Already in Use

**Problem**: Port 3000 or 8000 already in use

**Solutions**:
```bash
# Find process using port
lsof -i :3000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different ports
# Backend: uvicorn app.main:app --port 8001
# Frontend: npm run dev -- -p 3001
```

### Module Import Errors (Backend)

**Problem**: `ModuleNotFoundError`

**Solutions**:
1. Ensure virtual environment is activated
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check Python version: `python --version`

### Node Module Issues (Frontend)

**Problem**: Module not found or dependency issues

**Solutions**:
```bash
# Remove node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Next.js cache
rm -rf .next
npm run dev
```

### Docker Issues

**Problem**: Container fails to start

**Solutions**:
```bash
# View logs
docker-compose logs <service-name>

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d

# Clean up
docker-compose down -v
docker system prune -a
```

### Migration Issues

**Problem**: Migration fails or conflicts

**Solutions**:
```bash
# Check current migration status
alembic current

# View migration history
alembic history

# Stamp database to specific revision (use with caution)
alembic stamp head

# Downgrade and re-upgrade
alembic downgrade -1
alembic upgrade head
```

### CORS Issues

**Problem**: CORS errors in browser console

**Solutions**:
1. Check `ALLOWED_ORIGINS` in backend `.env`
2. Ensure frontend URL is included
3. Restart backend after changes

### Authentication Issues

**Problem**: JWT token errors

**Solutions**:
1. Check `SECRET_KEY` is set in backend `.env`
2. Clear browser localStorage
3. Verify token expiration settings
4. Check backend logs for detailed errors

## Testing

### Backend Tests

```bash
cd backend
pytest

# With coverage
pytest --cov=app tests/

# Specific test file
pytest tests/test_auth.py
```

### Frontend Tests

```bash
cd frontend
npm test

# With coverage
npm test -- --coverage

# Watch mode
npm test -- --watch
```

## Development Tools

### Backend Code Quality

```bash
# Format code
black app/

# Lint
flake8 app/

# Type check
mypy app/
```

### Frontend Code Quality

```bash
# Lint
npm run lint

# Type check
npm run type-check

# Fix linting issues
npm run lint -- --fix
```

## Next Steps

After successful setup:

1. Create an admin user
2. Explore the API documentation at http://localhost:8000/api/docs
3. Test authentication by registering a user
4. Review the architecture documentation in `docs/ARCHITECTURE.md`
5. Start building custom modules in `backend/app/modules/`

## Getting Help

- Check [README.md](../README.md) for project overview
- Review [ARCHITECTURE.md](./ARCHITECTURE.md) for system design
- Check API documentation at http://localhost:8000/api/docs
- Submit issues on GitHub
