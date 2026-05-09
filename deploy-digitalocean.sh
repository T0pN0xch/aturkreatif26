#!/bin/bash

# CTF Platform Digital Ocean Deployment Script
# This script helps with initial setup and deployment to Digital Ocean

set -e  # Exit on error

echo "=================================================="
echo "CTF PLATFORM - DIGITAL OCEAN DEPLOYMENT HELPER"
echo "=================================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "⚠ This script must be run as root (use 'sudo')"
    exit 1
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Step 1: Update system
echo ""
print_info "Step 1: Updating system packages..."
apt update && apt upgrade -y
print_status "System packages updated"

# Step 2: Install Docker
echo ""
print_info "Step 2: Installing Docker..."
if command -v docker &> /dev/null; then
    print_status "Docker is already installed"
else
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    usermod -aG docker root
    print_status "Docker installed"
fi

# Step 3: Install Docker Compose
echo ""
print_info "Step 3: Installing Docker Compose..."
if command -v docker-compose &> /dev/null; then
    print_status "Docker Compose is already installed"
else
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    print_status "Docker Compose installed"
fi

# Step 4: Install Nginx
echo ""
print_info "Step 4: Installing Nginx..."
if command -v nginx &> /dev/null; then
    print_status "Nginx is already installed"
else
    apt install -y nginx
    systemctl start nginx
    systemctl enable nginx
    print_status "Nginx installed and started"
fi

# Step 5: Install Certbot
echo ""
print_info "Step 5: Installing Certbot (Let's Encrypt)..."
if command -v certbot &> /dev/null; then
    print_status "Certbot is already installed"
else
    apt install -y certbot python3-certbot-nginx
    print_status "Certbot installed"
fi

# Step 6: Setup firewall
echo ""
print_info "Step 6: Configuring firewall..."
ufw allow 22/tcp || true
ufw allow 80/tcp || true
ufw allow 443/tcp || true
ufw --force enable || true
print_status "Firewall configured"

# Step 7: Clone repository
echo ""
print_info "Step 7: Cloning repository..."
if [ -d "aturkreatif26" ]; then
    print_status "Repository already exists"
    cd aturkreatif26
    git pull origin main
else
    git clone https://github.com/T0pN0xch/aturkreatif26.git
    cd aturkreatif26
    print_status "Repository cloned"
fi

# Step 8: Setup environment
echo ""
print_info "Step 8: Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_info "Created .env file from template"
    print_error "⚠ IMPORTANT: Edit .env file and set secure values:"
    print_error "   - SECRET_KEY: Generate with: python3 -c \"import secrets; print(secrets.token_hex(32))\""
    print_error "   - POSTGRES_PASSWORD: Set a strong password"
    print_error "   - WRITEUP_PASSWORD: Set admin password"
    echo ""
    read -p "Have you updated the .env file with secure values? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        print_error "Please update .env file first"
        exit 1
    fi
else
    print_status ".env file already exists"
fi

# Step 9: Start Docker containers
echo ""
print_info "Step 9: Starting Docker containers..."
docker-compose -f docker-compose.prod.yml up -d
print_status "Containers started"

# Step 10: Initialize database
echo ""
print_info "Step 10: Initializing database..."
sleep 5  # Wait for database to start
docker-compose -f docker-compose.prod.yml exec -T ctf-app bash -c "cd /app && python -c 'from init import init_db; init_db()'" || true
print_status "Database initialized"

# Step 11: Setup Nginx
echo ""
print_info "Step 11: Configuring Nginx..."
if [ ! -f "/etc/nginx/sites-available/ctf-platform" ]; then
    cp nginx-ctf-platform.conf /etc/nginx/sites-available/ctf-platform
    sed -i "s|YOUR_DOMAIN_OR_IP|$(hostname -I | awk '{print $1}')|g" /etc/nginx/sites-available/ctf-platform
    ln -s /etc/nginx/sites-available/ctf-platform /etc/nginx/sites-enabled/ 2>/dev/null || true
    nginx -t && systemctl reload nginx
    print_status "Nginx configured"
else
    print_status "Nginx configuration already exists"
fi

# Final summary
echo ""
echo "=================================================="
echo -e "${GREEN}✓ DEPLOYMENT SETUP COMPLETE!${NC}"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Configure your domain DNS records to point to this server"
echo "2. Set up SSL certificate:"
echo "   sudo certbot certify --nginx -d YOUR_DOMAIN"
echo "3. Access your CTF platform at: http://$(hostname -I | awk '{print $1}')"
echo ""
echo "Useful commands:"
echo "  View logs:        docker-compose -f docker-compose.prod.yml logs -f ctf-app"
echo "  Stop containers:  docker-compose -f docker-compose.prod.yml down"
echo "  Restart app:      docker-compose -f docker-compose.prod.yml restart ctf-app"
echo "  Update code:      git pull origin main && docker-compose -f docker-compose.prod.yml up -d --build"
echo ""
echo "For more details, see DIGITALOCEAN_DEPLOYMENT.md"
echo ""
