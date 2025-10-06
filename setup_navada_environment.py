#!/usr/bin/env python3
"""
NAVADA Environment Setup Script
Creates virtual environment and installs dependencies
"""

import os
import subprocess
import sys
from datetime import datetime

def setup_environment():
    """Set up NAVADA development environment"""

    print("="*70)
    print("NAVADA ENVIRONMENT SETUP")
    print("="*70)
    print("Setting up isolated Python environment for NAVADA project")

    # Check if virtual environment already exists
    if os.path.exists('navada_env'):
        print("[INFO] Virtual environment 'navada_env' already exists")
        choice = input("Do you want to recreate it? (y/n): ").lower()
        if choice == 'y':
            print("[ACTION] Removing existing environment...")
            if os.name == 'nt':  # Windows
                os.system('rmdir /s /q navada_env')
            else:  # Unix/Linux/Mac
                os.system('rm -rf navada_env')
        else:
            print("[SKIP] Using existing environment")
            activate_instructions()
            return

    # Create virtual environment
    print("\n[STEP 1] Creating Python virtual environment...")
    try:
        subprocess.run([sys.executable, '-m', 'venv', 'navada_env'], check=True)
        print("[SUCCESS] Virtual environment 'navada_env' created")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to create virtual environment: {e}")
        return False

    # Install dependencies
    print("\n[STEP 2] Installing NAVADA dependencies...")

    # Determine the correct pip path based on OS
    if os.name == 'nt':  # Windows
        pip_path = os.path.join('navada_env', 'Scripts', 'pip.exe')
        python_path = os.path.join('navada_env', 'Scripts', 'python.exe')
    else:  # Unix/Linux/Mac
        pip_path = os.path.join('navada_env', 'bin', 'pip')
        python_path = os.path.join('navada_env', 'bin', 'python')

    # Install core dependencies
    dependencies = [
        'pandas>=2.0.0',
        'numpy>=1.24.0',
        'matplotlib>=3.6.0',
        'seaborn>=0.12.0',
        'requests>=2.28.0',
        'python-dotenv>=1.0.0',
        'plotly>=5.15.0'
    ]

    try:
        # Upgrade pip first
        subprocess.run([python_path, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)

        # Install dependencies
        for dep in dependencies:
            print(f"   Installing {dep}...")
            subprocess.run([pip_path, 'install', dep], check=True, capture_output=True)

        print("[SUCCESS] All dependencies installed")

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to install dependencies: {e}")
        return False

    # Create activation script
    print("\n[STEP 3] Creating activation scripts...")
    create_activation_scripts()

    # Show summary
    print("\n" + "="*70)
    print("SETUP COMPLETE")
    print("="*70)
    print("NAVADA environment successfully created!")
    print("\nTo activate the environment:")

    if os.name == 'nt':  # Windows
        print("   navada_env\\Scripts\\activate")
    else:  # Unix/Linux/Mac
        print("   source navada_env/bin/activate")

    print("\nOr use the provided scripts:")
    print("   python activate_navada.py")
    print("   python run_navada.py")

    print("\nProject files:")
    print("   enhanced_navada_launcher.py - Main launcher")
    print("   navada_dashboard.html - Enhanced dashboard")
    print("   enhanced_adzuna_fetcher.py - Advanced analytics")
    print("   requirements.txt - Dependencies list")

    activate_instructions()
    return True

def create_activation_scripts():
    """Create helper activation scripts"""

    # Windows activation script
    if os.name == 'nt':
        activate_script = """@echo off
echo Activating NAVADA environment...
call navada_env\\Scripts\\activate
echo NAVADA environment activated!
echo.
echo To run NAVADA:
echo   python enhanced_navada_launcher.py
echo.
cmd /k
"""
        with open('activate_navada.bat', 'w') as f:
            f.write(activate_script)

        run_script = """@echo off
echo Starting NAVADA...
call navada_env\\Scripts\\activate
python enhanced_navada_launcher.py
pause
"""
        with open('run_navada.bat', 'w') as f:
            f.write(run_script)

    # Cross-platform Python activation script
    python_activate = """#!/usr/bin/env python3
import os
import subprocess
import sys

if os.name == 'nt':  # Windows
    activate_path = os.path.join('navada_env', 'Scripts', 'activate.bat')
    subprocess.run(f'cmd /k "{activate_path}"', shell=True)
else:  # Unix/Linux/Mac
    activate_path = os.path.join('navada_env', 'bin', 'activate')
    subprocess.run(f'source {activate_path} && bash', shell=True)
"""

    with open('activate_navada.py', 'w') as f:
        f.write(python_activate)

    # Run NAVADA script
    python_run = """#!/usr/bin/env python3
import os
import subprocess
import sys

print("Starting NAVADA AI Jobs Intelligence Platform...")

if os.name == 'nt':  # Windows
    python_path = os.path.join('navada_env', 'Scripts', 'python.exe')
else:  # Unix/Linux/Mac
    python_path = os.path.join('navada_env', 'bin', 'python')

subprocess.run([python_path, 'enhanced_navada_launcher.py'])
"""

    with open('run_navada.py', 'w') as f:
        f.write(python_run)

    print("[SUCCESS] Activation scripts created")

def activate_instructions():
    """Show activation instructions"""
    print("\n" + "="*70)
    print("QUICK START GUIDE")
    print("="*70)
    print("1. Activate environment:")
    if os.name == 'nt':
        print("   navada_env\\Scripts\\activate")
    else:
        print("   source navada_env/bin/activate")

    print("\n2. Run NAVADA:")
    print("   python enhanced_navada_launcher.py")

    print("\n3. Or use shortcuts:")
    print("   python run_navada.py")

    print("\n4. Check .env file has your API keys:")
    print("   ADZUNA_APP_ID=your_app_id")
    print("   ADZUNA_APP_KEY=your_app_key")
    print("   OPENAI_API_KEY=your_openai_key")

if __name__ == "__main__":
    try:
        setup_environment()
    except KeyboardInterrupt:
        print("\n[CANCELLED] Setup cancelled by user")
    except Exception as e:
        print(f"\n[ERROR] Setup failed: {e}")
        print("Please check your Python installation and try again")