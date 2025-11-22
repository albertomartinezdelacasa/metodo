#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pre-Deploy Diagnostic Script
=============================

Verifica que el proyecto esté listo para desplegar en Render.com
"""

import os
import sys
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def check_file_exists(filepath, required=True):
    """Check if file exists"""
    exists = Path(filepath).exists()
    symbol = "✅" if exists else ("❌" if required else "⚠️")
    status = "OK" if exists else ("REQUIRED" if required else "OPTIONAL")
    print(f"  {symbol} {filepath}: {status}")
    return exists


def check_requirements():
    """Check requirements.txt"""
    print("\n📦 Checking dependencies...")

    if not check_file_exists('requirements.txt'):
        return False

    with open('requirements.txt', 'r') as f:
        content = f.read()

    required_packages = [
        'Flask',
        'gunicorn',
        'supabase',
        'google-generativeai',
        'Flask-CORS'
    ]

    missing = []
    for pkg in required_packages:
        if pkg.lower() in content.lower():
            print(f"  ✅ {pkg}")
        else:
            print(f"  ❌ {pkg} - MISSING")
            missing.append(pkg)

    return len(missing) == 0


def check_env_template():
    """Check .env.example exists"""
    print("\n🔑 Checking environment configuration...")

    if not check_file_exists('.env.example'):
        print("  ⚠️  .env.example not found (optional)")

    if check_file_exists('.env'):
        print("  ✅ .env found (for local development)")

        # Check required env vars
        from dotenv import load_dotenv
        load_dotenv()

        required_vars = [
            'SUPABASE_URL',
            'SUPABASE_KEY',
            'GEMINI_API_KEY'
        ]

        print("\n  Environment variables in .env:")
        all_present = True
        for var in required_vars:
            value = os.getenv(var)
            if value:
                # Show first 20 chars only
                preview = value[:20] + "..." if len(value) > 20 else value
                print(f"    ✅ {var} = {preview}")
            else:
                print(f"    ❌ {var} - NOT SET")
                all_present = False

        return all_present
    else:
        print("  ⚠️  .env not found (will use Render env vars)")
        return True


def check_project_structure():
    """Check project structure"""
    print("\n📁 Checking project structure...")

    required_files = [
        'src/__init__.py',
        'src/app.py',
        'src/config.py',
        'templates/index.html',
        'static/js/app.js',
        'static/css/style.css'
    ]

    all_exist = True
    for file in required_files:
        if not check_file_exists(file):
            all_exist = False

    return all_exist


def check_render_config():
    """Check Render configuration"""
    print("\n🚀 Checking Render deployment files...")

    has_procfile = check_file_exists('Procfile', required=False)
    has_render_yaml = check_file_exists('render.yaml', required=False)
    has_runtime = check_file_exists('runtime.txt', required=False)

    if not has_procfile and not has_render_yaml:
        print("  ⚠️  Neither Procfile nor render.yaml found")
        print("  💡 Tip: Create render.yaml or configure manually in Render Dashboard")

    if has_runtime:
        with open('runtime.txt', 'r') as f:
            version = f.read().strip()
        print(f"  📌 Python version: {version}")

        # Check if version is valid
        if version.startswith('python-3.11') or version.startswith('python-3.12'):
            print(f"  ✅ Version is compatible with Render")
        else:
            print(f"  ⚠️  Version might not be supported. Recommended: python-3.11.9")

    return True


def check_imports():
    """Check if app can be imported"""
    print("\n🐍 Checking if app can be imported...")

    try:
        # Try to import the app
        sys.path.insert(0, str(Path.cwd()))
        from src.app import app
        print("  ✅ src.app:app imported successfully")

        # Check if create_app exists
        from src.app import create_app
        print("  ✅ create_app function found")

        return True
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        print("  💡 This will cause deployment to fail!")
        return False
    except Exception as e:
        print(f"  ⚠️  Warning: {e}")
        print("  💡 Check your environment variables")
        return True  # May work in Render with proper env vars


def check_git_status():
    """Check git status"""
    print("\n🌳 Checking git status...")

    import subprocess

    try:
        # Check if in git repo
        result = subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            capture_output=True,
            check=True
        )
        print("  ✅ Git repository initialized")

        # Check remote
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            remote_url = result.stdout.strip()
            print(f"  ✅ Git remote: {remote_url}")

            if 'github.com' in remote_url:
                print("  ✅ GitHub remote detected (ready for Render)")
            else:
                print("  ⚠️  Remote is not GitHub (Render prefers GitHub)")
        else:
            print("  ⚠️  No git remote configured")
            print("  💡 Add remote: git remote add origin <url>")

        # Check for uncommitted changes
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True
        )

        if result.stdout.strip():
            print("  ⚠️  You have uncommitted changes")
            print("  💡 Commit and push before deploying to Render")
        else:
            print("  ✅ No uncommitted changes")

        return True

    except subprocess.CalledProcessError:
        print("  ❌ Not a git repository")
        return False


def print_render_checklist():
    """Print manual checklist for Render Dashboard"""
    print("\n" + "="*60)
    print("📋 RENDER.COM DEPLOYMENT CHECKLIST")
    print("="*60)

    print("\n1️⃣ Create Web Service:")
    print("   • New → Web Service")
    print("   • Connect GitHub repository")
    print("   • Select 'metodo' repository")

    print("\n2️⃣ Configuration:")
    print("   • Name: metodo-comedia")
    print("   • Environment: Python 3")
    print("   • Build Command: pip install -r requirements.txt")
    print("   • Start Command: gunicorn src.app:app --bind 0.0.0.0:$PORT")

    print("\n3️⃣ Environment Variables (REQUIRED):")
    print("   Add these in Render Dashboard → Environment:")
    print("   ┌─────────────────────────────────────────────┐")
    print("   │ SUPABASE_URL = https://xxx.supabase.co     │")
    print("   │ SUPABASE_KEY = eyJhbGci...                 │")
    print("   │ SUPABASE_SERVICE_KEY = eyJhbGci...         │")
    print("   │ GEMINI_API_KEY = AIzaSy...                 │")
    print("   │ FLASK_ENV = production                     │")
    print("   │ FLASK_DEBUG = False                        │")
    print("   └─────────────────────────────────────────────┘")

    print("\n4️⃣ Optional Variables:")
    print("   ┌─────────────────────────────────────────────┐")
    print("   │ TODOIST_TOKEN = your_token                  │")
    print("   │ TODOIST_PROJECT_ID = 2362882414             │")
    print("   └─────────────────────────────────────────────┘")

    print("\n5️⃣ Deploy:")
    print("   • Click 'Create Web Service'")
    print("   • Wait 5-10 minutes for first deploy")
    print("   • Check logs for errors")

    print("\n6️⃣ Verify Deployment:")
    print("   • Visit: https://your-app.onrender.com/health")
    print("   • Should return: {\"status\": \"healthy\", ...}")

    print("\n" + "="*60)


def main():
    print("="*60)
    print("🔍 PRE-DEPLOY DIAGNOSTIC")
    print("="*60)
    print("Checking if your project is ready for Render.com deployment...\n")

    # Run all checks
    checks = [
        ("Requirements", check_requirements),
        ("Project Structure", check_project_structure),
        ("Render Config", check_render_config),
        ("Environment", check_env_template),
        ("Python Imports", check_imports),
        ("Git Status", check_git_status)
    ]

    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"  ❌ Error during {name} check: {e}")
            results[name] = False

    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for name, result in results.items():
        symbol = "✅" if result else "❌"
        print(f"{symbol} {name}")

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n🎉 Your project looks ready to deploy!")
        print_render_checklist()
    else:
        print("\n⚠️  Fix the issues above before deploying")
        print("\n💡 Tips:")
        print("   • Install missing dependencies: pip install <package>")
        print("   • Add to requirements.txt: pip freeze > requirements.txt")
        print("   • Check RENDER_TROUBLESHOOTING.md for detailed help")

    print("\n" + "="*60)


if __name__ == '__main__':
    main()
