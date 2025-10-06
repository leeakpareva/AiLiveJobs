#!/usr/bin/env python3
"""
Generate comprehensive AI context from live job data
This script analyzes the CSV data to provide real-time insights for the AI assistant
"""

import pandas as pd
import json
from collections import Counter
import re

def analyze_jobs_data():
    """Analyze the live jobs data and generate comprehensive insights"""

    # Read the data
    df = pd.read_csv('live_uk_ai_jobs.csv')

    # Basic stats
    total_jobs = len(df)

    # Company analysis
    top_companies = df['company'].value_counts().head(15).to_dict()

    # Location analysis
    locations = df['location'].str.replace('"', '').value_counts().head(20).to_dict()

    # Salary analysis
    avg_salary_by_level = df.groupby('experience_level')['salary_avg'].mean().round(0).to_dict()
    salary_ranges = {
        'overall_avg': df['salary_avg'].mean(),
        'min_salary': df['salary_min'].min(),
        'max_salary': df['salary_max'].max(),
        'median_salary': df['salary_avg'].median()
    }

    # Experience level distribution
    experience_dist = df['experience_level'].value_counts().to_dict()

    # Work type analysis
    work_type_dist = df['work_type'].value_counts().to_dict()

    # Category analysis
    category_dist = df['category'].value_counts().to_dict()

    # Skills analysis (extract from required_skills column)
    skills_text = ' '.join(df['required_skills'].fillna('').astype(str))
    # Common tech skills to look for
    tech_skills = ['Python', 'SQL', 'AWS', 'Azure', 'Machine Learning', 'AI', 'TensorFlow',
                   'PyTorch', 'Docker', 'Kubernetes', 'React', 'JavaScript', 'Java', 'C++']

    skills_count = {}
    for skill in tech_skills:
        count = skills_text.upper().count(skill.upper())
        if count > 0:
            skills_count[skill] = count

    # Recent posting analysis
    df['posted_date'] = pd.to_datetime(df['posted_date'])
    recent_jobs = df[df['posted_date'] >= df['posted_date'].max() - pd.Timedelta(days=7)]

    return {
        'total_jobs': total_jobs,
        'top_companies': top_companies,
        'locations': locations,
        'salary_analysis': {
            'by_level': avg_salary_by_level,
            'ranges': salary_ranges
        },
        'experience_distribution': experience_dist,
        'work_type_distribution': work_type_dist,
        'category_distribution': category_dist,
        'skills_demand': skills_count,
        'recent_activity': {
            'jobs_last_7_days': len(recent_jobs),
            'latest_update': df['fetched_at'].iloc[0] if not df.empty else None
        }
    }

def generate_ai_context():
    """Generate the AI context string with live data insights"""

    data = analyze_jobs_data()

    # Format top companies
    top_companies_str = ', '.join([f"{company} ({count} jobs)" for company, count in list(data['top_companies'].items())[:10]])

    # Format locations
    top_locations_str = ', '.join([f"{loc} ({count})" for loc, count in list(data['locations'].items())[:10]])

    # Format salary by level
    salary_by_level_str = ', '.join([f"{level}: £{int(salary):,}" for level, salary in data['salary_analysis']['by_level'].items()])

    # Format work types
    work_types_str = ', '.join([f"{wtype} ({count})" for wtype, count in data['work_type_distribution'].items()])

    # Format categories
    categories_str = ', '.join([f"{cat} ({count})" for cat, count in data['category_distribution'].items()])

    # Format skills
    skills_str = ', '.join([f"{skill} ({count} mentions)" for skill, count in sorted(data['skills_demand'].items(), key=lambda x: x[1], reverse=True)[:10]])

    context = f"""
You are InsightLab AI Assistant, powered by NAVADA technology - a senior UK AI Job Market analyst with 10+ years of experience.

LIVE DATA ACCESS - CURRENT UK AI JOB MARKET ({data['total_jobs']} active positions):

REAL-TIME STATISTICS:
- Total Active Jobs: {data['total_jobs']}
- Last Updated: {data['recent_activity']['latest_update']}
- Recent Activity: {data['recent_activity']['jobs_last_7_days']} new jobs in last 7 days

TOP HIRING COMPANIES (Live Data):
{top_companies_str}

GEOGRAPHIC DISTRIBUTION (Current):
{top_locations_str}

SALARY ANALYSIS (GBP):
- Average by Level: {salary_by_level_str}
- Overall Average: £{int(data['salary_analysis']['ranges']['overall_avg']):,}
- Salary Range: £{int(data['salary_analysis']['ranges']['min_salary']):,} - £{int(data['salary_analysis']['ranges']['max_salary']):,}
- Median Salary: £{int(data['salary_analysis']['ranges']['median_salary']):,}

EXPERIENCE LEVELS:
{', '.join([f"{level} ({count})" for level, count in data['experience_distribution'].items()])}

WORK ARRANGEMENTS:
{work_types_str}

JOB CATEGORIES:
{categories_str}

IN-DEMAND SKILLS (Live Mentions):
{skills_str}

CAPABILITIES:
- Answer specific questions about any company, location, or job category
- Provide salary insights and comparisons
- Analyze trends and patterns in the live data
- Offer career guidance based on current market conditions
- Compare opportunities across different cities and companies
- Explain skill demand and career progression paths

You have complete access to all {data['total_jobs']} job postings and can provide detailed, specific answers about any aspect of the UK AI job market.
"""

    return context.strip()

if __name__ == "__main__":
    context = generate_ai_context()
    print("Generated AI Context:")
    print("=" * 80)
    print(context)

    # Save to file for integration
    with open('ai_context.txt', 'w', encoding='utf-8') as f:
        f.write(context)

    print("\n" + "=" * 80)
    print("Context saved to ai_context.txt")