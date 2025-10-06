# NAVADA - AI Jobs Intelligence Platform

A comprehensive UK AI job market intelligence platform with real-time job listings, advanced analytics, sentiment analysis, and AI-powered insights.

## 🚀 Features

### 📊 Dashboard Analytics
- **Live Job Data**: 185+ real-time UK AI job listings from Adzuna API
- **Salary Analysis**: Comprehensive salary trends by experience level and location
- **Company Insights**: Top hiring companies with detailed metrics
- **Skills Demand**: In-demand technologies and skills analysis
- **Geographic Distribution**: UK job market regional breakdown
- **Work Arrangements**: Remote, hybrid, and on-site job patterns

### 🔍 Enhanced Analytics
- **Salary Histogram**: Distribution analysis across all salary ranges
- **Company Leaderboard**: Top employers ranked by job volume and average salaries
- **Geographic Mapping**: Regional salary and job concentration data
- **Historical Trends**: 12-month market trend analysis
- **Category Breakdown**: 30+ job categories with detailed insights

### 💭 Company Sentiment Analysis
- **Sentiment Ranking**: Companies ranked by job description positivity
- **Salary Correlation**: Relationship between company sentiment and compensation
- **Engagement Scores**: Company culture and employee engagement metrics
- **Distribution Analysis**: Market-wide sentiment patterns

### 🤖 AI Assistant (Leslie)
- **Intelligent Chat**: AI-powered job market insights and career guidance
- **Real-time Analysis**: Instant answers about salary trends, companies, and skills
- **Market Intelligence**: Deep insights from live job data
- **Personalized Guidance**: Career advice based on current market conditions

### 📱 Interactive Features
- **Burger Menu Navigation**: Clean interface with organized tools access
- **Job Listings Browser**: Searchable and filterable job database
- **Chart Zoom**: Click any chart for detailed view with close functionality
- **Responsive Design**: Mobile-friendly interface
- **Dark Theme**: Professional glass-morphism design

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python serverless functions (Vercel)
- **Design**: Glass-morphism dark theme with responsive layout
- **Data Processing**: Python with pandas, matplotlib, seaborn
- **APIs**: Adzuna Jobs API, OpenAI GPT integration
- **Charts**: Python-generated PNG visualizations
- **Deployment**: Vercel serverless platform
- **Architecture**: Static web application with CSV data backend

## 🚀 Quick Start

### 🌐 Live Demo (Recommended)
**Access the live platform instantly:**
- **Production URL**: https://navada-ai-jobs-e24gil3pw-leeakparevas-projects.vercel.app
- **Features**: Full dashboard, job listings, analytics, and AI assistant
- **No setup required**: Ready to use immediately

### 💻 Local Development

#### Method 1: Run with Local Server
1. **Clone the repository**
2. **Install dependencies**: pandas, matplotlib, seaborn, requests
3. **Start the server**: `python start_server.py` or double-click `start_navada.bat`
4. **Access dashboard**: Opens automatically at http://localhost:8888/navada_dashboard.html
5. **Access features via burger menu**: Job listings and AI assistant

#### Method 2: Direct Launch
1. **Run launcher**: `python enhanced_navada_launcher.py`
2. **Note**: Job listings may not load due to browser CORS restrictions

### 🚢 Deploy Your Own
1. **Fork the repository**
2. **Deploy to Vercel**: Connect your GitHub repo to Vercel for automatic deployment
3. **Or use Vercel CLI**: `npx vercel --prod --yes`

## 📊 16 Total Charts
- 8 Standard Analytics
- 4 Enhanced Analytics
- 4 Sentiment Analysis Charts

## 📋 Data Fetch Logging

NAVADA includes comprehensive logging for Adzuna API data fetching:

- **Log File**: `adzuna_fetch_log.txt` - Automatically created in project directory
- **What's Logged**:
  - Fetch start/completion times
  - Number of jobs retrieved
  - API response times
  - Error handling and diagnostics
  - Data processing statistics

**Sample Log Entry**:
```
2025-10-06 04:33:09,016 - INFO - REAL-TIME UK AI JOB DATA FETCHER - STARTED
2025-10-06 04:33:09,017 - INFO - Initializing Adzuna API fetcher...
2025-10-06 04:33:09,018 - INFO - Starting job data fetch from Adzuna API...
2025-10-06 04:33:15,234 - INFO - Successfully fetched 185 live UK AI jobs in 6.22 seconds
2025-10-06 04:33:15,456 - INFO - Data saved to live_uk_ai_jobs.csv
2025-10-06 04:33:15,457 - INFO - REAL-TIME DATA FETCH COMPLETED SUCCESSFULLY
2025-10-06 04:33:15,457 - INFO - Total execution time: 6.22 seconds
```

This logging helps track:
- ⏱️ **Schedule Performance**: Monitor fetch times and success rates
- 📈 **Data Volume**: Track job market growth and API response sizes
- 🔍 **Debugging**: Identify API issues or network problems
- 📊 **Analytics**: Historical data about fetch operations

Built with ❤️ for the UK AI job market community
