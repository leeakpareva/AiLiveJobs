#!/usr/bin/env python3
"""
Real-Time UK AI Job Data Fetcher using Adzuna API
Fetches live job data and updates the dashboard automatically
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import time
import json
import re

# Load environment variables
load_dotenv()

class AdzunaJobFetcher:
    def __init__(self):
        self.app_id = os.getenv('ADZUNA_APP_ID')
        self.app_key = os.getenv('ADZUNA_APP_KEY')
        self.base_url = "https://api.adzuna.com/v1/api/jobs/gb/search"

        if not self.app_id or not self.app_key:
            raise ValueError("Adzuna API credentials not found in .env file")

        print(f"[SUCCESS] Adzuna API initialized with App ID: {self.app_id}")

    def fetch_ai_jobs(self, max_results=500):
        """Fetch AI/ML jobs from UK using Adzuna API"""

        print(f"[FETCH] Getting live UK AI job data from Adzuna...")

        all_jobs = []
        page = 1
        results_per_page = 50  # Adzuna max per request

        # AI/ML related search terms
        search_terms = [
            "artificial intelligence",
            "machine learning",
            "data scientist",
            "ML engineer",
            "AI engineer",
            "deep learning",
            "NLP engineer",
            "computer vision"
        ]

        for search_term in search_terms:
            print(f"[SEARCH] Searching for: {search_term}")

            try:
                for page_num in range(1, 6):  # Get up to 5 pages per term
                    url = f"{self.base_url}/{page_num}"

                    params = {
                        'app_id': self.app_id,
                        'app_key': self.app_key,
                        'what': search_term,
                        'where': 'uk',
                        'results_per_page': results_per_page,
                        'sort_by': 'date',
                        'max_days_old': 30  # Only jobs posted in last 30 days
                    }

                    response = requests.get(url, params=params, timeout=10)

                    if response.status_code == 200:
                        data = response.json()
                        jobs = data.get('results', [])

                        if not jobs:
                            break  # No more results

                        all_jobs.extend(jobs)
                        print(f"[PAGE] Got {len(jobs)} jobs from page {page_num}")

                        # Rate limiting - be respectful to API
                        time.sleep(0.5)

                        if len(all_jobs) >= max_results:
                            break
                    else:
                        print(f"[ERROR] API request failed: {response.status_code}")
                        break

                if len(all_jobs) >= max_results:
                    break

            except Exception as e:
                print(f"[ERROR] Error fetching {search_term}: {e}")
                continue

        print(f"[SUCCESS] Fetched {len(all_jobs)} total jobs from Adzuna")
        return self.process_jobs_data(all_jobs)

    def process_jobs_data(self, raw_jobs):
        """Process raw Adzuna data into our dashboard format"""

        processed_jobs = []

        for job in raw_jobs:
            try:
                # Extract salary info
                salary_min, salary_max = self.extract_salary(job)

                # Classify job category
                category = self.classify_job_category(job.get('title', ''), job.get('description', ''))

                # Extract experience level
                experience = self.extract_experience_level(job.get('title', ''), job.get('description', ''))

                # Extract work type
                work_type = self.extract_work_type(job.get('description', ''))

                # Extract skills
                skills = self.extract_skills(job.get('description', ''))

                processed_job = {
                    'job_id': job.get('id', ''),
                    'title': job.get('title', 'Unknown'),
                    'company': job.get('company', {}).get('display_name', 'Unknown'),
                    'location': self.clean_location(job.get('location', {}).get('display_name', 'UK')),
                    'category': category,
                    'experience_level': experience,
                    'work_type': work_type,
                    'salary_min': salary_min,
                    'salary_max': salary_max,
                    'salary_avg': (salary_min + salary_max) / 2 if salary_min and salary_max else None,
                    'required_skills': ', '.join(skills),
                    'description': job.get('description', '')[:500] + '...',  # Truncate
                    'posted_date': self.parse_date(job.get('created')),
                    'url': job.get('redirect_url', ''),
                    'source': 'Adzuna API',
                    'fetched_at': datetime.now()
                }

                processed_jobs.append(processed_job)

            except Exception as e:
                print(f"[WARN] Error processing job: {e}")
                continue

        df = pd.DataFrame(processed_jobs)

        # Remove duplicates based on title + company
        df = df.drop_duplicates(subset=['title', 'company'], keep='first')

        print(f"[PROCESS] Processed {len(df)} unique jobs")
        return df

    def extract_salary(self, job):
        """Extract salary range from job data"""
        salary_min = job.get('salary_min')
        salary_max = job.get('salary_max')

        # If salary info not available, try to extract from description
        if not salary_min or not salary_max:
            description = job.get('description', '').lower()

            # Look for salary patterns
            salary_patterns = [
                r'£(\d{2,3}),?(\d{3})\s*-\s*£(\d{2,3}),?(\d{3})',  # £50,000 - £80,000
                r'£(\d{2,3})k\s*-\s*£(\d{2,3})k',  # £50k - £80k
                r'(\d{2,3}),?(\d{3})\s*-\s*(\d{2,3}),?(\d{3})',  # 50,000 - 80,000
            ]

            for pattern in salary_patterns:
                match = re.search(pattern, description)
                if match:
                    try:
                        if 'k' in pattern:
                            salary_min = int(match.group(1)) * 1000
                            salary_max = int(match.group(2)) * 1000
                        else:
                            salary_min = int(match.group(1) + match.group(2))
                            salary_max = int(match.group(3) + match.group(4))
                        break
                    except:
                        continue

        # Fallback estimates based on job title
        if not salary_min or not salary_max:
            title = job.get('title', '').lower()
            if 'senior' in title or 'lead' in title:
                salary_min, salary_max = 70000, 110000
            elif 'principal' in title or 'head of' in title:
                salary_min, salary_max = 120000, 180000
            elif 'junior' in title or 'graduate' in title:
                salary_min, salary_max = 35000, 55000
            else:
                salary_min, salary_max = 50000, 75000  # Mid-level default

        return salary_min, salary_max

    def classify_job_category(self, title, description):
        """Classify job into our categories"""
        text = (title + ' ' + description).lower()

        if any(term in text for term in ['research', 'scientist', 'phd']):
            return 'Research'
        elif any(term in text for term in ['product manager', 'product owner', 'strategy']):
            return 'Product & Management'
        elif any(term in text for term in ['nlp', 'natural language', 'computer vision', 'cv engineer']):
            return 'Specialized'
        elif any(term in text for term in ['data scientist', 'data analyst', 'analytics']):
            return 'Data Science'
        else:
            return 'Engineering'  # Default

    def extract_experience_level(self, title, description):
        """Extract experience level from job"""
        text = (title + ' ' + description).lower()

        if any(term in text for term in ['principal', 'head of', 'director']):
            return 'Principal'
        elif any(term in text for term in ['lead', 'team lead', 'tech lead']):
            return 'Lead'
        elif any(term in text for term in ['senior', 'sr.', 'sr ']):
            return 'Senior'
        elif any(term in text for term in ['junior', 'jr.', 'graduate', 'entry']):
            return 'Entry'
        else:
            return 'Mid'  # Default

    def extract_work_type(self, description):
        """Extract work arrangement type"""
        text = description.lower()

        if any(term in text for term in ['remote', 'work from home', 'wfh']):
            if any(term in text for term in ['hybrid', 'flexible', 'office days']):
                return 'Hybrid'
            else:
                return 'Remote'
        elif any(term in text for term in ['on-site', 'office-based', 'in office']):
            return 'On-site'
        else:
            return 'Hybrid'  # Default assumption for modern jobs

    def extract_skills(self, description):
        """Extract technical skills from job description"""
        text = description.lower()

        # Define skill patterns
        skill_keywords = [
            'python', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'sql', 'mongodb',
            'spark', 'hadoop', 'kafka', 'airflow', 'mlflow', 'cuda', 'git',
            'transformers', 'langchain', 'openai', 'hugging face', 'bert',
            'react', 'javascript', 'node.js', 'java', 'scala', 'r', 'matlab',
            'tableau', 'power bi', 'jupyter', 'anaconda', 'linux'
        ]

        found_skills = []
        for skill in skill_keywords:
            if skill in text:
                found_skills.append(skill.title())

        return found_skills[:6]  # Limit to top 6 skills

    def clean_location(self, location):
        """Clean and standardize location names"""
        if not location:
            return 'UK'

        location = location.strip()

        # Map common variations
        location_mapping = {
            'Greater London': 'London',
            'City of London': 'London',
            'Central London': 'London',
            'Manchester, Greater Manchester': 'Manchester',
            'Birmingham, West Midlands': 'Birmingham',
            'Edinburgh, Scotland': 'Edinburgh',
            'Glasgow, Scotland': 'Glasgow',
            'Cambridge, Cambridgeshire': 'Cambridge',
            'Oxford, Oxfordshire': 'Oxford',
            'Bristol, South West': 'Bristol',
            'Leeds, West Yorkshire': 'Leeds',
            'Newcastle upon Tyne': 'Newcastle'
        }

        return location_mapping.get(location, location)

    def parse_date(self, date_str):
        """Parse Adzuna date format"""
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            return datetime.now() - timedelta(days=1)

    def save_data(self, df, filename='live_uk_ai_jobs.csv'):
        """Save fetched data to CSV"""
        df.to_csv(filename, index=False)
        print(f"[SAVE] Data saved to {filename}")
        return filename


def main():
    """Test the real-time data fetcher"""
    print("="*60)
    print("REAL-TIME UK AI JOB DATA FETCHER")
    print("="*60)

    try:
        # Initialize fetcher
        fetcher = AdzunaJobFetcher()

        # Fetch live data
        df = fetcher.fetch_ai_jobs(max_results=200)

        if len(df) > 0:
            # Display summary
            print(f"\n[SUMMARY] Fetched {len(df)} live UK AI jobs")
            print(f"Companies: {df['company'].nunique()}")
            print(f"Locations: {df['location'].nunique()}")
            print(f"Categories: {df['category'].value_counts().to_dict()}")
            print(f"Date range: {df['posted_date'].min()} to {df['posted_date'].max()}")

            # Save data
            filename = fetcher.save_data(df)

            print(f"\n[SUCCESS] Real-time data ready for dashboard!")
            print(f"[FILE] {filename}")

        else:
            print("[WARN] No jobs fetched - check API credentials or network")

    except Exception as e:
        print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()