# 🖨️ Print Analytics Dashboard

A modern, real-time Power BI-style dashboard built with **Streamlit** and **Neon PostgreSQL**. Monitor printing activities, employee usage, and printer performance with beautiful visualizations and auto-refresh capabilities.

## ✨ Features

- ✅ **Real-time Dashboard** - Auto-refreshes every 30 seconds
- ✅ **Power BI-style Design** - Modern dark theme with professional UI
- ✅ **KPI Cards** - Key metrics at a glance
  - Total Prints
  - Active Printers
  - Total Employees
  - Total Pages Printed
- ✅ **Advanced Charts** - Interactive Plotly visualizations
  - Daily print trends
  - Top 10 employees by usage
  - Printer usage analysis
- ✅ **Filtered Reports** - Dynamic data filtering
  - By Employee
  - By Printer
  - By Date Range
- ✅ **Recent Print Jobs** - Detailed table with 100+ records
- ✅ **CSV Export** - Download reports as CSV
- ✅ **Performance Optimized** - Smart caching (30-second TTL)
- ✅ **FREE Hosting** - Deploy on Streamlit Cloud
- ✅ **Responsive Design** - Works on desktop and mobile

## 🎯 What You Get

```
project/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.9+
- Neon PostgreSQL Database (Free tier available)
- Streamlit Account (for free hosting)

### 2. Clone & Setup

```bash
# Clone or download the project
git clone <your-repo>
cd Printer

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Database

**Copy `.env.example` to `.env` and add your Neon credentials:**

```bash
cp .env.example .env
```

**Edit `.env` with your Neon database connection:**

```
# Option 1: Use DATABASE_URL (recommended)
DATABASE_URL=postgresql://user:password@ep-xxxxx.neon.tech/dbname?sslmode=require

# Option 2: Use individual parameters
DB_HOST=ep-xxxxx.neon.tech
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_SSLMODE=require
```

### 4. Run Locally

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

## 🌐 Deploy to Streamlit Cloud (FREE)

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Initial dashboard commit"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repository and branch
5. Choose main file: `app.py`
6. Click **"Deploy"**

### Step 3: Add Secrets

In Streamlit Cloud dashboard:
1. Click on your app settings ⚙️
2. Go to **Secrets**
3. Add your `.env` variables:

```
DATABASE_URL="postgresql://user:password@ep-xxxxx.neon.tech/dbname?sslmode=require"
```

That's it! Your dashboard is now live! 🎉

## 📊 Database Schema

The dashboard connects to these 4 tables:

```sql
-- Employees table
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    employee_name TEXT NOT NULL UNIQUE,
    department TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Printers table
CREATE TABLE printers (
    id SERIAL PRIMARY KEY,
    printer_name TEXT NOT NULL UNIQUE,
    location TEXT,
    model TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Print logs (main data)
CREATE TABLE print_logs (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    printer_id INTEGER NOT NULL REFERENCES printers(id) ON DELETE CASCADE,
    document_name TEXT NOT NULL,
    pages_printed INTEGER NOT NULL,
    print_time TIMESTAMPTZ NOT NULL,
    captured_at TIMESTAMPTZ DEFAULT NOW()
);

-- Collected jobs
CREATE TABLE collected_jobs (
    id SERIAL PRIMARY KEY,
    job_id TEXT NOT NULL UNIQUE,
    printer_name TEXT NOT NULL,
    collected_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 🎨 Dashboard Sections

### 1. **KPI Cards** (Top)
Quick overview of key metrics:
- Total Prints - Cumulative print count
- Active Printers - Printers used in last 7 days
- Total Employees - Registered employees
- Total Pages - Total pages printed

### 2. **Analytics Charts**
- **Daily Print Trends** - Line chart of prints over time
- **Top 10 Employees** - Bar chart by usage
- **Printer Usage** - Bar chart with location info

### 3. **Recent Print Jobs**
- 100 most recent jobs
- Filterable by employee and printer
- Sortable columns
- CSV export button

### 4. **Sidebar Filters**
- **Date Range** - Last 1-90 days
- **Employee** - Filter by specific employee
- **Printer** - Filter by specific printer
- **Refresh Button** - Manual cache refresh

## ⚙️ Performance & Caching

The dashboard uses Streamlit's caching to optimize performance:

- **KPI & Chart Data**: 30-second TTL
- **Employee/Printer Lists**: 60-second TTL
- **Auto-refresh**: Every 30 seconds (via `streamlit-autorefresh`)
- **Database Queries**: Optimized with indexes on `employee_id`, `printer_id`, `print_time`

### Database Indexes (Recommended)

For better performance, add these indexes to your Neon database:

```sql
CREATE INDEX idx_print_logs_employee_id ON print_logs(employee_id);
CREATE INDEX idx_print_logs_printer_id ON print_logs(printer_id);
CREATE INDEX idx_print_logs_print_time ON print_logs(print_time DESC);
CREATE INDEX idx_print_logs_time_employee ON print_logs(print_time, employee_id);
```

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Streamlit** | Web framework & UI |
| **Plotly** | Interactive charts |
| **Pandas** | Data manipulation |
| **Psycopg2** | PostgreSQL driver |
| **Neon** | Database hosting |
| **streamlit-autorefresh** | Auto-refresh feature |

## 📱 Browser Support

- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers

## 🔒 Security

- Credentials stored in `.env` (never commit!)
- SSL/TLS for database connection
- No sensitive data in code
- Streamlit Cloud handles secrets securely

## 🐛 Troubleshooting

### Connection Error?
```
Error: "could not translate host name "ep-xxxxx.neon.tech" to address"
```
✅ **Solution**: Check your `DATABASE_URL` in `.env`

### No data showing?
```
📭 No print jobs found
```
✅ **Solution**: Ensure your tables have data. Try:
```sql
SELECT COUNT(*) FROM print_logs;
```

### Dashboard slow?
✅ **Solution**: Add database indexes (see Performance section)

### Cache not clearing?
✅ **Solution**: Click "Refresh Now" button in sidebar

## 📈 Next Steps

### To enhance your dashboard:

1. **Add more filters** - Department, date range
2. **More charts** - Hourly trends, heatmaps
3. **Alerts** - Low printer toner, high usage
4. **Export reports** - PDF, Excel with historical data
5. **User authentication** - Multi-user dashboard
6. **Mobile app** - Streamlit for mobile

## 📞 Support

For help:
- Check the code comments in `app.py`
- Review Streamlit docs: https://docs.streamlit.io
- Neon docs: https://neon.tech/docs
- Plotly docs: https://plotly.com/python

## 📄 License

Free to use and modify for personal/commercial projects.

## 🎉 Happy Analyzing!

Your print analytics dashboard is ready to monitor, analyze, and optimize your printing operations! 

**Questions?** Check the code comments or Streamlit documentation.

---

Made with ❤️ | Last updated: 2026