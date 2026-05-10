"""
Web Challenge Endpoints - Provides challenge instances for web-based CTF challenges
"""

from flask import Blueprint, render_template_string, request, redirect, url_for, jsonify

web_challenges = Blueprint('web_challenges', __name__, url_prefix='/web-challenges')

# ==================== Hidden in Comments ====================
@web_challenges.route('/comments')
def hidden_comments():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hidden in Comments Challenge</title>
        <style>
            body { font-family: Arial; padding: 20px; background: #f0f0f0; }
            .container { max-width: 600px; margin: 50px auto; background: white; padding: 20px; border-radius: 5px; }
            h1 { color: #0033ff; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hidden in Comments Challenge</h1>
            <p>Look at the HTML source code (Ctrl+U) to find the flag hidden in comments!</p>
            <!-- FLAG IS HERE: AKCTF26{always_check_source} -->
            <!-- This is a hint for CTF players -->
            <!-- The flag format is: AKCTF26{...} -->
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

# ==================== HTTP Headers Mystery ====================
@web_challenges.route('/headers')
def http_headers():
    response_text = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>HTTP Headers Challenge</title>
        <style>
            body { font-family: monospace; padding: 20px; background: #1e1e1e; color: #00ff00; }
            .container { max-width: 600px; margin: 50px auto; }
            h1 { color: #ffff00; }
            code { display: block; margin: 10px 0; padding: 10px; background: #000; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>HTTP Headers Mystery</h1>
            <p>Check the HTTP response headers in DevTools (F12)!</p>
            <p>Open DevTools → Network tab → Click this request → Look for custom headers</p>
            <code>The flag is in a custom header called "X-CTF-Flag"</code>
        </div>
    </body>
    </html>
    '''
    from flask import make_response
    response = make_response(response_text)
    response.headers['X-CTF-Flag'] = 'AKCTF26{headers_expose_secrets}'
    return response

# ==================== JavaScript Variable Hunt ====================
@web_challenges.route('/js-challenge')
def js_challenge():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>JavaScript Variable Challenge</title>
        <style>
            body { font-family: Arial; padding: 20px; background: #f0f0f0; }
            .container { max-width: 600px; margin: 50px auto; background: white; padding: 20px; border-radius: 5px; }
            h1 { color: #0033ff; }
        </style>
        <script>
            var ctfFlag = "AKCTF26{javascript_variables_are_visible}";
            var userSecret = "HIDDEN_SECRET_123";
            window.flag = ctfFlag;
        </script>
    </head>
    <body>
        <div class="container">
            <h1>JavaScript Variable Hunt</h1>
            <p>Open DevTools (F12) → Console</p>
            <p>Type: <code>ctfFlag</code> or <code>window.flag</code></p>
            <p>JavaScript is client-side, so all variables are visible to users!</p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

# ==================== Cookie Monster ====================
@web_challenges.route('/cookie-challenge')
def cookie_challenge():
    from flask import make_response
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cookie Monster Challenge</title>
        <style>
            body { font-family: Arial; padding: 20px; background: #f0f0f0; }
            .container { max-width: 600px; margin: 50px auto; background: white; padding: 20px; border-radius: 5px; }
            h1 { color: #0033ff; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Cookie Monster Challenge</h1>
            <p>Open DevTools (F12) → Application → Cookies</p>
            <p>Look for a cookie with the flag in its value!</p>
            <p>Cookies are stored locally and sent with every request.</p>
        </div>
    </body>
    </html>
    '''
    response = make_response(render_template_string(html))
    response.set_cookie('ctf_hint', 'AKCTF26{n0m_n0m_c00k13s}', max_age=3600)
    return response

# ==================== Query String Secrets ====================
@web_challenges.route('/challenge')
def query_string():
    user = request.args.get('user')
    level = request.args.get('level')
    secret = request.args.get('secret')
    
    if user == 'admin' and level == '10' and secret == 'true':
        flag_text = 'AKCTF26{qu3ry_str1ng_p0w3r}'
    else:
        flag_text = 'Missing or incorrect parameters. Try: ?user=admin&level=10&secret=true'
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Query String Challenge</title>
        <style>
            body {{ font-family: Arial; padding: 20px; background: #f0f0f0; }}
            .container {{ max-width: 600px; margin: 50px auto; background: white; padding: 20px; border-radius: 5px; }}
            h1 {{ color: #0033ff; }}
            .flag {{ background: #ffffcc; padding: 10px; border-left: 4px solid #ffcc00; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Query String Challenge</h1>
            <p>URL parameters can contain sensitive data!</p>
            <div class="flag"><strong>Flag:</strong> {flag_text}</div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

# ==================== LocalStorage ====================
@web_challenges.route('/storage')
def local_storage():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>LocalStorage Challenge</title>
        <style>
            body { font-family: Arial; padding: 20px; background: #f0f0f0; }
            .container { max-width: 600px; margin: 50px auto; background: white; padding: 20px; border-radius: 5px; }
            h1 { color: #0033ff; }
        </style>
        <script>
            localStorage.setItem('flag_data', 'AKCTF26{l0c4l_st0r4g3}');
            localStorage.setItem('user_id', '12345');
        </script>
    </head>
    <body>
        <div class="container">
            <h1>LocalStorage Challenge</h1>
            <p>Open DevTools (F12) → Application → Local Storage</p>
            <p>Look for the stored flag data!</p>
            <p>LocalStorage persists between page refreshes.</p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

# ==================== Redirect Chain ====================
@web_challenges.route('/redirect1')
def redirect1():
    return redirect('/web-challenges/redirect2')

@web_challenges.route('/redirect2')
def redirect2():
    return redirect('/web-challenges/redirect3')

@web_challenges.route('/redirect3')
def redirect3():
    return redirect('/web-challenges/redirect-final')

@web_challenges.route('/redirect-final')
def redirect_final():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Redirect Chain Complete</title>
        <style>
            body { font-family: Arial; padding: 20px; background: #f0f0f0; }
            .container { max-width: 600px; margin: 50px auto; background: white; padding: 20px; border-radius: 5px; }
            .flag { background: #ccffcc; padding: 15px; border-left: 4px solid #00cc00; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Redirect Chain Complete!</h1>
            <p>You followed the redirect chain successfully!</p>
            <div class="flag">Flag: AKCTF26{follow_the_redirects}</div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

# ==================== Meta Refresh ====================
@web_challenges.route('/meta-challenge')
def meta_refresh():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Meta Refresh Challenge</title>
        <meta http-equiv="refresh" content="5;url=/web-challenges/meta-result">
        <style>
            body { font-family: Arial; padding: 20px; background: #f0f0f0; }
            .container { max-width: 600px; margin: 50px auto; background: white; padding: 20px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Meta Refresh Challenge</h1>
            <p>This page will redirect in 5 seconds...</p>
            <p>Meta refresh is an old way to redirect (not recommended).</p>
            <p>Redirecting to the flag page...</p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

@web_challenges.route('/meta-result')
def meta_result():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Meta Refresh Result</title>
        <style>
            body { font-family: Arial; padding: 20px; background: #f0f0f0; }
            .container { max-width: 600px; margin: 50px auto; background: white; padding: 20px; border-radius: 5px; }
            .flag { background: #e6f3ff; padding: 15px; border-left: 4px solid #0033ff; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Meta Refresh Result</h1>
            <div class="flag"><strong>Flag:</strong> AKCTF26{meta_refresh_works}</div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

# ==================== Path Traversal ====================
@web_challenges.route('/file')
def path_traversal():
    path = request.args.get('path', 'default.txt')
    
    # Safe files
    safe_files = {
        'default.txt': 'Welcome to Path Traversal Challenge',
        'secret.txt': 'AKCTF26{path_traversal_blocked}',
        '../etc/passwd': 'ERROR: Path traversal blocked!',
    }
    
    content = safe_files.get(path, f'File not found: {path}')
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Path Traversal Challenge</title>
        <style>
            body {{ font-family: monospace; padding: 20px; background: #1e1e1e; color: #00ff00; }}
            .container {{ max-width: 600px; margin: 50px auto; }}
            code {{ display: block; padding: 10px; background: #000; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Path Traversal Challenge</h1>
            <p>Try accessing different files:</p>
            <p><a href="?path=default.txt">/file?path=default.txt</a></p>
            <p><a href="?path=secret.txt">/file?path=secret.txt</a></p>
            <code>{content}</code>
            <p><em>Note: This is protected - malicious paths are blocked</em></p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

# ==================== Case Sensitivity ====================
@web_challenges.route('/case/<path:resource>')
def case_sensitivity(resource):
    if resource.lower() == 'flag':
        flag = 'AKCTF26{case_matters}'
    else:
        flag = 'Not found. Try different cases of "flag": flag, Flag, FLAG, etc.'
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Case Sensitivity Challenge</title>
        <style>
            body {{ font-family: Arial; padding: 20px; background: #f0f0f0; }}
            .container {{ max-width: 600px; margin: 50px auto; background: white; padding: 20px; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Case Sensitivity Challenge</h1>
            <p>URLs are case-sensitive! Try different cases:</p>
            <p>Result: {flag}</p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

# ==================== SQL Injection ====================
@web_challenges.route('/login')
def sql_injection():
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    
    # Simulated check (not actually vulnerable - just for the challenge)
    if username == 'admin' and password == "' OR '1'='1":
        message = 'AKCTF26{sql_injection_detected}'
    elif username and password:
        message = 'Login failed. Try SQL injection: password = \' OR \'1\'=\'1'
    else:
        message = 'Enter username and password'
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>SQL Injection Challenge</title>
        <style>
            body {{ font-family: Arial; padding: 20px; background: #f0f0f0; }}
            .container {{ max-width: 600px; margin: 50px auto; background: white; padding: 20px; border-radius: 5px; }}
            form {{ margin-top: 20px; }}
            input {{ padding: 8px; margin: 5px 0; width: 100%; }}
            button {{ padding: 10px; background: #0033ff; color: white; border: none; cursor: pointer; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>SQL Injection Basics</h1>
            <p>Result: {message}</p>
            <form method="get">
                <input type="text" name="username" placeholder="Username" value="{username}">
                <input type="text" name="password" placeholder="Password" value="{password}">
                <button type="submit">Login</button>
            </form>
            <p><small>Hint: Try using SQL syntax in the password field!</small></p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)
