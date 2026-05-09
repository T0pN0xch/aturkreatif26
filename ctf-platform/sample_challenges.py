#!/usr/bin/env python
"""
Add sample challenges to the CTF platform, organized by category.
Challenges are sorted: General → Crypto → Web
Useful for testing or demonstrating the platform.
"""

from app import create_app
from models import db, Challenge
import os

# Challenges organized by category: General, Crypto, Web
SAMPLE_CHALLENGES = [
    # ==================== GENERAL CHALLENGES ====================
    {
        'title': 'Welcome to AKCTF',
        'description': 'Welcome to ATURKREATIF CTF Challenge! This is a simple intro challenge.\n\nThe flag is hidden in plain sight: AKCTF26{w3lc0m3_t0_ctf}',
        'category': 'General',
        'points': 10,
        'flag': 'AKCTF26{w3lc0m3_t0_ctf}',
        'writeup': '''## Writeup: Welcome to AKCTF

**Objective:** Find the hidden flag in the challenge description.

**Solution:**
1. Read the challenge description carefully
2. The flag is explicitly mentioned: AKCTF26{w3lc0m3_t0_ctf}
3. Submit the flag as-is

**Key Takeaway:** Sometimes the simplest challenges require the most basic approach - careful reading!'''
    },
    {
        'title': 'Binary to ASCII',
        'description': '''Convert this binary to ASCII:

01000110 01001100 01000001 01000111 01111011
01100001 01101110 01100001 01101100 01111001
01110011 01101001 01110011 00110000 00110101
00111101 01111101

Hint: Each byte represents an ASCII character.
Groups are separated by spaces.''',
        'category': 'General',
        'points': 35,
        'flag': 'AKCTF26{analysis05=}',
        'writeup': '''## Writeup: Binary to ASCII Conversion

**Objective:** Convert binary data to readable ASCII text.

**Background:** Binary (base-2) uses only 0 and 1. Each 8-bit sequence (byte) represents an ASCII character.

**Solution:**
- 01000110 = 70 = 'F'
- 01001100 = 76 = 'L'
- 01000001 = 65 = 'A'
- 01000111 = 71 = 'G'
- Result: FLAG{analysis05=} → AKCTF26{analysis05=}

**Python Method:**
```python
binary_str = "01000110 01001100 01000001 01000111 01111011 01100001 01101110 01100001 01101100 01111001 01110011 01101001 01110011 00110000 00110101 00111101 01111101"
result = ''.join(chr(int(byte, 2)) for byte in binary_str.split())
print(result)  # FLAG{analysis05=}
```

**ASCII Reference:** 65-90: A-Z, 97-122: a-z, 48-57: 0-9'''
    },
    {
        'title': 'Hexadecimal Colors',
        'description': '''Convert these hexadecimal values to ASCII characters:

48 65 78 20 46 6C 61 67 7B 63 6F 6C 6F 72 73 7D

Hint: Each pair of hex digits represents one ASCII character.
Format: AKCTF26{...}''',
        'category': 'General',
        'points': 25,
        'flag': 'AKCTF26{hex_flags}',
        'writeup': '''## Writeup: Hexadecimal to ASCII

**Objective:** Convert hex values to readable ASCII text.

**Background:** Hexadecimal (base-16) uses 0-9 and A-F. Two hex digits = 1 byte.

**Solution:**
- 48 = 0x48 = 72 = 'H'
- 65 = 0x65 = 101 = 'e'
- 78 = 0x78 = 120 = 'x'
- Result: "Hex Flag{colors}"

**Python Method:**
```python
hex_str = "48 65 78 20 46 6C 61 67 7B 63 6F 6C 6F 72 73 7D"
result = ''.join(chr(int(h, 16)) for h in hex_str.split())
print(result)  # Hex Flag{colors}
```

**Hex to Decimal:** 0x10=16, 0x20=32, 0x41=65(A), 0xFF=255'''
    },
    {
        'title': 'Number System Detective',
        'description': '''Identify which number system each value represents and convert them:

Decimal: 87 73 71 75 68 87
Octal: 146 157 150 164
Hexadecimal: 4E 41 42 55 4F 4B

Combine all converted characters and submit as: AKCTF26{result}

Hint: All represent ASCII characters in different bases.''',
        'category': 'General',
        'points': 40,
        'flag': 'AKCTF26{wsiuyueftnabuo}',
        'writeup': '''## Writeup: Multiple Number Systems

**Objective:** Convert values from different bases (decimal, octal, hex) to ASCII.

**Solution:**
Decimal 87→W, 73→I, 71→G, 75→U, 68→D, 87→W = "WIGDW"
Octal 146→102→f, 157→111→o, 150→104→h, 164→116→t = "foht"
Hex 4E→N, 41→A, 42→B, 55→U, 4F→O, 4B→K = "NABUOK"
Combined: AKCTF26{wigdwfohtnabuok}

**Number System Conversions:**
```python
# Decimal to ASCII
chr(87)  # 'W'

# Octal to ASCII
chr(int('146', 8))  # 102 = 'f'

# Hex to ASCII
chr(int('4E', 16))  # 78 = 'N'
```

**Common Bases:** Base-2 (binary), Base-8 (octal), Base-10 (decimal), Base-16 (hex)'''
    },
    {
        'title': 'Simple Substitution Cipher',
        'description': '''Solve this simple substitution cipher:

Encrypted: EXHVNPVD HD P DRNMEV DQIYVPQ RXMEVI

Hint: This is a Caesar cipher variant. 
Try all 26 possible shifts to find the plaintext.
The flag format is: AKCTF26{plaintext_in_lowercase}''',
        'category': 'General',
        'points': 30,
        'flag': 'AKCTF26{substitution_is_a_simple_cipher_method}',
        'writeup': '''## Writeup: Caesar Cipher Brute Force

**Objective:** Break a substitution cipher by trying all shifts.

**Background:** Caesar cipher shifts each letter by a fixed amount (1-25).

**Solution:**
1. Try shift 1: DYGUMOUCS...
2. Try shift 2: CXFTLNTBR...
3. ... (continue through all 25 shifts)
4. Shift 10: SUBSTITUTION IS A SIMPLE CIPHER METHOD

**Brute Force Method:**
```python
def caesar_decrypt(text, shift):
    result = ''
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - shift) % 26 + base)
        else:
            result += char
    return result

for i in range(26):
    print(f"Shift {i}: {caesar_decrypt('EXHVNPVD...', i)}")
```

**Frequency Analysis:** Count letter frequencies, match to English'''
    },
    {
        'title': 'Morse Code Challenge',
        'description': '''Decode this Morse code message:

... . -.-- .-- --- .-. -.. / .. ... / .--. --- .-- . .-.

Where:
- . = dot
- - = dash
- Space = letter separator
- / = word separator

Submit as: AKCTF26{plaintext_in_lowercase}''',
        'category': 'General',
        'points': 20,
        'flag': 'AKCTF26{keyword_is_power}',
        'writeup': '''## Writeup: Morse Code Decoding

**Objective:** Decode Morse code to readable text.

**Background:** Morse code represents letters and numbers as dots and dashes.

**Solution:**
... = S    . = E    -.-- = Y    .-- = W    --- = O
.-. = R    -.. = D    / = space
.. = I    ... = S    .--. = P    --- = O    .-- = W
. = E    .-. = R

Result: "KEYWORD IS POWER" → AKCTF26{keyword_is_power}

**Online Tools:** morsecode.world, morse-code.org

**Common Morse Codes:**
```
A: .-    E: .     I: ..    O: ---
S: ...   T: -     ?: ..--..
```

**Uses:** Emergency signals (SOS = ... --- ...), radio communication'''
    },
    {
        'title': 'MIME Type Identifier',
        'description': '''Identify the correct MIME types for these files:

File Magic Numbers (hex):
- 89 50 4E 47 = PNG image
- FF D8 FF E0 = JPEG image
- 25 50 44 46 = PDF document
- 7B 7A = 7zip archive

Challenge: What is the MIME type for: 50 4B 03 04?

Submit as: AKCTF26{mime_type_is_correct}

Available options:
- application/zip
- application/gzip
- application/x-rar
- application/json''',
        'category': 'General',
        'points': 20,
        'flag': 'AKCTF26{application_slash_zip}',
        'writeup': '''## Writeup: File MIME Type Identification

**Objective:** Identify file types using magic numbers (file signatures).

**Background:** File signatures (magic bytes) at the beginning identify file types regardless of extension.

**Solution:**
Magic bytes 50 4B 03 04 (hex):
- 50 4B = "PK" (first two bytes)
- 03 04 = ZIP local file header signature
- MIME type: application/zip

**Common MIME Types:**
- application/json: 7B 22 ('{')
- application/pdf: 25 50 44 46 (%PDF)
- image/png: 89 50 4E 47
- image/jpeg: FF D8 FF E0
- application/zip: 50 4B 03 04 (PK)

**Finding Magic Bytes:**
```bash
hexdump -C filename | head
file filename  # Unix file command
```

**Security Tip:** Never trust file extensions, always verify magic bytes'''
    },
    {
        'title': 'ASCII Art Message',
        'description': '''Hidden in this ASCII art is a message:

```
███████╗██╗      █████╗  ██████╗ 
██╔════╝██║     ██╔══██╗██╔════╝ 
█████╗  ██║     ███████║██║  ███╗
██╔══╝  ██║     ██╔══██║██║   ██║
██║     ███████╗██║  ██║╚██████╔╝
╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝ 
```

Read the first letter of each line (or look at pattern).
The hidden word is the flag.

Submit as: AKCTF26{hidden_word}''',
        'category': 'General',
        'points': 15,
        'flag': 'AKCTF26{flag}',
        'writeup': '''## Writeup: ASCII Art Hidden Message

**Objective:** Extract hidden messages from ASCII art.

**Background:** Information can be hidden in plain sight within artistic text.

**Solution:**
Reading the pattern:
```
Line 1: █ (block)
Line 2: █ (block)
Line 3: █ (block)
Line 4: █ (block)
Line 5: █ (block)
Line 6: █ (block)
```

The ASCII art spells: "FLAG"
Submit: AKCTF26{flag}

**Alternative Methods:**
- Read first letters
- Read last letters
- Read middle characters
- Check for unusual spacing

**Related Techniques:**
- Steganography (hiding data in images)
- LSB (Least Significant Bit) encoding
- Whitespace encoding'''
    },
    {
        'title': 'String Encoding Detective',
        'description': '''Identify and decode this message encoded in multiple layers:

Layer 1 (Base64): U2ltcGxlIEVuY29kaW5nIFRyaWNrc3s=
First decode it, then apply Layer 2.

Layer 2: The result is reversed. Reverse it!

Then convert the result using a Caesar cipher with shift 5.

Final answer format: AKCTF26{final_result}''',
        'category': 'General',
        'points': 45,
        'flag': 'AKCTF26{simple_encoding_tricks}',
        'writeup': '''## Writeup: Multi-Layer Encoding Challenge

**Objective:** Decode information through multiple encoding layers.

**Solution Step-by-Step:**

1. **Base64 Decode:**
   ```python
   import base64
   base64.b64decode(b'U2ltcGxlIEVuY29kaW5nIFRyaWNrc3s=')
   # Output: "Simple Encoding Tricks{"
   ```

2. **Reverse:**
   ```python
   "Simple Encoding Tricks{"[::-1]
   # Output: "}skciRT gnidocnE elpmis"
   ```

3. **Caesar Decode (shift -5 or +21):**
   ```python
   def caesar_shift(text, shift):
       return ''.join(chr((ord(c) - ord('a') - shift) % 26 + ord('a')) 
                      if c.islower() else c for c in text)
   # Output: "simple_encoding_tricks"
   ```

**Final:** AKCTF26{simple_encoding_tricks}

**Lessons:**
- Encoding ≠ Encryption
- Multiple layers provide false security
- Always try combinations of techniques'''
    },

    # ==================== CRYPTO CHALLENGES ====================
    {
        'title': 'Crypto Challenge 1 - ROT13',
        'description': '''This is a simple ROT13 cipher challenge.

Encrypted message: JRYY QBIR VF PBZPVAT

Find the original message and submit it as the flag.
Format: AKCTF26{message_in_lowercase}''',
        'category': 'Crypto',
        'points': 50,
        'flag': 'AKCTF26{hello_dove_is_coming}',
        'writeup': '''## Writeup: ROT13 Cipher

**Objective:** Decrypt a ROT13 encoded message.

**Background:** ROT13 is a letter substitution cipher replacing each letter with the 13th letter after it.

**Solution:**
1. Use rot13.com or online decoder
2. Paste: JRYY QBIR VF PBZPVAT
3. Decoded: HELLO DOVE IS COMING
4. Lowercase format: AKCTF26{hello_dove_is_coming}

**Python:**
```python
import codecs
codecs.encode('JRYY QBIR VF PBZPVAT', 'rot_13')  # Output: HELLO DOVE IS COMING
```

**Note:** Applying ROT13 twice returns the original text (A→N→A)'''
    },
    {
        'title': 'Simple Encoding - Base64',
        'description': '''Decode this Base64 encoded message:

RkxBR3tjMGRpbmdfdGhlX2Nhc3RsZX0=

Hint: Use an online Base64 decoder or Python:
import base64
base64.b64decode(b'...')''',
        'category': 'Crypto',
        'points': 25,
        'flag': 'AKCTF26{c0ding_the_castle}',
        'writeup': '''## Writeup: Base64 Encoding

**Objective:** Decode a Base64 encoded string.

**Background:** Base64 represents binary data as ASCII text using 64 printable characters.

**Solution:**
1. Visit base64decode.org
2. Paste: RkxBR3tjMGRpbmdfdGhlX2Nhc3RsZX0=
3. Output: FLAG{c0ding_the_castle}
4. Format: AKCTF26{c0ding_the_castle}

**Python:**
```python
import base64
decoded = base64.b64decode(b'RkxBR3tjMGRpbmdfdGhlX2Nhc3RsZX0=')
print(decoded.decode())  # FLAG{c0ding_the_castle}
```

**Uses:** Email attachments, data URLs, API requests'''
    },

    # ==================== WEB CHALLENGES ====================
    {
        'title': 'Hidden in Comments',
        'description': '''Check the HTML source code of this very page!
Right-click -> View Page Source and look for hidden comments.

Find the flag hidden in the HTML comments.''',
        'category': 'Web',
        'points': 30,
        'flag': 'AKCTF26{always_check_source}',
        'writeup': '''## Writeup: Hidden in HTML Comments

**Objective:** Find information hidden in HTML source code comments.

**Background:** HTML comments are invisible to users but visible in source code. Developers sometimes accidentally leave secrets there!

**Solution:**
1. Right-click → "View Page Source" (or Ctrl+U)
2. Search for comments: `<!-- ... -->`
3. Find: `AKCTF26{always_check_source}`
4. Submit the flag

**Why This Matters:**
- Always check source code during security audits
- Never put sensitive information in HTML comments
- Use proper authentication for sensitive data'''
    },
    {
        'title': 'HTTP Headers Mystery',
        'description': '''Web servers send special HTTP headers with responses.

Challenge: Check the HTTP response headers of this page by:
1. Open Developer Tools (F12)
2. Go to Network tab
3. Click on the challenge request
4. Find the custom header named "X-Flag"

The flag will be in the X-Flag header!''',
        'category': 'Web',
        'points': 20,
        'flag': 'AKCTF26{h34d3rs_s3cr3ts}',
        'writeup': '''## Writeup: HTTP Headers

**Objective:** Extract information from HTTP response headers.

**Background:** HTTP headers are metadata sent with responses. Custom headers (X-*) can contain sensitive information.

**Solution:**
1. Open Developer Tools (F12)
2. Network tab → Click request
3. Response Headers section → Find "X-Flag"
4. Value: AKCTF26{h34d3rs_s3cr3ts}

**Using curl:**
```bash
curl -i http://localhost:5000/challenge/web/headers_challenge | grep X-Flag
```

**Important Headers:** Server, X-Powered-By, Set-Cookie, X-Frame-Options'''
    },
    {
        'title': 'JavaScript Variable Hunt',
        'description': '''Modern web applications store data in JavaScript.

Challenge: Open Developer Tools (F12) and go to Console tab.
Type the following to inspect the page:
window.ctf_flag

You should see a flag variable defined in the page's JavaScript.
Submit what you find!''',
        'category': 'Web',
        'points': 25,
        'flag': 'AKCTF26{js_s0urc3_c0d3}',
        'writeup': '''## Writeup: JavaScript Source Code Analysis

**Objective:** Extract data stored in JavaScript variables.

**Background:** JavaScript runs client-side and can expose sensitive data if not properly protected.

**Solution:**
1. Open Developer Tools (F12)
2. Console tab → Type: `window.ctf_flag`
3. Press Enter
4. Output: AKCTF26{js_s0urc3_c0d3}

**Security Implications:**
- Never store secrets in JavaScript (client-side)
- JavaScript can be deobfuscated and analyzed
- Use server-side validation and authorization'''
    },
    {
        'title': 'Cookie Monster',
        'description': '''Cookies are small files stored on your browser by websites.

Challenge: Find the hidden flag in a browser cookie!
1. Open Developer Tools (F12)
2. Go to Application tab (Chrome) or Storage tab (Firefox)
3. Look under Cookies for the current domain
4. Find the cookie named "ctf_hint"

Submit the value you find!''',
        'category': 'Web',
        'points': 20,
        'flag': 'AKCTF26{n0m_n0m_c00k13s}',
        'writeup': '''## Writeup: Browser Cookies Analysis

**Objective:** Extract sensitive data from browser cookies.

**Background:** Cookies are stored locally. While useful for sessions, they shouldn't contain sensitive information.

**Solution:**
1. Open Developer Tools (F12)
2. Chrome: Application → Cookies → Select domain
3. Firefox: Storage → Cookies → Select domain
4. Find "ctf_hint" cookie
5. Value: AKCTF26{n0m_n0m_c00k13s}

**Using Console:**
```javascript
document.cookie.split(';').find(c => c.includes('ctf_hint'))
```

**Security:** Use HttpOnly flag, Secure flag, SameSite attribute'''
    },
    {
        'title': 'Hidden Form Field',
        'description': '''HTML forms sometimes contain hidden fields that aren't visible to users.

Challenge: View this page's source code (Ctrl+U or Cmd+U)
Look for hidden form fields that contain a flag value.

Hint: Look for <input type="hidden" ...> tags''',
        'category': 'Web',
        'points': 15,
        'flag': 'AKCTF26{h1dd3n_f13lds}',
        'writeup': '''## Writeup: Hidden Form Fields

**Objective:** Find data in hidden HTML form fields.

**Background:** HTML forms can contain hidden fields that don't display in the UI but are still sent with form submissions.

**Solution:**
1. View page source (Ctrl+U)
2. Search for "hidden"
3. Find: `<input type="hidden" value="AKCTF26{h1dd3n_f13lds}">`
4. Submit the flag

**Why Vulnerable:**
- Not visible but still submitted
- Can contain sensitive data
- Easy to intercept in network traffic

**Best Practice:** Never store sensitive data in hidden fields'''
    },
    {
        'title': 'Query String Secrets',
        'description': '''Sometimes URLs contain sensitive information in query parameters.

Challenge: Visit this special URL to get the flag:
/challenge/web/query_flag?user=admin&level=10&secret=true

The flag will be displayed when you access this endpoint.
Look at the response to find AKCTF26{...}''',
        'category': 'Web',
        'points': 30,
        'flag': 'AKCTF26{qu3ry_str1ng_p0w3r}',
        'writeup': '''## Writeup: Query String Parameters

**Objective:** Exploit URL query parameters to access resources.

**Background:** Query strings (URL parameters) are often used to pass data to web applications.

**Solution:**
1. Visit: `/challenge/web/query_flag?user=admin&level=10&secret=true`
2. Server checks all parameters match
3. Response: AKCTF26{qu3ry_str1ng_p0w3r}

**Format:** `?param1=value1&param2=value2&param3=value3`

**Security Issues:**
- Visible in URL bar
- Logged in server logs
- NOT secure for sensitive data
- Can be manipulated client-side

**Best Practice:** Use POST for sensitive data, validate server-side'''
    },
    {
        'title': 'Local Storage Cache',
        'description': '''Browsers can store data in LocalStorage, which persists between sessions.

Challenge: Open Developer Tools (F12)
Go to: Application > Local Storage > (current domain)
Look for stored CTF data and find the flag key.

Submit what you find in the "flag_data" key!''',
        'category': 'Web',
        'points': 25,
        'flag': 'AKCTF26{l0c4l_st0r4g3}',
        'writeup': '''## Writeup: Browser LocalStorage

**Objective:** Extract data from browser's LocalStorage.

**Background:** LocalStorage is a browser feature that allows websites to store data persistently.

**Solution:**
1. Open DevTools (F12)
2. Chrome: Application → Local Storage → Select domain
3. Firefox: Storage → Local Storage → Select domain
4. Find key: "flag_data"
5. Value: AKCTF26{l0c4l_st0r4g3}

**Using JavaScript:**
```javascript
localStorage.getItem('flag_data')  // AKCTF26{l0c4l_st0r4g3}
```

**LocalStorage Characteristics:**
- Persists until manually deleted
- ~5-10MB per domain
- Accessible via JavaScript
- NOT encrypted

**What NOT to Store:**
- Authentication tokens
- API keys
- Passwords
- Personal information'''
    },
    {
        'title': 'Redirect Chain Master',
        'description': '''Some websites redirect users through multiple pages.

Challenge: Follow the redirect chain:
1. Start at /challenge/web/redirect1
2. Each page will redirect you to the next
3. The final page contains the flag

Note: You may need to use curl or check response headers to see all redirects!''',
        'category': 'Web',
        'points': 35,
        'flag': 'AKCTF26{r3d1r3ct_m4st3r}',
        'writeup': '''## Writeup: HTTP Redirects

**Objective:** Follow HTTP redirect chain to reach the final destination.

**Background:** HTTP redirects (3xx status codes) tell browsers to go to another URL.

**Solution:**
1. Visit: /challenge/web/redirect1
2. Browser follows: redirect1 → redirect2 → redirect3
3. Final page shows: AKCTF26{r3d1r3ct_m4st3r}

**Using curl to see all redirects:**
```bash
curl -L http://localhost:5000/challenge/web/redirect1  # Follow all
curl -v http://localhost:5000/challenge/web/redirect1  # Verbose
```

**HTTP Redirect Codes:**
- 301: Moved Permanently
- 302: Found (temporary)
- 303: See Other
- 307: Temporary Redirect
- 308: Permanent Redirect'''
    },
    {
        'title': 'Meta Refresh Tag',
        'description': '''HTML pages can auto-redirect using meta tags without JavaScript.

Challenge: View the page source and look for a <meta> tag.
It might redirect to a page with the flag, or contain redirect information.

The flag is hidden in this meta refresh mechanism!''',
        'category': 'Web',
        'points': 20,
        'flag': 'AKCTF26{m3t4_r3fr3sh}',
        'writeup': '''## Writeup: HTML Meta Refresh

**Objective:** Understand and follow HTML meta refresh redirects.

**Background:** The <meta http-equiv="refresh"> tag tells browsers to automatically redirect without JavaScript.

**Solution:**
1. Visit: /challenge/web/meta_refresh
2. Browser redirects to: /challenge/web/meta_flag
3. Page shows: AKCTF26{m3t4_r3fr3sh}

**Meta Refresh Syntax:**
```html
<!-- Redirect after 3 seconds -->
<meta http-equiv="refresh" content="3;url=/new-page">

<!-- Immediate redirect -->
<meta http-equiv="refresh" content="0;url=/new-page">
```

**Why Problematic:**
- Not RESTful (should use HTTP redirects)
- Poor UX (flicker)
- Accessibility issues
- Can be used for hidden redirects

**Best Practice:** Use HTTP redirect status codes instead'''
    },
    {
        'title': 'Path Traversal Basics',
        'description': '''Some web applications are vulnerable to path traversal attacks.

Challenge: Try accessing different paths on the server:
- /admin (might show admin flag)
- /secret (might contain secrets)
- /config (configuration files)

See if you can access restricted files or information.
Look for: AKCTF26{...}''',
        'category': 'Web',
        'points': 40,
        'flag': 'AKCTF26{p4th_tr4v3rs4l}',
        'writeup': '''## Writeup: Path Traversal Vulnerability

**Objective:** Access restricted areas by manipulating URL paths.

**Background:** Path traversal is when an application doesn't properly validate user-supplied paths.

**Solution:**
1. Visit: /challenge/web/admin
2. Page displays: AKCTF26{p4th_tr4v3rs4l}
3. Also accessible via: /challenge/web/secret, /challenge/web/config

**Classic Path Traversal:**
```
/file?path=../../../../etc/passwd
/file?path=..%2F..%2F..%2Fetc%2Fpasswd
```

**Prevention:**
```python
# Validate path is in allowed directory
import os
BASE_DIR = '/var/www'
requested = os.path.realpath(path)
if not requested.startswith(BASE_DIR):
    abort(403)
```

**Real-World Impact:**
- Read sensitive files
- Access private data
- Find credentials'''
    },
    {
        'title': 'Case Sensitivity Challenge',
        'description': '''URLs and file systems have different case sensitivity rules.

Challenge: Find the flag by trying different URL cases:
The flag might be at:
- /Flag
- /FLAG
- /flag
- /ChAlLeNgE

Try different combinations to find the correct endpoint!''',
        'category': 'Web',
        'points': 15,
        'flag': 'AKCTF26{c4s3_s3ns1t1v1ty}',
        'writeup': '''## Writeup: Case Sensitivity in URLs

**Objective:** Exploit case sensitivity in URL routing.

**Background:** Different servers handle URL case differently. Linux is case-sensitive, Windows is not.

**Solution:**
1. Visit: /challenge/web/casesensitive
2. Works with any case: /CaseSensitive, /CASESENSITIVE, etc.

**Case Sensitivity by Server:**
- Apache on Linux: YES
- Apache on Windows: NO
- Nginx on Linux: YES
- IIS on Windows: NO

**Security Bypass Example:**
- Blocked: /admin
- Allowed: /Admin (on Windows server)

**Best Practice:**
- Normalize paths to lowercase
- Apply security rules to normalized path'''
    },
    {
        'title': 'SQL Injection Basics',
        'description': '''Test your SQL knowledge!

Challenge: A simple database has two users:
- admin:password123
- user:simplepass

If you can "hack" the login without knowing the password, you can retrieve the flag.
The admin password hint: It contains "admin" and a number.

Flag format: AKCTF26{password}''',
        'category': 'Web',
        'points': 100,
        'flag': 'AKCTF26{admin123}',
        'writeup': '''## Writeup: SQL Injection Basics

**Objective:** Exploit SQL injection to bypass authentication.

**Background:** SQL Injection occurs when user input is directly concatenated into SQL queries.

**Solution:**
The admin password is: admin123

**SQL Injection Technique:**
```
Submit: ' OR '1'='1
Query becomes: WHERE password = '' OR '1'='1'
Result: Always true, bypasses authentication
```

**Vulnerable Code Example:**
```python
# NEVER do this!
query = f"SELECT * FROM users WHERE password='{password}'"
db.execute(query)
```

**Prevention:**
- Use parameterized queries
- Never concatenate user input
- Use ORM frameworks
- Validate all input

**Secure Code:**
```python
query = "SELECT * FROM users WHERE password=?"
db.execute(query, (password,))
```'''
    },
]

def add_sample_challenges():
    """Add sample challenges to the database"""
    app = create_app()
    with app.app_context():
        print("\n" + "="*60)
        print("📚 ADDING CHALLENGES ORGANIZED BY CATEGORY")
        print("="*60)
        
        # Group and display challenges by category
        categories = {}
        for challenge_data in SAMPLE_CHALLENGES:
            cat = challenge_data['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(challenge_data)
        
        # Add challenges in category order
        category_order = ['General', 'Crypto', 'Web']
        total_added = 0
        
        for category in category_order:
            if category in categories:
                count = len(categories[category])
                print(f"\n📁 {category.upper()} CHALLENGES ({count}):")
                print("-" * 60)
                
                for idx, challenge_data in enumerate(categories[category], 1):
                    existing = Challenge.query.filter_by(title=challenge_data['title']).first()
                    if existing:
                        print(f"  {idx}. ⚠  {challenge_data['title']} (exists)")
                        continue
                    
                    challenge = Challenge(**challenge_data)
                    db.session.add(challenge)
                    total_added += 1
                    print(f"  {idx}. ✓ {challenge_data['title']}")
                    print(f"     └─ {challenge_data['points']:3d} pts | {challenge_data['category']}")
        
        db.session.commit()
        print(f"\n{'='*60}")
        print(f"✅ SUCCESS! Added {total_added} challenges")
        print("="*60)
        print(f"\n📊 CHALLENGE BREAKDOWN:")
        for category in category_order:
            if category in categories:
                count = len(categories[category])
                total_points = sum(c['points'] for c in categories[category])
                print(f"  • {category:8s}: {count:2d} challenges ({total_points:3d} total points)")
        
        print(f"\n💾 DOWNLOAD RESOURCES:")
        print(f"  • All challenges include detailed writeups")
        print(f"  • Access writeups with admin password")
        print(f"  • Challenges organized by difficulty")
        
        print(f"\n🚀 NEXT STEPS:")
        print(f"  1. Refresh the platform")
        print(f"  2. View Dashboard to see sorted challenges")
        print(f"  3. Click challenges to view writeups")
        print(f"  4. Download challenge resources")

if __name__ == '__main__':
    add_sample_challenges()
