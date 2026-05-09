# 🚩 CTF Platform Setup Complete!

Your CTF platform is ready to use! Here's what's been created:

## 📁 Project Structure

```
ctf-platform/
├── app.py                 # Main Flask application
├── config.py             # Configuration
├── models.py             # Database models
├── init.py               # Database initialization script
├── sample_challenges.py   # Sample challenges loader
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
├── .gitignore            # Git ignore file
├── start.bat             # Quick start for Windows
├── README.md             # Full documentation
├── templates/            # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── challenge.html
│   ├── scoreboard.html
│   └── admin.html
└── static/               # Static files folder
```

## 🚀 Getting Started (Windows)

### Option 1: Quick Start (Easiest)
```bash
# Double-click: start.bat
```

This will:
1. Create virtual environment
2. Install dependencies
3. Initialize database
4. Start the server

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database and create admin user
python init.py

# 5. (Optional) Add sample challenges
python sample_challenges.py

# 6. Start the server
python app.py
```

### Access the Platform

- **Main app**: http://localhost:5000
- **Login**: Use admin credentials you created
- **Admin panel**: http://localhost:5000/admin
- **Scoreboard**: http://localhost:5000/scoreboard

## 👤 Creating Your First Admin User

When you run `python init.py`, you'll be prompted to create an admin user:

```
=== Create Admin User ===
Enter admin username: admin
Enter admin email: admin@ctf.local
Enter admin password: your_secure_password
```

## 📝 Adding Challenges

### Via Admin Panel (Easiest)

1. Login as admin
2. Go to http://localhost:5000/admin
3. Fill the "Create Challenge" form
4. Click "Create Challenge"

### Via Script

```bash
python sample_challenges.py
```

This adds 6 sample challenges to test the platform.

## 🎮 Testing the Platform

1. **Register a test user** - Go to /register
2. **Solve a challenge** - Navigate to /dashboard and submit a flag
3. **Check scoreboard** - View your score at /scoreboard
4. **Admin panel** - Monitor everything at /admin

## 🌐 Deploying for Your Workshop

### Local Network (LAN)

If everyone's on the same network, find your computer's IP:

```bash
ipconfig
# Look for "IPv4 Address" (e.g., 192.168.1.100)
# Share: http://192.168.1.100:5000
```

### Online (DigitalOcean, Heroku, etc.)

See detailed instructions in **README.md** for:
- DigitalOcean deployment ($6/month)
- Heroku deployment (free tier available)
- AWS deployment
- Other cloud providers

## ⚙️ Important Configuration

### Change the Secret Key

Before deploying, update `.env`:

```
SECRET_KEY=your-super-secret-random-string-here
```

Generate a secure key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Database

Default uses SQLite (`ctf.db`). For production with more users:

1. Use PostgreSQL (see README.md)
2. Update `DATABASE_URL` in `.env`

## 🔧 Troubleshooting

**Port 5000 already in use?**
```bash
# Use a different port
python app.py --port 8000
```

**Database issues?**
```bash
# Delete old database and recreate
del ctf.db
python init.py
```

**Virtual environment issues?**
```bash
# Deactivate and recreate
deactivate
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 📊 Features Available

✅ User authentication
✅ Team support  
✅ Jeopardy-style challenges
✅ Flag submission system
✅ Scoring system
✅ Real-time scoreboard
✅ Admin panel
✅ Mobile-friendly design

## 🎯 Quick Tips for Your Workshop

1. **Create themed challenges** - Mix easy (10 pts) and hard (500 pts)
2. **Clear descriptions** - Help participants understand the goal
3. **Multiple categories** - Web, Crypto, General, Forensics, etc.
4. **Monitor progress** - Use admin panel to see submissions in real-time
5. **Announce winners** - Use the scoreboard to celebrate top players

## 📚 Next Steps

1. [ ] Complete initial setup (run start.bat or init.py)
2. [ ] Login as admin
3. [ ] Test creating a challenge in admin panel
4. [ ] Register a test player account
5. [ ] Solve a test challenge to verify flow
6. [ ] Deploy to internet (if needed for workshop)
7. [ ] Prepare actual CTF challenges
8. [ ] Share link with workshop participants

## 🆘 Need Help?

Check **README.md** for:
- Full feature documentation
- Deployment guides
- Security best practices
- API information
- Advanced configuration

---

**Your platform is ready! Good luck with your workshop! 🎉**
