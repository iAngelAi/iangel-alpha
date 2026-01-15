import os
from dotenv import load_dotenv

print("--- DEBUG ENV ---")
# 1. Avant load_dotenv
print(f"OS Environ 'ANTHROPIC_MODEL': {os.environ.get('ANTHROPIC_MODEL')}")

# 2. Après load_dotenv
load_dotenv()
print(f"DotEnv 'ANTHROPIC_MODEL': {os.environ.get('ANTHROPIC_MODEL')}")

# 3. Vérification physique
try:
    with open(".env", "r") as f:
        content = f.read()
        print(f"\nContenu physique .env (grep MODEL):\n{[line for line in content.splitlines() if 'MODEL' in line]}")
except Exception as e:
    print(f"\nImpossible de lire .env: {e}")
