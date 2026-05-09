# 🚩 CTF Platform

A minimal, lightweight CTF (Capture The Flag) platform built with Flask for hosting mini CTF challenges.

## Features

- ✅ User authentication (register/login)
- ✅ Team support
- ✅ Challenge management (Jeopardy-style)
- ✅ Flag submission system
- ✅ Real-time scoreboard
- ✅ Admin panel for creating/managing challenges
- ✅ Mobile-friendly design

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone/Copy the project**
   ```bash
   cd ctf-platform
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and change SECRET_KEY to something secure
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

   The platform will be available at `http://localhost:5000`

## First Time Setup

### Create Admin User

1. Start the app and register a regular account
2. To make it an admin, run:
   ```bash
   python -c "
   from app import create_app
   from models import db, User
   
   app = create_app()
   with app.app_context():
       user = User.query.filter_by(username='your_username').first()
       if user:
           user.is_admin = True
           db.session.commit()
           print('Admin privileges granted!')
   "
   ```

### Add Sample Challenges

Once logged in as admin, go to `/admin` and create challenges. Here's an example:

**Challenge 1:**
- Title: Welcome Challenge
- Category: General
- Points: 10
- Description: This is a simple welcome challenge to get you started!
- Flag: FLAG{welcome}

**Challenge 2:**
- Title: Secret Code
- Category: General
- Points: 50
- Description: Find the hidden secret code in the database. Hint: It's in a famous speech.
- Flag: FLAG{one_small_step}

## Deployment

### Deploy to DigitalOcean (Recommended for Workshop)

1. **Create a Droplet**
   - OS: Ubuntu 22.04
   - Size: $6/month is sufficient

2. **SSH into your droplet**
   ```bash
   ssh root@your_droplet_ip
   ```

3. **Install dependencies**
   ```bash
   apt update && apt upgrade -y
   apt install python3 python3-pip python3-venv git -y
   ```

4. **Clone your repository**
   ```bash
   git clone your_repo_url /opt/ctf-platform
   cd /opt/ctf-platform
   ```

5. **Setup and run**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

6. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
   ```

7. **Access at**: `http://your_droplet_ip:5000`

### Deploy to Heroku

1. **Create Heroku account** and install Heroku CLI

2. **Create Procfile**
   ```
   web: gunicorn "app:create_app()"
   release: python -c "from app import create_app; from models import db; app = create_app(); app.app_context().push(); db.create_all()"
   ```

3. **Add requirements**
   ```bash
   pip install gunicorn
   pip freeze > requirements.txt
   ```

4. **Deploy**
   ```bash
   heroku create your-ctf-app
   heroku addons:create heroku-postgresql:hobby-dev
   git push heroku main
   ```

## Usage

### For Participants

1. **Register** - Create an account with username, email, and optional team name
2. **Browse Challenges** - View all available challenges in the dashboard
3. **Solve & Submit** - Read challenge descriptions and submit flags
4. **Check Scoreboard** - View your ranking and others' scores

### For Admins

1. **Login** as admin account
2. **Go to Admin Panel** - `/admin`
3. **Create Challenges** - Use the form to add new challenges
4. **Monitor Activity** - View user submissions and stats
5. **Manage Challenges** - Enable/disable challenges as needed

## Project Structure

```
ctf-platform/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── models.py           # Database models
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── templates/          # HTML templates
│   ├── base.html      # Base template
│   ├── login.html     # Login page
│   ├── register.html  # Registration page
│   ├── dashboard.html # Challenge dashboard
│   ├── challenge.html # Challenge detail page
│   ├── scoreboard.html# Public scoreboard
│   └── admin.html     # Admin panel
└── static/            # Static files (CSS, JS)
```

## Database

The app uses SQLite by default (`ctf.db`). To use PostgreSQL in production:

1. Install PostgreSQL
2. Set `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost/ctfdb
   ```
3. Install psycopg2:
   ```bash
   pip install psycopg2-binary
   ```

## Security Notes

- ⚠️ Change `SECRET_KEY` in production
- ⚠️ Use HTTPS in production
- ⚠️ Don't commit `.env` file
- ⚠️ Sanitize user inputs for production
- ⚠️ Use strong passwords for admin accounts

## Tips for Your Workshop

1. **Create themed challenges** - Mix easy and hard challenges
2. **Use clear descriptions** - Help participants understand what to find
3. **Provide hints gradually** - Consider adding a hints system later
4. **Monitor submissions** - Use admin panel to see progress
5. **Announce winners** - Use the scoreboard for final rankings

## Future Enhancements

- [ ] Hints system
- [ ] File uploads/downloads
- [ ] Challenge difficulty levels
- [ ] User profiles
- [ ] Email notifications
- [ ] Dark mode
- [ ] API endpoints

## Troubleshooting

**Port 5000 already in use?**
```bash
python app.py --port 5001
```

**Database errors?**
```bash
rm ctf.db  # Delete old database
python app.py  # Restart to recreate
```

**Admin privileges not working?**
- Make sure you followed the admin creation steps above

## License

Free to use for educational purposes.

---

Good luck with your workshop! 🎯
