# Digital Ocean Deployment Guide

This guide will help you deploy the ATURKREATIF CTF platform to Digital Ocean using Docker Compose.

## Prerequisites

- Digital Ocean account with billing enabled
- SSH key pair for secure access
- Domain name (optional but recommended for SSL)

---

## Step 1: Create a Digital Ocean Droplet

### 1.1 Create the Droplet
1. Go to [Digital Ocean Console](https://cloud.digitalocean.com)
2. Click **"Create"** → **"Droplets"**
3. Choose the following settings:

   **Region:**
   - Select a region closest to your users (e.g., Singapore, Amsterdam, San Francisco)

   **OS Image:**
   - Select **Ubuntu 22.04 LTS** (long-term support)

   **Droplet Type:**
   - **Basic - Shared CPU**
   - **2 GB Memory / 1 vCPU / 50 GB SSD** (minimum recommended)
   - OR **4 GB Memory / 2 vCPU / 80 GB SSD** (for production use)

   **Authentication:**
   - Select **SSH key** (recommended over password)
   - Create/select your SSH key

   **Hostname:**
   - `ctf-platform` or your preferred name

4. Click **Create Droplet**

### 1.2 Note Your Droplet IP
Once created, note the droplet's public IP address (e.g., `192.168.1.100`)

---

## Step 2: SSH into Your Droplet

```bash
# Replace with your droplet IP
ssh root@YOUR_DROPLET_IP

# Or if using a specific SSH key
ssh -i ~/.ssh/your-key root@YOUR_DROPLET_IP
```

---

## Step 3: Install Docker and Docker Compose

### 3.1 Update System Packages
```bash
apt update && apt upgrade -y
```

### 3.2 Install Docker
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (so you don't need sudo)
usermod -aG docker root
```

### 3.3 Install Docker Compose
```bash
# Download Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make it executable
chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

### 3.4 Install Nginx (Optional but Recommended)
```bash
apt install -y nginx
```

### 3.5 Install Certbot for SSL (Optional but Recommended)
```bash
apt install -y certbot python3-certbot-nginx
```

---

## Step 4: Clone Your Repository

```bash
# Navigate to home directory
cd ~

# Clone your GitHub repository
git clone https://github.com/T0pN0xch/aturkreatif26.git
cd aturkreatif26
```

---

## Step 5: Configure Environment Variables

### 5.1 Create Production Environment File
```bash
# Create a .env file for production
cat > .env << 'EOF'
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-very-secure-random-key-change-this-32-chars-min
WRITEUP_PASSWORD=your-secure-admin-password

# Database Configuration
POSTGRES_USER=ctf_user
POSTGRES_PASSWORD=your-secure-db-password-change-this
POSTGRES_DB=ctf_db
DATABASE_URL=postgresql://ctf_user:your-secure-db-password-change-this@db:5432/ctf_db

# Flask App Configuration
FLASK_APP=ctf-platform/app.py
EOF
```

### 5.2 Generate a Strong Secret Key
```bash
# Generate a random 32+ character secret key
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Update the `.env` file with the generated secret key.

---

## Step 6: Create Production Docker Compose File

Create `docker-compose.prod.yml`:

```bash
cat > docker-compose.prod.yml << 'EOF'
version: '3.8'

services:
  ctf-app:
    build:
      context: ./ctf-platform
      dockerfile: Dockerfile
    container_name: akctf-platform
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=${FLASK_ENV}
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
      - WRITEUP_PASSWORD=${WRITEUP_PASSWORD}
    depends_on:
      - db
    volumes:
      - ./ctf-platform/instance:/app/instance
      - ./ctf-platform/static:/app/static
    networks:
      - ctf-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:15-alpine
    container_name: akctf-db
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - ctf-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:

networks:
  ctf-network:
    driver: bridge
EOF
```

---

## Step 7: Configure Nginx Reverse Proxy (Recommended)

### 7.1 Create Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/ctf-platform
```

Add the following configuration:

```nginx
upstream ctf_app {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    # Redirect HTTP to HTTPS (if using SSL)
    # return 301 https://$server_name$request_uri;

    location / {
        proxy_pass http://ctf_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
        proxy_connect_timeout 60s;
    }

    # Static files
    location /static/ {
        alias /home/root/aturkreatif26/ctf-platform/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

### 7.2 Enable the Configuration
```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/ctf-platform /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

---

## Step 8: Set Up SSL/HTTPS (Let's Encrypt)

### 8.1 Get SSL Certificate
```bash
# Replace YOUR_DOMAIN with your actual domain
sudo certbot certify --nginx -d YOUR_DOMAIN

# Certbot will automatically update your Nginx configuration
```

### 8.2 Auto-Renewal
```bash
# Verify auto-renewal is set up
sudo systemctl status certbot.timer

# Test renewal
sudo certbot renew --dry-run
```

---

## Step 9: Deploy the Application

### 9.1 Start Docker Containers
```bash
# Navigate to your project directory
cd ~/aturkreatif26

# Load environment variables
export $(cat .env | xargs)

# Build and start containers
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f ctf-app
```

### 9.2 Verify Application is Running
```bash
# Check container status
docker-compose -f docker-compose.prod.yml ps

# Test the application
curl http://localhost:5000

# Or access via your domain/IP in a browser
```

---

## Step 10: Database Initialization

### 10.1 Initialize Database
```bash
# Enter the Flask app container
docker-compose -f docker-compose.prod.yml exec ctf-app bash

# Inside the container:
cd /app
python -c "from init import init_db; init_db()"

# Exit container
exit
```

### 10.2 Add Sample Challenges (Optional)
```bash
# Enter Flask shell
docker-compose -f docker-compose.prod.yml exec ctf-app bash

# Inside the container:
cd /app
python sample_challenges.py

exit
```

---

## Step 11: Configure Firewall

```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP
sudo ufw allow 80/tcp

# Allow HTTPS
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Verify rules
sudo ufw status
```

---

## Step 12: Set Up Domain Name (Optional)

If using a domain name:

1. Point your domain's DNS records to your droplet IP:
   - Type: **A Record**
   - Name: `@` (root) or your subdomain
   - Value: Your droplet IP (e.g., `192.168.1.100`)

2. Update your Nginx configuration with the domain name

3. Get SSL certificate using the domain

---

## Management Commands

### View Logs
```bash
# Application logs
docker-compose -f docker-compose.prod.yml logs -f ctf-app

# Database logs
docker-compose -f docker-compose.prod.yml logs -f db

# All logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Stop Containers
```bash
docker-compose -f docker-compose.prod.yml down
```

### Restart Containers
```bash
docker-compose -f docker-compose.prod.yml restart
```

### Update Code
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build
```

### Backup Database
```bash
# Export database dump
docker-compose -f docker-compose.prod.yml exec db pg_dump -U ctf_user ctf_db > backup_$(date +%Y%m%d).sql
```

### Restore Database
```bash
# Restore from backup
cat backup_20240510.sql | docker-compose -f docker-compose.prod.yml exec -T db psql -U ctf_user ctf_db
```

---

## Monitoring and Maintenance

### Check Disk Space
```bash
df -h
```

### Check Memory Usage
```bash
free -h
```

### Monitor Containers
```bash
docker stats
```

### Regular Updates
```bash
# Update all system packages (monthly)
apt update && apt upgrade -y

# Update Docker images
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

---

## Troubleshooting

### Port Already in Use
```bash
# Check what's using port 5000
sudo lsof -i :5000

# If needed, kill the process
sudo kill -9 PID
```

### Database Connection Issues
```bash
# Check if database is running
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs db
```

### Static Files Not Loading
```bash
# Verify static files exist
ls -la ctf-platform/static/

# Check Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### SSL Certificate Issues
```bash
# Check certificate expiration
sudo certbot certificates

# Renew manually
sudo certbot renew --force-renewal
```

---

## Security Best Practices

1. **Change Default Passwords**: Always change PostgreSQL and admin passwords
2. **Use Strong Secret Keys**: Use a cryptographically secure random key
3. **Enable Firewall**: Only allow necessary ports
4. **Use SSH Keys**: Never use password authentication for SSH
5. **Keep System Updated**: Run `apt update && apt upgrade` regularly
6. **Monitor Logs**: Regularly check application and system logs
7. **Backup Database**: Set up regular automated backups
8. **Use HTTPS**: Always use SSL/TLS encryption
9. **Update Docker Images**: Keep Docker images updated for security patches
10. **Limit Resource Access**: Use Docker resource limits

---

## Additional Resources

- [Digital Ocean Documentation](https://docs.digitalocean.com)
- [Docker Documentation](https://docs.docker.com)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## Support

For issues or questions:
1. Check logs: `docker-compose -f docker-compose.prod.yml logs`
2. Review this guide
3. Check Digital Ocean's support documentation
4. Contact your hosting provider support

---

**Last Updated:** May 10, 2026
**Version:** 1.0
