#!/usr/bin/env python
"""Update localhost URLs to internal blueprint paths"""

import sys

file_path = r'c:\Users\megat\Downloads\akctf26 workshop\ctf-platform\sample_challenges.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    "'challenge_url': 'http://localhost:8082/headers'": "'challenge_url': '/web-challenges/headers'",
    "'challenge_url': 'http://localhost:8083/js-challenge'": "'challenge_url': '/web-challenges/js-challenge'",
    "'challenge_url': 'http://localhost:8084/cookie-challenge'": "'challenge_url': '/web-challenges/cookie-challenge'",
    "'challenge_url': 'http://localhost:8085/challenge?user=admin&level=10&secret=true'": "'challenge_url': '/web-challenges/challenge?user=admin&level=10&secret=true'",
    "'challenge_url': 'http://localhost:8086/storage'": "'challenge_url': '/web-challenges/storage'",
    "'challenge_url': 'http://localhost:8087/redirect1'": "'challenge_url': '/web-challenges/redirect1'",
    "'challenge_url': 'http://localhost:8088/meta-challenge'": "'challenge_url': '/web-challenges/meta-challenge'",
    "'challenge_url': 'http://localhost:8089'": "'challenge_url': '/web-challenges/file?path=secret.txt'",
    "'challenge_url': 'http://localhost:8090'": "'challenge_url': '/web-challenges/case/flag'",
    "'challenge_url': 'http://localhost:8091/login'": "'challenge_url': '/web-challenges/login'",
}

count = 0
for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        count += 1
        print(f"✓ Updated: {old[:50]}...")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\n✅ Updated {count} challenge URLs to internal paths!')
