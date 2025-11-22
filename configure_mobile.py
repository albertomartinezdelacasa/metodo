#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configure Mobile Management System
===================================

This script configures the GitHub username in the mobile management panel
and validates that all required files are in place.

Usage:
    python configure_mobile.py
    python configure_mobile.py --username YOUR_GITHUB_USERNAME
"""

import re
import sys
import subprocess
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def get_git_username():
    """Get GitHub username from git remote URL"""
    try:
        result = subprocess.run(
            ['git', 'config', '--get', 'remote.origin.url'],
            capture_output=True,
            text=True,
            check=True
        )
        url = result.stdout.strip()

        # Parse GitHub URL
        # Example: https://github.com/username/repo.git
        # or git@github.com:username/repo.git

        if 'github.com' in url:
            # HTTPS format
            if url.startswith('https://'):
                match = re.search(r'github\.com[/:]([^/]+)/', url)
            # SSH format
            else:
                match = re.search(r'github\.com:([^/]+)/', url)

            if match:
                return match.group(1)

        return None
    except subprocess.CalledProcessError:
        return None

def update_html_template(username):
    """Update the HTML template with the GitHub username"""
    html_path = Path('templates/index.html')

    if not html_path.exists():
        print(f"❌ Error: {html_path} not found")
        return False

    content = html_path.read_text(encoding='utf-8')

    # Replace TU_USUARIO with the actual username
    updated_content = content.replace('TU_USUARIO', username)

    if updated_content == content:
        print(f"⚠️  Warning: No 'TU_USUARIO' placeholders found in {html_path}")
        print("    This might mean the file was already configured.")
        return True

    html_path.write_text(updated_content, encoding='utf-8')

    # Count replacements
    count = content.count('TU_USUARIO')
    print(f"✅ Updated {count} GitHub username references in templates/index.html")

    return True

def validate_github_files():
    """Validate that all GitHub workflow and template files exist"""
    required_files = [
        '.github/workflows/mobile-commands.yml',
        '.github/ISSUE_TEMPLATE/mobile-run-tests.yml',
        '.github/ISSUE_TEMPLATE/mobile-deploy.yml',
        '.github/ISSUE_TEMPLATE/mobile-backup-db.yml',
        '.github/ISSUE_TEMPLATE/mobile-analyze-code.yml',
        '.github/ISSUE_TEMPLATE/mobile-update-deps.yml',
    ]

    missing = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)

    if missing:
        print("\n❌ Missing required files:")
        for file_path in missing:
            print(f"   - {file_path}")
        return False

    print(f"✅ All {len(required_files)} GitHub workflow files are present")
    return True

def check_git_repo():
    """Check if we're in a git repository"""
    try:
        subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            capture_output=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🔧 Configuring Mobile Management System...\n")

    # Check if we're in a git repo
    if not check_git_repo():
        print("❌ Error: Not a git repository")
        print("   Run 'git init' first or navigate to your git repository")
        sys.exit(1)

    # Get username from command line or git config
    if len(sys.argv) > 1 and sys.argv[1] != '--username':
        username = sys.argv[1]
        print(f"📝 Using username from argument: {username}")
    elif len(sys.argv) > 2 and sys.argv[1] == '--username':
        username = sys.argv[2]
        print(f"📝 Using username from argument: {username}")
    else:
        username = get_git_username()
        if username:
            print(f"📝 Detected GitHub username from git remote: {username}")
        else:
            print("⚠️  Could not detect GitHub username from git remote")
            username = input("Enter your GitHub username: ").strip()

    if not username:
        print("❌ Error: GitHub username is required")
        sys.exit(1)

    print(f"\n🎯 Configuring for GitHub user: {username}\n")

    # Validate files
    print("1️⃣ Validating GitHub workflow files...")
    if not validate_github_files():
        print("\n❌ Configuration failed: Missing required files")
        print("   Make sure you've committed all the GitHub workflow files")
        sys.exit(1)

    # Update HTML template
    print("\n2️⃣ Updating HTML template...")
    if not update_html_template(username):
        print("\n❌ Configuration failed: Could not update template")
        sys.exit(1)

    # Show next steps
    print("\n✅ Configuration completed successfully!\n")
    print("📋 Next Steps:")
    print("   1. Review the changes in templates/index.html")
    print("   2. Commit the changes:")
    print("      git add .")
    print("      git commit -m \"Configure mobile management for GitHub user\"")
    print("   3. Push to GitHub:")
    print("      git push")
    print("   4. Wait 5 minutes for GitHub to index the issue templates")
    print("   5. Open your PWA and test the mobile management features")
    print("\n📖 For detailed instructions, see MOBILE_GUIDE.md\n")

if __name__ == '__main__':
    main()
