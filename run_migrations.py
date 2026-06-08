"""
run_migrations.py
=================
Double-click this file OR run:  python run_migrations.py
Place this file next to manage.py (inside eye_drishti_optical/)

What it does:
  1. makemigrations optical  — detects model changes
  2. migrate                 — applies all pending migrations
  3. Offers to create a superuser if none exists
"""

import subprocess
import sys
import os

# ── Make sure we're running from the project root ────────────────────────────
HERE = os.path.dirname(os.path.abspath(__file__))
MANAGE = os.path.join(HERE, 'manage.py')

if not os.path.exists(MANAGE):
    print("❌  ERROR: manage.py not found in this folder.")
    print("   Move run_migrations.py next to manage.py and try again.")
    input("\nPress Enter to exit...")
    sys.exit(1)

PY = sys.executable   # same Python interpreter that's running this script


def run(cmd, label):
    print(f"\n{'─'*55}")
    print(f"▶  {label}")
    print(f"   Command: {' '.join(cmd)}")
    print(f"{'─'*55}")
    result = subprocess.run(cmd, cwd=HERE)
    if result.returncode != 0:
        print(f"\n❌  '{label}' failed (exit code {result.returncode}).")
        input("\nPress Enter to exit...")
        sys.exit(result.returncode)
    print(f"✅  {label} — done!")


# ── Step 1: makemigrations ────────────────────────────────────────────────────
run([PY, MANAGE, 'makemigrations', 'optical'], 'makemigrations optical')

# ── Step 2: migrate ───────────────────────────────────────────────────────────
run([PY, MANAGE, 'migrate'], 'migrate')

# ── Step 3: offer superuser creation ─────────────────────────────────────────
print("\n" + "="*55)
print("✅  All migrations applied successfully!")
print("="*55)

try:
    answer = input("\n🔐  Do you want to create a superuser (admin) now? [y/N]: ").strip().lower()
    if answer == 'y':
        subprocess.run([PY, MANAGE, 'createsuperuser'], cwd=HERE)
    else:
        print("   Skipped. Run:  python manage.py createsuperuser  anytime.")
except KeyboardInterrupt:
    pass

print("\n🚀  All done! Now run:  python manage.py runserver")
input("Press Enter to exit...")