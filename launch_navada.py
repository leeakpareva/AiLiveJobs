#!/usr/bin/env python3
"""
NAVADA Quick Launch Script
One-click launch for AI Live Jobs Intelligence Platform
"""

import os
import sys
import subprocess
from datetime import datetime

def main():
    """Quick launch NAVADA from AiLiveJobs folder"""

    print("="*70)
    print("NAVADA - AI LIVE JOBS INTELLIGENCE PLATFORM")
    print("="*70)
    print("Advanced UK AI jobs market intelligence with live data")

    # Check if we're in the right directory
    required_files = [
        'navada_dashboard.html',
        'enhanced_navada_launcher.py',
        'real_time_data_fetcher.py',
        '.env'
    ]

    missing_files = [f for f in required_files if not os.path.exists(f)]

    if missing_files:
        print("\nERROR: Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nMake sure you're running this from the AiLiveJobs folder")
        return False

    print("\nAll required files found")

    # Check environment file
    if not os.path.exists('.env'):
        print("\nWARNING: .env file not found")
        print("Please create .env with your API keys:")
        print("   ADZUNA_APP_ID=your_app_id")
        print("   ADZUNA_APP_KEY=your_app_key")
        print("   OPENAI_API_KEY=your_openai_key")
        return False

    # Launch NAVADA
    print("\nLaunching NAVADA...")
    try:
        subprocess.run([sys.executable, 'enhanced_navada_launcher.py'], check=True)
        print("\nNAVADA launched successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nFailed to launch NAVADA: {e}")
        print("\nTroubleshooting:")
        print("   1. Check API credentials in .env file")
        print("   2. Ensure internet connection for live data")
        print("   3. Install dependencies: pip install -r requirements.txt")
        return False
    except FileNotFoundError:
        print("\nPython not found in PATH")
        print("   Please ensure Python is properly installed")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\n\nLaunch cancelled by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        input("Press Enter to exit...")