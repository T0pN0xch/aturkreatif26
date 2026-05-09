# Docker Setup Guide for AKCTF Platform

## Option 1: Using Docker Compose (Recommended)

This setup includes the Flask app and PostgreSQL database.

### Prerequisites
- Docker and Docker Compose installed
- Port 5000 and 5432 available on your machine

### Steps

1. **Build and start the containers:**
   ```bash
   docker-compose up -d
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f ctf-app
   ```

3. **Access the application:**
   - Open http://localhost:5000 in your browser

4. **Initialize the database:**
   The database tables are created automatically when the app starts.

5. **Stop the containers:**
   ```bash
   docker-compose down
   ```

### Environment Variables

Update the following in `docker-compose.yml` before deploying to production:
- `SECRET_KEY` - Set a strong secret key
- `WRITEUP_PASSWORD` - Set admin writeup password
- Database credentials (POSTGRES_USER, POSTGRES_PASSWORD)

### Persistent Data

- Database data is stored in the `postgres_data` volume
- Application data is stored in `ctf-platform/instance` directory
- Static files are mounted from `ctf-platform/static`

---

## Option 2: Using Dockerfile Directly (Development)

For quick local testing without PostgreSQL:

1. **Build the Docker image:**
   ```bash
   cd ctf-platform
   docker build -t akctf-platform .
   ```

2. **Run the container:**
   ```bash
   docker run -p 5000:5000 \
     -e FLASK_ENV=development \
     -e SECRET_KEY=dev-secret-key \
     -v "$(pwd)/instance:/app/instance" \
     -v "$(pwd)/static:/app/static" \
     akctf-platform
   ```

3. **Access the application:**
   - Open http://localhost:5000 in your browser

4. **To run with SQLite database:**
   ```bash
   docker run -p 5000:5000 \
     -e FLASK_ENV=development \
     -e DATABASE_URL=sqlite:///ctf.db \
     -v "$(pwd)/instance:/app/instance" \
     akctf-platform
   ```

---

## Docker Compose Configuration Details

### Services

**ctf-app**
- Flask application running with Gunicorn
- Port: 5000
- Uses PostgreSQL for data storage
- Volumes: instance directory and static files

**db**
- PostgreSQL 15 Alpine (lightweight)
- Port: 5432 (not exposed externally, only to ctf-app)
- Persistent volume: `postgres_data`

### Network

- Both services communicate via `ctf-network` bridge
- App can reach database at `db:5432`

---

## Useful Docker Commands

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# Execute command in container
docker-compose exec ctf-app bash

# Restart services
docker-compose restart

# Remove containers and volumes
docker-compose down -v

# Rebuild images
docker-compose build --no-cache
```

---

## Troubleshooting

### Port already in use
```bash
# Change ports in docker-compose.yml
# Or kill the process using the port
# On Windows: netstat -ano | findstr :5000
```

### Database connection errors
- Ensure `db` service is running: `docker-compose ps`
- Check logs: `docker-compose logs db`

### Application not starting
- Check app logs: `docker-compose logs ctf-app`
- Ensure all environment variables are set

### Resetting the database
```bash
docker-compose down -v
docker-compose up -d
```

---

## Production Deployment

Before deploying to production:

1. **Update `docker-compose.yml`:**
   - Change `FLASK_ENV` to `production`
   - Set strong `SECRET_KEY`
   - Change database credentials
   - Consider using secrets management

2. **Security considerations:**
   - Use environment files (.env) for sensitive data
   - Never commit secrets to version control
   - Use strong passwords
   - Consider reverse proxy (nginx) in front
   - Enable HTTPS

3. **Deployment example with .env file:**
   ```bash
   docker-compose --env-file .env.production up -d
   ```

4. **Example .env file structure:**
   ```
   FLASK_ENV=production
   SECRET_KEY=your-very-strong-secret-key-here
   WRITEUP_PASSWORD=secure-password
   POSTGRES_USER=ctf_user
   POSTGRES_PASSWORD=secure-database-password
   ```

---

## Accessing the Database

```bash
# Connect to PostgreSQL from host machine
psql -h localhost -U ctf_user -d ctf_db

# Connect from Docker container
docker-compose exec db psql -U ctf_user -d ctf_db
```

---

For more information, see the main README.md in the ctf-platform directory.
