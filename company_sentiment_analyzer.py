#!/usr/bin/env python3
"""
Company Sentiment Analysis Dashboard
Analyzes sentiment of job descriptions to gauge company perception
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import re
from collections import defaultdict

# Simple sentiment analysis using keyword scoring
POSITIVE_KEYWORDS = [
    'innovative', 'exciting', 'cutting-edge', 'leading', 'excellent', 'dynamic',
    'collaborative', 'flexible', 'growth', 'opportunity', 'benefits', 'competitive',
    'rewarding', 'supportive', 'progressive', 'modern', 'world-class', 'prestigious',
    'ambitious', 'thriving', 'successful', 'award-winning', 'industry-leading',
    'state-of-the-art', 'fast-growing', 'vibrant', 'passionate', 'creative',
    'empowering', 'inclusive', 'diverse', 'agile', 'forward-thinking'
]

NEGATIVE_KEYWORDS = [
    'demanding', 'pressure', 'tight deadlines', 'stressful', 'challenging',
    'difficult', 'complex', 'intensive', 'fast-paced', 'high-pressure',
    'strict', 'rigid', 'demanding schedule', 'overtime', 'weekend work'
]

ENGAGEMENT_KEYWORDS = [
    'team', 'collaboration', 'partnership', 'community', 'culture',
    'environment', 'work-life balance', 'remote', 'hybrid', 'training',
    'development', 'career', 'mentorship', 'learning', 'education'
]

def analyze_text_sentiment(text):
    """Analyze sentiment of text using keyword scoring"""
    if not text:
        return {'positive': 0, 'negative': 0, 'engagement': 0, 'score': 0}

    text_lower = text.lower()

    positive_count = sum(1 for word in POSITIVE_KEYWORDS if word in text_lower)
    negative_count = sum(1 for word in NEGATIVE_KEYWORDS if word in text_lower)
    engagement_count = sum(1 for word in ENGAGEMENT_KEYWORDS if word in text_lower)

    # Calculate overall sentiment score (-1 to 1)
    total_words = len(text.split())
    if total_words == 0:
        sentiment_score = 0
    else:
        sentiment_score = (positive_count - negative_count) / max(total_words / 50, 1)
        sentiment_score = max(-1, min(1, sentiment_score))

    return {
        'positive': positive_count,
        'negative': negative_count,
        'engagement': engagement_count,
        'score': sentiment_score
    }

def create_company_sentiment_analysis():
    """Create comprehensive company sentiment analysis"""

    print("="*70)
    print("COMPANY SENTIMENT ANALYSIS")
    print("="*70)

    # Load job data
    df = pd.read_csv('live_uk_ai_jobs.csv')
    print(f"[DATA] Analyzing {len(df)} job listings for company sentiment")

    # Analyze sentiment for each job
    sentiment_data = []

    for _, job in df.iterrows():
        description = str(job.get('description', ''))
        sentiment = analyze_text_sentiment(description)

        sentiment_data.append({
            'company': job.get('company', ''),
            'title': job.get('title', ''),
            'location': job.get('location', ''),
            'salary_avg': job.get('salary_avg', 0),
            'work_type': job.get('work_type', ''),
            'positive_score': sentiment['positive'],
            'negative_score': sentiment['negative'],
            'engagement_score': sentiment['engagement'],
            'overall_sentiment': sentiment['score']
        })

    sentiment_df = pd.DataFrame(sentiment_data)

    # Aggregate by company
    company_sentiment = sentiment_df.groupby('company').agg({
        'positive_score': 'mean',
        'negative_score': 'mean',
        'engagement_score': 'mean',
        'overall_sentiment': 'mean',
        'title': 'count',
        'salary_avg': 'mean'
    }).reset_index()

    company_sentiment.columns = ['company', 'avg_positive', 'avg_negative',
                                'avg_engagement', 'overall_sentiment', 'job_count', 'avg_salary']

    # Filter companies with at least 2 jobs
    company_sentiment = company_sentiment[company_sentiment['job_count'] >= 2]

    create_sentiment_visualizations(company_sentiment, sentiment_df)

    return company_sentiment

def create_sentiment_visualizations(company_sentiment, sentiment_df):
    """Create sentiment analysis visualizations"""

    # Set style
    plt.style.use('default')
    sns.set_palette("Set2")
    plt.rcParams.update({
        'font.size': 12,
        'axes.titlesize': 16,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10
    })

    # 1. Overall Company Sentiment Ranking
    print("[CHART 1] Creating company sentiment ranking...")
    create_sentiment_ranking(company_sentiment)

    # 2. Sentiment vs Salary Analysis
    print("[CHART 2] Creating sentiment vs salary analysis...")
    create_sentiment_salary_analysis(company_sentiment)

    # 3. Engagement Score Analysis
    print("[CHART 3] Creating engagement score analysis...")
    create_engagement_analysis(company_sentiment)

    # 4. Sentiment Distribution
    print("[CHART 4] Creating sentiment distribution...")
    create_sentiment_distribution(sentiment_df)

    print("[SUCCESS] All sentiment analysis charts created!")

def create_sentiment_ranking(company_sentiment):
    """Create company sentiment ranking chart"""

    plt.figure(figsize=(14, 10))

    # Sort by overall sentiment
    top_companies = company_sentiment.nlargest(15, 'overall_sentiment')

    # Create color map based on sentiment score
    colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(top_companies)))

    bars = plt.barh(range(len(top_companies)), top_companies['overall_sentiment'],
                    color=colors)

    plt.title('Company Sentiment Analysis - Top 15 UK AI Employers',
              fontsize=18, fontweight='bold', pad=25)
    plt.xlabel('Overall Sentiment Score', fontsize=14, fontweight='bold')
    plt.ylabel('Companies', fontsize=14, fontweight='bold')
    plt.yticks(range(len(top_companies)), top_companies['company'])

    # Add value labels with job count
    for i, (sentiment, jobs) in enumerate(zip(top_companies['overall_sentiment'],
                                            top_companies['job_count'])):
        plt.text(sentiment + 0.01, i, f'{sentiment:.3f} ({int(jobs)} jobs)',
                ha='left', va='center', fontsize=10, fontweight='bold')

    plt.xlim(0, max(top_companies['overall_sentiment']) * 1.2)
    plt.grid(axis='x', alpha=0.3)

    # Add sentiment scale explanation
    plt.figtext(0.02, 0.02,
               "Sentiment Score: Higher values indicate more positive language in job descriptions",
               fontsize=10, style='italic')

    plt.tight_layout()
    plt.savefig('sentiment_1_company_ranking.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_sentiment_salary_analysis(company_sentiment):
    """Create sentiment vs salary analysis"""

    plt.figure(figsize=(12, 8))

    # Filter companies with salary data
    salary_data = company_sentiment[
        (company_sentiment['avg_salary'] > 0) &
        (company_sentiment['avg_salary'].notna())
    ]

    if len(salary_data) > 0:
        scatter = plt.scatter(salary_data['avg_salary'], salary_data['overall_sentiment'],
                            s=salary_data['job_count'] * 20,  # Size by job count
                            c=salary_data['overall_sentiment'],
                            cmap='RdYlGn', alpha=0.7,
                            edgecolors='black', linewidth=0.5)

        plt.colorbar(scatter, label='Sentiment Score')

        # Add trend line
        if len(salary_data) > 3:
            z = np.polyfit(salary_data['avg_salary'], salary_data['overall_sentiment'], 1)
            p = np.poly1d(z)
            plt.plot(salary_data['avg_salary'], p(salary_data['avg_salary']),
                    "r--", alpha=0.8, linewidth=2, label='Trend Line')
            plt.legend()

        # Annotate some interesting points
        for _, row in salary_data.nlargest(5, 'overall_sentiment').iterrows():
            plt.annotate(row['company'],
                        (row['avg_salary'], row['overall_sentiment']),
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=8, alpha=0.8)

    plt.title('Company Sentiment vs Average Salary', fontsize=18, fontweight='bold', pad=25)
    plt.xlabel('Average Salary (GBP)', fontsize=14, fontweight='bold')
    plt.ylabel('Overall Sentiment Score', fontsize=14, fontweight='bold')

    # Format x-axis as currency
    ax = plt.gca()
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'£{x:,.0f}'))

    plt.figtext(0.02, 0.02,
               "Bubble size indicates number of job postings",
               fontsize=10, style='italic')

    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('sentiment_2_salary_correlation.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_engagement_analysis(company_sentiment):
    """Create engagement score analysis"""

    plt.figure(figsize=(14, 8))

    # Sort by engagement score
    top_engagement = company_sentiment.nlargest(12, 'avg_engagement')

    bars = plt.bar(range(len(top_engagement)), top_engagement['avg_engagement'],
                   color=plt.cm.viridis(np.linspace(0.2, 0.8, len(top_engagement))))

    plt.title('Company Engagement Score Analysis - Top 12 Companies',
              fontsize=18, fontweight='bold', pad=25)
    plt.xlabel('Companies', fontsize=14, fontweight='bold')
    plt.ylabel('Average Engagement Score', fontsize=14, fontweight='bold')
    plt.xticks(range(len(top_engagement)), top_engagement['company'],
               rotation=45, ha='right')

    # Add value labels
    for i, (bar, score) in enumerate(zip(bars, top_engagement['avg_engagement'])):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{score:.2f}', ha='center', va='bottom', fontweight='bold')

    plt.figtext(0.02, 0.02,
               "Engagement Score: Based on mentions of team, culture, training, development, etc.",
               fontsize=10, style='italic')

    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('sentiment_3_engagement_scores.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_sentiment_distribution(sentiment_df):
    """Create sentiment distribution analysis"""

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Sentiment Analysis Distribution', fontsize=18, fontweight='bold')

    # 1. Overall sentiment distribution
    ax1.hist(sentiment_df['overall_sentiment'], bins=20, alpha=0.7, color='skyblue',
             edgecolor='black')
    ax1.set_title('Overall Sentiment Distribution')
    ax1.set_xlabel('Sentiment Score')
    ax1.set_ylabel('Number of Jobs')
    ax1.axvline(sentiment_df['overall_sentiment'].mean(), color='red', linestyle='--',
                label=f'Mean: {sentiment_df["overall_sentiment"].mean():.3f}')
    ax1.legend()

    # 2. Positive vs Negative scores
    ax2.scatter(sentiment_df['positive_score'], sentiment_df['negative_score'],
                alpha=0.6, c=sentiment_df['overall_sentiment'], cmap='RdYlGn')
    ax2.set_title('Positive vs Negative Sentiment')
    ax2.set_xlabel('Positive Keywords Count')
    ax2.set_ylabel('Negative Keywords Count')

    # 3. Sentiment by work type
    work_types = sentiment_df['work_type'].value_counts().head(5).index
    work_sentiment = [sentiment_df[sentiment_df['work_type'] == wt]['overall_sentiment'].mean()
                     for wt in work_types]

    ax3.bar(range(len(work_types)), work_sentiment,
            color=plt.cm.Set3(np.linspace(0, 1, len(work_types))))
    ax3.set_title('Sentiment by Work Type')
    ax3.set_xlabel('Work Type')
    ax3.set_ylabel('Average Sentiment')
    ax3.set_xticks(range(len(work_types)))
    ax3.set_xticklabels(work_types, rotation=45, ha='right')

    # 4. Engagement score distribution
    ax4.hist(sentiment_df['engagement_score'], bins=15, alpha=0.7, color='lightgreen',
             edgecolor='black')
    ax4.set_title('Engagement Score Distribution')
    ax4.set_xlabel('Engagement Score')
    ax4.set_ylabel('Number of Jobs')
    ax4.axvline(sentiment_df['engagement_score'].mean(), color='red', linestyle='--',
                label=f'Mean: {sentiment_df["engagement_score"].mean():.2f}')
    ax4.legend()

    plt.tight_layout()
    plt.savefig('sentiment_4_distributions.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    try:
        company_sentiment = create_company_sentiment_analysis()

        # Save detailed results
        company_sentiment.to_csv('company_sentiment_analysis.csv', index=False)
        print(f"\n[SAVED] Detailed sentiment analysis saved to 'company_sentiment_analysis.csv'")

        print(f"\n[COMPLETE] Company sentiment analysis finished at {datetime.now()}")

    except Exception as e:
        print(f"[ERROR] Sentiment analysis failed: {e}")
        print("Make sure 'live_uk_ai_jobs.csv' exists in the current directory")