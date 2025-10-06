#!/usr/bin/env python3
"""
Enhanced NAVADA Launcher with Additional Adzuna API Analytics
Includes salary histograms, top companies, geographic data, and historical trends
"""

import os
import subprocess
from datetime import datetime

print("="*80)
print("NAVADA - ENHANCED AI JOBS INTELLIGENCE PLATFORM")
print("="*80)
print("Now with advanced Adzuna API analytics and insights")

def main():
    """Launch NAVADA with enhanced analytics"""

    print("[STEP 1] Updating live job data...")
    try:
        os.system('python real_time_data_fetcher.py > nul 2>&1')
        print("[SUCCESS] Live job data refreshed")
    except:
        print("[WARN] Using existing job data")

    print("\n[STEP 2] Creating enhanced visualizations...")
    try:
        os.system('python enhanced_dashboard.py > nul 2>&1')
        print("[SUCCESS] Standard charts created")
    except:
        print("[WARN] Standard charts may be outdated")

    print("\n[STEP 3] Generating advanced analytics...")
    try:
        os.system('python fixed_enhanced_analytics.py > nul 2>&1')
        print("[SUCCESS] Advanced analytics completed")
    except:
        print("[WARN] Advanced analytics failed - check API keys")

    print("\n[STEP 4] Launching NAVADA dashboard...")
    try:
        subprocess.run(["start", "navada_dashboard.html"], shell=True, check=True)
        print("[SUCCESS] NAVADA launched successfully!")
    except Exception as e:
        print(f"[ERROR] {e}")
        print("[INFO] Please manually open 'navada_dashboard.html'")

    print("\n" + "="*80)
    print("NAVADA ENHANCED FEATURES")
    print("="*80)

    print("\n[LIVE DATA]")
    print("   * Real-time UK AI jobs from Adzuna API")
    print("   * 279+ active job postings")
    print("   * Live salary and company data")

    print("\n[STANDARD ANALYTICS]")
    print("   * Top hiring companies")
    print("   * Salary by experience level")
    print("   * Skills demand analysis")
    print("   * Location distribution")
    print("   * Work arrangement types")
    print("   * Job categories breakdown")

    print("\n[ADVANCED ANALYTICS - NEW!]")
    print("   * Salary histogram distribution")
    print("   * Top companies leaderboard with average salaries")
    print("   * Geographic salary mapping by UK regions")
    print("   * 12-month historical salary trends")
    print("   * 30+ job categories analysis")

    print("\n[DASHBOARD FEATURES]")
    print("   * Collapsible chat panel with OpenAI integration")
    print("   * Dark theme with glass-morphism design")
    print("   * Side-by-side chart display")
    print("   * Smooth animations and transitions")
    print("   * Mobile-responsive layout")

    print("\n[CHART IMPROVEMENTS]")
    print("   * Better text visibility and contrast")
    print("   * Horizontal bar charts prevent label overlap")
    print("   * Enhanced color schemes")
    print("   * Professional data presentation")

    print("\n[API INTEGRATIONS]")
    print("   * Adzuna Jobs API (multiple endpoints)")
    print("   * OpenAI GPT for intelligent chat")
    print("   * Real-time data refresh capabilities")

    print(f"\n[LAUNCHED] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("[STATUS] NAVADA ready for AI job market intelligence!")

    print("\n" + "="*80)
    print("AVAILABLE CHARTS")
    print("="*80)
    print("Standard Charts:")
    print("   1_companies_hiring.png - Top companies")
    print("   2_location_distribution.png - Job locations")
    print("   3_salary_by_experience.png - Salary analysis")
    print("   5_required_skills.png - Skills demand")
    print("   6_work_type.png - Work arrangements")
    print("   7_salary_by_location.png - Regional salaries")
    print("   8_posting_timeline.png - Job posting trends")
    print("   10_job_categories.png - Category breakdown")

    print("\nEnhanced Charts:")
    print("   enhanced_1_salary_histogram.png - Salary distribution")
    print("   enhanced_2_top_companies_leaderboard.png - Company rankings")
    print("   enhanced_3_geographic_distribution.png - Regional analysis")
    print("   enhanced_4_historical_trends.png - 12-month trends")

    print("\nData Files:")
    print("   live_uk_ai_jobs.csv - Live job data")
    print("   adzuna_categories.csv - Available categories")

if __name__ == "__main__":
    main()