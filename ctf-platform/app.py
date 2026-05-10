from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from config import config
from models import db, User, Challenge, Submission
from datetime import datetime
import os
from io import BytesIO

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Auto-load sample challenges if database is empty
        if Challenge.query.count() == 0:
            try:
                from sample_challenges import SAMPLE_CHALLENGES
                print("📚 Loading sample challenges...")
                for challenge_data in SAMPLE_CHALLENGES:
                    challenge = Challenge(**challenge_data)
                    db.session.add(challenge)
                db.session.commit()
                print(f"✅ Loaded {Challenge.query.count()} challenges!")
            except Exception as e:
                print(f"⚠️  Could not load challenges: {e}")
                db.session.rollback()
    
    # ============ ROUTES ============
    
    @app.route('/')
    def index():
        """Home page"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """Register new user"""
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            team_name = request.form.get('team_name', '').strip()
            
            if not username or not email or not password:
                flash('All fields are required', 'error')
                return redirect(url_for('register'))
            
            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'error')
                return redirect(url_for('register'))
            
            if User.query.filter_by(email=email).first():
                flash('Email already exists', 'error')
                return redirect(url_for('register'))
            
            user = User(username=username, email=email, team_name=team_name)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        
        return render_template('register.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Login user"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        if request.method == 'POST':
            username = request.form.get('username', '')
            password = request.form.get('password', '')
            remember_me = request.form.get('remember_me')
            
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user, remember=bool(remember_me))
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password', 'error')
        
        return render_template('login.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        """Logout user"""
        logout_user()
        return redirect(url_for('login'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """User dashboard with challenges"""
        challenges = Challenge.query.filter_by(is_active=True).all()
        user_submissions = {sub.challenge_id: sub for sub in current_user.submissions}
        user_score = current_user.get_score()
        
        return render_template('dashboard.html', 
                             challenges=challenges,
                             submissions=user_submissions,
                             score=user_score)
    
    @app.route('/challenge/<int:challenge_id>')
    @login_required
    def challenge_detail(challenge_id):
        """View challenge details"""
        challenge = Challenge.query.get_or_404(challenge_id)
        user_submission = Submission.query.filter_by(
            user_id=current_user.id, 
            challenge_id=challenge_id
        ).first()
        
        return render_template('challenge.html', 
                             challenge=challenge,
                             submission=user_submission)
    
    @app.route('/api/submit', methods=['POST'])
    @login_required
    def submit_flag():
        """Submit flag for a challenge"""
        data = request.get_json() or request.form
        challenge_id = data.get('challenge_id')
        flag = data.get('flag', '').strip()
        
        challenge = Challenge.query.get(challenge_id)
        if not challenge:
            return jsonify({'error': 'Challenge not found'}), 404
        
        # Check if user already solved it
        existing = Submission.query.filter_by(
            user_id=current_user.id,
            challenge_id=challenge_id
        ).first()
        
        if existing and existing.is_correct:
            return jsonify({'error': 'You already solved this challenge'}), 400
        
        # Validate flag
        is_correct = flag.lower() == challenge.flag.lower()
        
        if existing:
            existing.flag_submitted = flag
            existing.is_correct = is_correct
            existing.submitted_at = datetime.utcnow()
        else:
            submission = Submission(
                user_id=current_user.id,
                challenge_id=challenge_id,
                flag_submitted=flag,
                is_correct=is_correct
            )
            db.session.add(submission)
        
        db.session.commit()
        
        if is_correct:
            return jsonify({
                'success': True,
                'message': 'Correct! Flag accepted.',
                'points': challenge.points
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Incorrect flag. Try again.'
            })
    
    @app.route('/scoreboard')
    def scoreboard():
        """Public scoreboard"""
        users = User.query.all()
        scoreboard_data = [(user.username, user.team_name, user.get_score()) for user in users]
        scoreboard_data.sort(key=lambda x: x[2], reverse=True)
        
        return render_template('scoreboard.html', scoreboard=scoreboard_data)
    
    # ============ WEB CHALLENGE ROUTES ============
    
    @app.route('/challenge/web/query_flag')
    def web_challenge_query():
        """Query String Challenge - Flag in URL parameters"""
        user = request.args.get('user', '')
        level = request.args.get('level', '')
        secret = request.args.get('secret', '')
        
        if user == 'admin' and level == '10' and secret == 'true':
            return '''
            <html>
            <head><title>Query Challenge</title></head>
            <body>
                <h2>Access Granted!</h2>
                <p>You successfully passed the query string challenge!</p>
                <p>Flag: <strong>FLAG{qu3ry_str1ng_p0w3r}</strong></p>
                <a href="/dashboard">Back to Dashboard</a>
            </body>
            </html>
            '''
        else:
            return '''
            <html>
            <head><title>Query Challenge</title></head>
            <body>
                <h2>Access Denied</h2>
                <p>Incorrect query parameters.</p>
                <p>Hint: Try accessing with user=admin, level=10, and secret=true</p>
                <a href="/challenge/web/query_flag?user=admin&level=10&secret=true">Retry with hint</a>
            </body>
            </html>
            '''
    
    @app.route('/challenge/web/redirect1')
    def web_challenge_redirect1():
        """Redirect chain challenge - Step 1"""
        return redirect('/challenge/web/redirect2')
    
    @app.route('/challenge/web/redirect2')
    def web_challenge_redirect2():
        """Redirect chain challenge - Step 2"""
        return redirect('/challenge/web/redirect3')
    
    @app.route('/challenge/web/redirect3')
    def web_challenge_redirect3():
        """Redirect chain challenge - Final step with flag"""
        return '''
        <html>
        <head><title>Redirect Challenge Complete</title></head>
        <body>
            <h2>Redirect Chain Complete!</h2>
            <p>You successfully followed all redirects!</p>
            <p>Flag: <strong>FLAG{r3d1r3ct_m4st3r}</strong></p>
            <a href="/dashboard">Back to Dashboard</a>
        </body>
        </html>
        '''
    
    @app.route('/challenge/web/meta_refresh')
    def web_challenge_meta_refresh():
        """Meta refresh redirect challenge"""
        return '''
        <html>
        <head>
            <title>Meta Refresh Challenge</title>
            <meta http-equiv="refresh" content="3;url=/challenge/web/meta_flag">
        </head>
        <body>
            <h2>Meta Refresh Challenge</h2>
            <p>This page will redirect in 3 seconds...</p>
            <p>Or you can <a href="/challenge/web/meta_flag">click here</a> to continue.</p>
        </body>
        </html>
        '''
    
    @app.route('/challenge/web/meta_flag')
    def web_challenge_meta_flag():
        """Meta refresh challenge - Flag page"""
        response = '''
        <html>
        <head><title>Meta Refresh Success</title></head>
        <body>
            <h2>Meta Refresh Success!</h2>
            <p>You found the flag via meta refresh!</p>
            <p>Flag: <strong>FLAG{m3t4_r3fr3sh}</strong></p>
            <a href="/dashboard">Back to Dashboard</a>
        </body>
        </html>
        '''
        return response
    
    @app.route('/challenge/web/headers_challenge')
    def web_challenge_headers():
        """HTTP Headers Challenge - Custom header with flag"""
        response = '''
        <html>
        <head><title>Headers Challenge</title></head>
        <body>
            <h2>HTTP Headers Challenge</h2>
            <p>Check the HTTP response headers for a hidden flag!</p>
            <p>Instructions:</p>
            <ol>
                <li>Open Developer Tools (F12)</li>
                <li>Go to Network tab</li>
                <li>Refresh this page</li>
                <li>Click on this request</li>
                <li>Look for the "X-Flag" header</li>
            </ol>
            <a href="/dashboard">Back to Dashboard</a>
        </body>
        </html>
        '''
        from flask import make_response
        resp = make_response(response)
        resp.headers['X-Flag'] = 'FLAG{h34d3rs_s3cr3ts}'
        resp.headers['X-Hint'] = 'Found the flag in headers!'
        resp.headers['Cache-Control'] = 'no-cache'
        return resp
    
    @app.route('/challenge/web/js_challenge')
    def web_challenge_javascript():
        """JavaScript Challenge - Flag in page source"""
        return '''
        <html>
        <head><title>JavaScript Challenge</title></head>
        <body>
            <h2>JavaScript Challenge</h2>
            <p>Check the page source or open Developer Tools console!</p>
            <p>Try typing: window.ctf_flag</p>
            <button onclick="showFlag()">Click to Show Hint</button>
            
            <script>
                // The flag is stored in this variable
                window.ctf_flag = 'FLAG{js_s0urc3_c0d3}';
                
                function showFlag() {
                    alert('Hint: Use console to access window.ctf_flag');
                }
            </script>
            <a href="/dashboard">Back to Dashboard</a>
        </body>
        </html>
        '''
    
    @app.route('/challenge/web/cookie_challenge')
    def web_challenge_cookie():
        """Cookie Challenge - Flag in cookie"""
        from flask import make_response
        response = '''
        <html>
        <head><title>Cookie Challenge</title></head>
        <body>
            <h2>Cookie Challenge</h2>
            <p>The flag is hidden in a browser cookie!</p>
            <p>Instructions:</p>
            <ol>
                <li>Open Developer Tools (F12)</li>
                <li>Go to Application tab (Chrome) or Storage (Firefox)</li>
                <li>Check the Cookies section</li>
                <li>Find the cookie named "ctf_hint"</li>
            </ol>
            <a href="/dashboard">Back to Dashboard</a>
        </body>
        </html>
        '''
        resp = make_response(response)
        resp.set_cookie('ctf_hint', 'FLAG{n0m_n0m_c00k13s}', max_age=86400)
        resp.set_cookie('session_id', '12345abcde', max_age=86400)
        return resp
    
    @app.route('/challenge/web/hidden_form')
    def web_challenge_hidden_form():
        """Hidden Form Field Challenge"""
        return '''
        <html>
        <head><title>Hidden Form Challenge</title></head>
        <body>
            <h2>Hidden Form Challenge</h2>
            <p>View the source code of this page (Ctrl+U) to find the hidden flag!</p>
            
            <form method="POST">
                <label>Username: <input type="text" name="username"></label><br>
                <!-- This is a hidden field containing a hint -->
                <input type="hidden" name="flag_data" value="FLAG{h1dd3n_f13lds}">
                <input type="submit" value="Submit">
            </form>
            
            <a href="/dashboard">Back to Dashboard</a>
        </body>
        </html>
        '''
    
    @app.route('/challenge/web/local_storage')
    def web_challenge_local_storage():
        """LocalStorage Challenge - Flag in browser storage"""
        return '''
        <html>
        <head><title>LocalStorage Challenge</title></head>
        <body>
            <h2>LocalStorage Challenge</h2>
            <p>The flag is stored in the browser's LocalStorage!</p>
            <p>Instructions:</p>
            <ol>
                <li>Open Developer Tools (F12)</li>
                <li>Go to Application > Local Storage</li>
                <li>Look for the key "flag_data"</li>
            </ol>
            <button onclick="showFromStorage()">Show from Storage</button>
            
            <script>
                // Store the flag in LocalStorage
                localStorage.setItem('flag_data', 'FLAG{l0c4l_st0r4g3}');
                localStorage.setItem('hint', 'The flag is in the flag_data key');
                
                function showFromStorage() {
                    const flag = localStorage.getItem('flag_data');
                    alert('Flag from storage: ' + flag);
                }
            </script>
            <a href="/dashboard">Back to Dashboard</a>
        </body>
        </html>
        '''
    
    @app.route('/challenge/web/path_traversal')
    def web_challenge_path_traversal():
        """Path Traversal Challenge Info Page"""
        return '''
        <html>
        <head><title>Path Traversal Challenge</title></head>
        <body>
            <h2>Path Traversal Challenge</h2>
            <p>Try accessing different paths to find the flag:</p>
            <ul>
                <li><a href="/challenge/web/admin">/admin</a></li>
                <li><a href="/challenge/web/secret">/secret</a></li>
                <li><a href="/challenge/web/config">/config</a></li>
                <li><a href="/Flag">/Flag</a></li>
                <li><a href="/flag">/flag</a></li>
            </ul>
            <a href="/dashboard">Back to Dashboard</a>
        </body>
        </html>
        '''
    
    @app.route('/challenge/web/admin')
    def web_challenge_admin():
        """Path Traversal - Admin page with flag"""
        return '''
        <html>
        <head><title>Admin Area</title></head>
        <body>
            <h2>Admin Area Accessed!</h2>
            <p>You found the admin path!</p>
            <p>Flag: <strong>FLAG{p4th_tr4v3rs4l}</strong></p>
            <a href="/challenge/web/path_traversal">Back to Challenge</a>
        </body>
        </html>
        '''
    
    @app.route('/challenge/web/secret')
    def web_challenge_secret():
        """Path Traversal - Secret page with flag"""
        return '''
        <html>
        <head><title>Secret Area</title></head>
        <body>
            <h2>Secret Area Found!</h2>
            <p>Flag: <strong>FLAG{p4th_tr4v3rs4l}</strong></p>
            <a href="/challenge/web/path_traversal">Back to Challenge</a>
        </body>
        </html>
        '''
    
    @app.route('/challenge/web/config')
    def web_challenge_config():
        """Path Traversal - Config page with flag"""
        return '''
        <html>
        <head><title>Configuration</title></head>
        <body>
            <h2>Configuration File</h2>
            <pre>
# Application Config
DEBUG=True
SECRET_KEY=super_secret_key
DATABASE=ctf.db
FLAG=FLAG{p4th_tr4v3rs4l}
API_KEY=sk-1234567890abcdef
            </pre>
            <a href="/challenge/web/path_traversal">Back to Challenge</a>
        </body>
        </html>
        '''
    
    @app.route('/challenge/web/case_sensitivity')
    def web_challenge_case_sensitivity():
        """Case Sensitivity Challenge Info"""
        return '''
        <html>
        <head><title>Case Sensitivity Challenge</title></head>
        <body>
            <h2>Case Sensitivity Challenge</h2>
            <p>URLs can be case-sensitive. Try different variations:</p>
            <ul>
                <li><a href="/challenge/web/CaseSensitive">/CaseSensitive</a></li>
                <li><a href="/challenge/web/CASESENSITIVE">/CASESENSITIVE</a></li>
                <li><a href="/challenge/web/casesensitive">/casesensitive</a></li>
                <li><a href="/challenge/web/CaSeSenSiTiVe">/CaSeSenSiTiVe</a></li>
            </ul>
            <a href="/dashboard">Back to Dashboard</a>
        </body>
        </html>
        '''
    
    @app.route('/challenge/web/casesensitive', methods=['GET', 'POST'], strict_slashes=False)
    def web_challenge_case_found():
        """Case Sensitivity - Found the flag"""
        return '''
        <html>
        <head><title>Found!</title></head>
        <body>
            <h2>You Found It!</h2>
            <p>Flag: <strong>AKCTF26{c4s3_s3ns1t1v1ty}</strong></p>
            <a href="/challenge/web/case_sensitivity">Back to Challenge</a>
        </body>
        </html>
        '''
    
    # ============ WRITEUP ROUTE ============
    
    @app.route('/api/writeup/<int:challenge_id>', methods=['POST'])
    @login_required
    def get_writeup(challenge_id):
        """Get writeup for a challenge with password protection"""
        challenge = Challenge.query.get(challenge_id)
        if not challenge:
            return jsonify({'error': 'Challenge not found'}), 404
        
        data = request.get_json() or request.form
        password = data.get('password', '').strip()
        
        # Check password
        if password != app.config['WRITEUP_PASSWORD']:
            return jsonify({
                'success': False,
                'error': 'Incorrect password'
            }), 403
        
        return jsonify({
            'success': True,
            'writeup': challenge.writeup,
            'title': challenge.title
        })
    
    @app.route('/challenge/<int:challenge_id>/download-writeup', methods=['POST'])
    @login_required
    def download_writeup(challenge_id):
        """Download challenge writeup as a file with password protection"""
        challenge = Challenge.query.get(challenge_id)
        if not challenge:
            return jsonify({'error': 'Challenge not found'}), 404
        
        data = request.get_json() or request.form
        password = data.get('password', '').strip()
        
        # Check password
        if password != app.config['WRITEUP_PASSWORD']:
            return jsonify({
                'success': False,
                'error': 'Incorrect password'
            }), 403
        
        # Create markdown file content
        filename = f"{challenge.title.replace(' ', '_')}_WRITEUP"
        content = f"""# {challenge.title}

**Challenge ID:** {challenge.id}
**Category:** {challenge.category}
**Points:** {challenge.points}
**Difficulty:** {'Easy' if challenge.points <= 30 else 'Medium' if challenge.points <= 75 else 'Hard'}

---

## Challenge Description

{challenge.description}

---

## Writeup

{challenge.writeup}

---

## Flag Format

`{challenge.flag}`

---

**Challenge Platform:** ATURKREATIF 2026
**Downloaded:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # Create BytesIO object
        file_obj = BytesIO(content.encode('utf-8'))
        
        return send_file(
            file_obj,
            mimetype='text/markdown',
            as_attachment=True,
            download_name=f"{filename}.md"
        )
    
    @app.route('/admin')
    @login_required
    def admin():
        """Admin panel"""
        if not current_user.is_admin:
            flash('Access denied', 'error')
            return redirect(url_for('dashboard'))
        
        challenges = Challenge.query.all()
        users = User.query.all()
        submissions = Submission.query.all()
        
        return render_template('admin.html', 
                             challenges=challenges,
                             users=users,
                             submissions=submissions)
    
    @app.route('/admin/challenge/new', methods=['POST'])
    @login_required
    def add_challenge():
        """Add new challenge"""
        if not current_user.is_admin:
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json() or request.form
        
        challenge = Challenge(
            title=data.get('title'),
            description=data.get('description'),
            flag=data.get('flag'),
            points=int(data.get('points', 100)),
            category=data.get('category', 'General')
        )
        
        db.session.add(challenge)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'challenge_id': challenge.id,
            'message': 'Challenge added successfully'
        })
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
