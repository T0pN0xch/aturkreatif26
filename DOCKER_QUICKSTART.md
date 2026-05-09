# Docker Quick Start Guide

## 🚀 Quick Start (5 minutes)

### Option A: Development with SQLite (Simplest)

```bash
# In the project root directory
docker-compose -f docker-compose.dev.yml up
```

✅ Done! Open http://localhost:5000

- Uses SQLite database (no setup needed)
- Auto-reloads code changes
- Perfect for development

---

### Option B: Production with PostgreSQL (Recommended)

```bash
# In the project root directory
docker-compose up
```

✅ Done! Open http://localhost:5000

- Uses PostgreSQL database (enterprise-grade)
- Multiple worker processes
- Production-ready

---

## 📋 Prerequisites

- Docker installed: https://docs.docker.com/get-docker/
- Docker Compose installed (comes with Docker Desktop)

---

## 🛑 Stop the Application

```bash
# Stop but keep data
docker-compose down

# Stop and remove all data
docker-compose down -v
```

---

## 🔍 Common Tasks

### View Logs
```bash
docker-compose logs -f
```

### Enter the Application Container
```bash
docker-compose exec ctf-app bash
```

### Access Database
```bash
# PostgreSQL (if using docker-compose)
docker-compose exec db psql -U ctf_user -d ctf_db
```

### Rebuild Images
```bash
docker-compose build --no-cache
```

### Reset Database
```bash
docker-compose down -v
docker-compose up
```

---

## 🔐 Security for Production

Before deploying to production:

1. Copy `.env.example` to `.env`
2. Update all values with strong, unique credentials
3. Never commit `.env` to version control
4. Use the docker-compose.yml (production version)
5. Consider adding a reverse proxy (nginx)

---

## 📝 Files Created

- `Dockerfile` - Production-ready image with Gunicorn
- `Dockerfile.dev` - Development image with Flask dev server
- `docker-compose.yml` - Production setup with PostgreSQL
- `docker-compose.dev.yml` - Development setup with SQLite
- `wsgi.py` - WSGI entry point for Gunicorn
- `.dockerignore` - Files to exclude from Docker image
- `.env.example` - Environment variables template
- `DOCKER.md` - Complete Docker documentation

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 5000 in use | Change port in docker-compose.yml: `5001:5000` |
| Container won't start | Check logs: `docker-compose logs` |
| Database not accessible | Ensure `db` service is running: `docker-compose ps` |
| Code changes not showing | For production, rebuild: `docker-compose build` |

---

## 📚 More Information

See `DOCKER.md` for comprehensive documentation.

---

Happy CTF-ing! 🚩
