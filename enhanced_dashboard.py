#!/usr/bin/env python3
"""
Enhanced UK AI Jobs Dashboard with Improved Charts
Better text visibility and more meaningful visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import subprocess
import os
from real_time_data_fetcher import AdzunaJobFetcher

print("="*60)
print("[ENHANCED] UK AI JOBS DASHBOARD")
print("="*60)
print("Improved charts with better visibility and insights")

def create_enhanced_visualizations(df):
    """Create enhanced visualizations with better text visibility"""
    print("[VIZ] Creating enhanced visualizations...")

    # Set style for better visibility
    plt.style.use('default')
    sns.set_palette("Set2")

    # Set default font sizes
    plt.rcParams.update({
        'font.size': 12,
        'axes.titlesize': 16,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 11
    })

    # 1. Top Companies (Enhanced Bar Chart)
    plt.figure(figsize=(14, 8))
    company_counts = df['company'].value_counts().head(15)

    # Create horizontal bar chart for better label visibility
    bars = plt.barh(range(len(company_counts)), company_counts.values,
                    color=plt.cm.viridis(np.linspace(0, 1, len(company_counts))))

    plt.title('Top 15 UK Companies Hiring for AI Positions (LIVE DATA)',
              fontsize=18, fontweight='bold', pad=25)
    plt.xlabel('Number of Active Job Postings', fontsize=14, fontweight='bold')
    plt.ylabel('Companies', fontsize=14, fontweight='bold')
    plt.yticks(range(len(company_counts)), company_counts.index)

    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width + 0.3, bar.get_y() + bar.get_height()/2,
                 f'{int(width)}', ha='left', va='center', fontweight='bold')

    plt.figtext(0.02, 0.02, f"LIVE DATA - Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                fontsize=10, style='italic', color='red')
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig('1_companies_hiring.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Location Distribution (Enhanced with better labels)
    plt.figure(figsize=(14, 8))
    location_counts = df['location'].value_counts().head(12)

    bars = plt.bar(range(len(location_counts)), location_counts.values,
                   color=plt.cm.plasma(np.linspace(0.2, 0.8, len(location_counts))))

    plt.title('Top UK Locations for AI Jobs (LIVE DATA)',
              fontsize=18, fontweight='bold', pad=25)
    plt.xlabel('Locations', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Job Postings', fontsize=14, fontweight='bold')
    plt.xticks(range(len(location_counts)), location_counts.index, rotation=45, ha='right')

    # Add value labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                 f'{int(height)}', ha='center', va='bottom', fontweight='bold')

    plt.figtext(0.02, 0.02, f"LIVE DATA - Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                fontsize=10, style='italic', color='red')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('2_location_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Salary by Experience (Enhanced Box Plot)
    plt.figure(figsize=(12, 8))
    salary_df = df[df['salary_avg'].notna() & (df['salary_avg'] > 0)]

    if len(salary_df) > 0:
        experience_order = ['Entry', 'Mid', 'Senior', 'Lead', 'Principal']
        salary_data = []
        exp_labels = []

        for exp in experience_order:
            salaries = salary_df[salary_df['experience_level'] == exp]['salary_avg'].values
            if len(salaries) > 0:
                salary_data.append(salaries)
                exp_labels.append(f'{exp}\n({len(salaries)} jobs)')

        if salary_data:
            bp = plt.boxplot(salary_data, labels=exp_labels, patch_artist=True,
                           showmeans=True, meanline=True)

            colors = plt.cm.plasma(np.linspace(0.2, 0.8, len(salary_data)))
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)

    plt.title('UK AI Salary Distribution by Experience Level (LIVE DATA)',
              fontsize=18, fontweight='bold', pad=25)
    plt.xlabel('Experience Level', fontsize=14, fontweight='bold')
    plt.ylabel('Salary (GBP)', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)

    # Format y-axis as currency
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'£{x:,.0f}'))

    plt.figtext(0.02, 0.02, f"LIVE DATA - Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                fontsize=10, style='italic', color='red')
    plt.tight_layout()
    plt.savefig('3_salary_by_experience.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 4. Skills Demand (Enhanced with counts)
    plt.figure(figsize=(14, 8))
    skill_counts = {}
    for skills_str in df['required_skills'].dropna():
        if skills_str:
            for skill in str(skills_str).split(', '):
                skill = skill.strip()
                if skill:
                    skill_counts[skill] = skill_counts.get(skill, 0) + 1

    if skill_counts:
        top_skills = dict(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:15])

        # Horizontal bar chart for better label visibility
        bars = plt.barh(range(len(top_skills)), list(top_skills.values()),
                       color=plt.cm.viridis(np.linspace(0, 1, len(top_skills))))

        plt.title('Top 15 Most In-Demand Skills for UK AI Jobs (LIVE DATA)',
                  fontsize=18, fontweight='bold', pad=25)
        plt.xlabel('Number of Job Postings Mentioning Skill', fontsize=14, fontweight='bold')
        plt.ylabel('Skills', fontsize=14, fontweight='bold')
        plt.yticks(range(len(top_skills)), list(top_skills.keys()))

        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                     f'{int(width)}', ha='left', va='center', fontweight='bold')

    plt.figtext(0.02, 0.02, f"LIVE DATA - Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                fontsize=10, style='italic', color='red')
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig('5_required_skills.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 5. Work Arrangements (IMPROVED - Much Better Visibility)
    plt.figure(figsize=(12, 10))
    work_type_counts = df['work_type'].value_counts()

    if len(work_type_counts) > 0:
        # Use better colors and larger text
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        explode = (0.1, 0.05, 0.05)  # Explode first slice

        wedges, texts, autotexts = plt.pie(
            work_type_counts.values,
            labels=work_type_counts.index,
            autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*len(df))} jobs)',
            startangle=90,
            colors=colors[:len(work_type_counts)],
            explode=explode[:len(work_type_counts)] if len(work_type_counts) <= 3 else None,
            textprops={'fontsize': 14, 'fontweight': 'bold'},
            pctdistance=0.85
        )

        # Enhance text visibility
        for text in texts:
            text.set_fontsize(16)
            text.set_fontweight('bold')
            text.set_color('black')

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(12)
            autotext.set_fontweight('bold')
            autotext.set_bbox(dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))

    plt.title('UK Work Arrangement Distribution (LIVE DATA)',
              fontsize=20, fontweight='bold', pad=30)

    # Add a legend with counts
    legend_labels = [f'{wt}: {count} jobs ({count/len(df)*100:.1f}%)'
                     for wt, count in work_type_counts.items()]
    plt.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)

    plt.figtext(0.02, 0.02, f"LIVE DATA - Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                fontsize=10, style='italic', color='red')
    plt.tight_layout()
    plt.savefig('6_work_type.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 6. Job Categories (Enhanced)
    plt.figure(figsize=(12, 10))
    category_counts = df['category'].value_counts()

    if len(category_counts) > 0:
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        explode = tuple(0.05 for _ in range(len(category_counts)))

        wedges, texts, autotexts = plt.pie(
            category_counts.values,
            labels=category_counts.index,
            autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*len(df))} jobs)',
            startangle=90,
            colors=colors[:len(category_counts)],
            explode=explode,
            textprops={'fontsize': 12, 'fontweight': 'bold'},
            pctdistance=0.85
        )

        # Enhance text visibility
        for text in texts:
            text.set_fontsize(14)
            text.set_fontweight('bold')
            text.set_color('black')

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')
            autotext.set_bbox(dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))

    plt.title('UK AI Job Categories Distribution (LIVE DATA)',
              fontsize=20, fontweight='bold', pad=30)

    # Add legend with counts
    legend_labels = [f'{cat}: {count} jobs ({count/len(df)*100:.1f}%)'
                     for cat, count in category_counts.items()]
    plt.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1), fontsize=11)

    plt.figtext(0.02, 0.02, f"LIVE DATA - Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                fontsize=10, style='italic', color='red')
    plt.tight_layout()
    plt.savefig('10_job_categories.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 7. NEW: Salary vs Location Analysis
    plt.figure(figsize=(14, 8))
    salary_location_df = df[df['salary_avg'].notna() & (df['salary_avg'] > 0)]

    if len(salary_location_df) > 0:
        top_locations = salary_location_df['location'].value_counts().head(8).index
        location_salary_data = []
        location_labels = []

        for loc in top_locations:
            salaries = salary_location_df[salary_location_df['location'] == loc]['salary_avg'].values
            if len(salaries) >= 3:  # Only include locations with 3+ jobs
                location_salary_data.append(salaries)
                location_labels.append(f'{loc}\n({len(salaries)} jobs)')

        if location_salary_data:
            bp = plt.boxplot(location_salary_data, labels=location_labels,
                           patch_artist=True, showmeans=True)

            colors = plt.cm.Set3(np.linspace(0, 1, len(location_salary_data)))
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)

    plt.title('Salary Distribution by Top UK Locations (LIVE DATA)',
              fontsize=18, fontweight='bold', pad=25)
    plt.xlabel('Location', fontsize=14, fontweight='bold')
    plt.ylabel('Salary (GBP)', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')

    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'£{x:,.0f}'))

    plt.figtext(0.02, 0.02, f"LIVE DATA - Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                fontsize=10, style='italic', color='red')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('7_salary_by_location.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 8. NEW: Job Posting Timeline
    plt.figure(figsize=(14, 8))
    df_timeline = df.copy()
    df_timeline['posted_date'] = pd.to_datetime(df_timeline['posted_date'])
    df_timeline['posted_day'] = df_timeline['posted_date'].dt.date

    daily_posts = df_timeline['posted_day'].value_counts().sort_index()

    plt.plot(daily_posts.index, daily_posts.values, marker='o', linewidth=3, markersize=8,
             color='#667eea', markerfacecolor='#FF6B6B', markeredgecolor='white', markeredgewidth=2)

    plt.title('Daily AI Job Postings Timeline (LIVE DATA)',
              fontsize=18, fontweight='bold', pad=25)
    plt.xlabel('Date', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Jobs Posted', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)

    # Add trend line
    if len(daily_posts) > 1:
        z = np.polyfit(range(len(daily_posts)), daily_posts.values, 1)
        p = np.poly1d(z)
        plt.plot(daily_posts.index, p(range(len(daily_posts))),
                 "--", alpha=0.8, linewidth=2, color='red', label='Trend')
        plt.legend()

    plt.figtext(0.02, 0.02, f"LIVE DATA - Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                fontsize=10, style='italic', color='red')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('8_posting_timeline.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("[SUCCESS] Enhanced visualizations created!")

def main():
    """Main function to create enhanced dashboard"""

    # Load existing data
    data_file = 'live_uk_ai_jobs.csv'

    if os.path.exists(data_file):
        df = pd.read_csv(data_file)
        print(f"[LOADED] {len(df)} jobs for enhanced visualizations")

        # Create enhanced visualizations
        create_enhanced_visualizations(df)

        # Launch dashboard
        print("\n" + "="*60)
        print("[LAUNCH] STARTING ENHANCED DASHBOARD")
        print("="*60)

        try:
            subprocess.run(["start", "navada_dashboard.html"], shell=True, check=True)
            print("[SUCCESS] NAVADA dashboard launched!")

            print(f"\n[ENHANCED] NEW FEATURES:")
            print(f"   * Better text visibility on all charts")
            print(f"   * Improved Work Arrangement chart with clear labels")
            print(f"   * New Salary by Location analysis")
            print(f"   * New Job Posting Timeline chart")
            print(f"   * Enhanced color schemes and layouts")
            print(f"   * Horizontal bar charts for better readability")

        except Exception as e:
            print(f"[ERROR] Failed to launch: {e}")

    else:
        print("[ERROR] No data file found. Run 'python start_live_dashboard.py' first")

if __name__ == "__main__":
    main()