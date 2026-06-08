"""
delete_migrations.py
====================
Double-click this file OR run:  python delete_migrations.py
Place this file next to manage.py (inside eye_drishti_optical/)

⚠️  WARNING: This deletes ALL migration files inside optical/migrations/
    (except __init__.py) AND clears all __pycache__ folders.

USE THIS WHEN:
  - Migrations are conflicted / broken and you want a fresh start
  - You get errors like "InconsistentMigrationHistory"
  - You want to reset the database completely

STEPS THIS SCRIPT RUNS:
  1. Deletes optical/migrations/00*.py files
  2. Deletes all __pycache__ folders
  3. Deletes db.sqlite3 (optional — you choose)
  4. Runs makemigrations + migrate fresh
"""

import os
import sys
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
MANAGE = os.path.join(HERE, 'manage.py')
MIGRATIONS_DIR = os.path.join(HERE, 'optical', 'migrations')
DB_FILE = os.path.join(HERE, 'db.sqlite3')
PY = sys.executable

if not os.path.exists(MANAGE):
    print("❌  ERROR: manage.py not found. Place this script next to manage.py.")
    input("\nPress Enter to exit...")
    sys.exit(1)

print("="*60)
print("  ⚠️   Eye Drishti Optical — Migration Reset Tool")
print("="*60)
print("\nThis will DELETE all migration files in optical/migrations/")
print("and all __pycache__ folders in the project.\n")

confirm = input("Type  YES  to continue (anything else = cancel): ").strip()
if confirm != 'YES':
    print("\n❌  Cancelled. No files were deleted.")
    input("Press Enter to exit...")
    sys.exit(0)


# ── 1. Delete migration files (keep __init__.py) ─────────────────────────────
deleted_migrations = []
if os.path.exists(MIGRATIONS_DIR):
    for fname in os.listdir(MIGRATIONS_DIR):
        if fname.startswith('0') and fname.endswith('.py'):
            fpath = os.path.join(MIGRATIONS_DIR, fname)
            os.remove(fpath)
            deleted_migrations.append(fname)
    # Also remove migration .pyc files
    pyc_dir = os.path.join(MIGRATIONS_DIR, '__pycache__')
    if os.path.exists(pyc_dir):
        shutil.rmtree(pyc_dir)
        print(f"🗑️   Deleted: optical/migrations/__pycache__/")

if deleted_migrations:
    for f in deleted_migrations:
        print(f"🗑️   Deleted: optical/migrations/{f}")
else:
    print("ℹ️   No numbered migration files found (already clean).")

print(f"✅  Migration files cleared. {len(deleted_migrations)} file(s) deleted.")


# ── 2. Delete ALL __pycache__ folders in project ─────────────────────────────
pycache_count = 0
for root, dirs, files in os.walk(HERE):
    for d in dirs:
        if d == '__pycache__':
            full = os.path.join(root, d)
            shutil.rmtree(full)
            print(f"🗑️   Deleted: {os.path.relpath(full, HERE)}/")
            pycache_count += 1

print(f"✅  {pycache_count} __pycache__ folder(s) deleted.")


# ── 3. Optionally delete db.sqlite3 ──────────────────────────────────────────
if os.path.exists(DB_FILE):
    del_db = input(
        "\n🗄️   Delete db.sqlite3 too? (Removes all existing data!) [y/N]: "
    ).strip().lower()
    if del_db == 'y':
        os.remove(DB_FILE)
        print("🗑️   Deleted: db.sqlite3")
    else:
        print("ℹ️   db.sqlite3 kept.")
else:
    print("ℹ️   db.sqlite3 not found (nothing to delete).")


# ── 4. Fresh makemigrations + migrate ─────────────────────────────────────────
print("\n" + "─"*60)
print("▶  Running fresh makemigrations optical ...")
r1 = subprocess.run([PY, MANAGE, 'makemigrations', 'optical'], cwd=HERE)

print("\n" + "─"*60)
print("▶  Running migrate ...")
r2 = subprocess.run([PY, MANAGE, 'migrate'], cwd=HERE)

print("\n" + "="*60)
if r1.returncode == 0 and r2.returncode == 0:
    print("✅  All done! Fresh migrations created and applied.")
    print("\n🚀  Run:  python manage.py runserver")
    try:
        su = input("\n🔐  Create superuser now? [y/N]: ").strip().lower()
        if su == 'y':
            subprocess.run([PY, MANAGE, 'createsuperuser'], cwd=HERE)
    except KeyboardInterrupt:
        pass
else:
    print("❌  Something went wrong. Check the output above.")

input("\nPress Enter to exit...")