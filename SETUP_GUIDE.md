# 📋 Setup & Deployment Guide

## 🚀 LOCAL SETUP (5 minutes)

### Option 1: Quick Setup Script

**On macOS/Linux:**
```bash
#!/bin/bash

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
echo "✅ Setup complete! Edit .env with your database credentials, then run:"
echo "streamlit run app.py"
```

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
echo "✅ Setup complete! Edit .env with your database credentials, then run:"
echo "streamlit run app.py"
```

### Option 2: Manual Setup

```bash
# 1. Create & activate virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure database
cp .env.example .env
# Edit .env with your Neon PostgreSQL credentials

# 4. Run dashboard
streamlit run app.py
```

Dashboard will be available at: **http://localhost:8501**

---

## ☁️ DEPLOY ON STREAMLIT CLOUD (FREE)

### Prerequisites
- GitHub account
- Streamlit Cloud account (free)
- Your project pushed to GitHub

### Step-by-Step Deployment

#### Step 1: Prepare Your GitHub Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Add print analytics dashboard"

# Push to GitHub
git branch -M main
git push -u origin main
```

#### Step 2: Create Streamlit Cloud Account

1. Go to **https://share.streamlit.io**
2. Click **Sign up**
3. Choose **Sign up with GitHub**
4. Authorize Streamlit to access your GitHub account
5. Click **Continue**

#### Step 3: Deploy Your App

1. Click **Create app** (top-right)
2. Fill in the form:
   - **Repository:** Select your GitHub repo
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. Click **Deploy**

**Wait 2-3 minutes for deployment** ✨

#### Step 4: Add Database Secrets

1. Click the **☰** menu (top-right corner)
2. Go to **Settings** → **Secrets**
3. Add your database credentials:

```
DATABASE_URL="postgresql://user:password@ep-xxxxx.neon.tech/dbname?sslmode=require"
```

4. Click **Save**

**Done!** Your dashboard is now live! 🎉

---

## 🔐 Getting Your Neon PostgreSQL Connection String

### From Neon Console:

1. Go to **https://console.neon.tech**
2. Login to your account
3. Select your project
4. Click **Connection Details**
5. Copy the **Connection string** (looks like):
   ```
   postgresql://user:password@ep-xxxxx.neon.tech/dbname?sslmode=require
   ```
6. Paste it in `.env` or Streamlit Secrets

---

## 🐛 Troubleshooting Deployment

### Issue: "ModuleNotFoundError: No module named 'psycopg2'"

**Solution:** Ensure `requirements.txt` includes `psycopg2-binary`
```
pip install psycopg2-binary
```

### Issue: "Connection refused" or "Host not found"

**Solution:** Check your DATABASE_URL:
```bash
# Test connection locally first
python -c "import psycopg2; psycopg2.connect('$DATABASE_URL')"
```

### Issue: Dashboard shows "No data"

**Solution:** Verify your database has data:
```sql
SELECT COUNT(*) FROM print_logs;
SELECT COUNT(*) FROM employees;
SELECT COUNT(*) FROM printers;
```

### Issue: Secrets not loading in Streamlit Cloud

**Solution:** 
1. Clear browser cache (Ctrl+Shift+Delete)
2. Redeploy app (click menu → Rerun)
3. Check secret names match exactly

### Issue: Auto-refresh not working

**Solution:** 
- Update `streamlit-autorefresh` to latest version
- Ensure app is running in browser for 30+ seconds

---

## ⚡ Performance Tips

### 1. Add Database Indexes

```sql
-- Run these on your Neon database
CREATE INDEX idx_print_logs_employee_id ON print_logs(employee_id);
CREATE INDEX idx_print_logs_printer_id ON print_logs(printer_id);
CREATE INDEX idx_print_logs_print_time ON print_logs(print_time DESC);
CREATE INDEX idx_print_logs_date ON print_logs(DATE(print_time));
```

### 2. Optimize Queries

- Dashboard caches data for 30 seconds
- Lists cache for 60 seconds
- Manual refresh available in sidebar

### 3. Monitor Usage

On Streamlit Cloud:
- Click **Manage app** → **View logs**
- Watch for slow queries
- Check memory usage

---

## 📊 Verifying Installation

### Local Test

```python
# test_connection.py
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

try:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM print_logs;")
    count = cursor.fetchone()[0]
    print(f"✅ Connection successful! Print logs: {count}")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

Run it:
```bash
python test_connection.py
```

---

## 🆘 Getting Help

1. **Streamlit Docs:** https://docs.streamlit.io
2. **Neon Help:** https://neon.tech/docs/get-started-with-neon
3. **Plotly Docs:** https://plotly.com/python
4. **GitHub Issues:** Create an issue in your repo

---

## ✅ Checklist Before Going Live

- [ ] Database tables created with sample data
- [ ] `.env` file created with correct credentials
- [ ] Local test: `streamlit run app.py` works
- [ ] Repository pushed to GitHub
- [ ] Streamlit Cloud app created
- [ ] Secrets added to Streamlit Cloud
- [ ] Dashboard accessible at public URL
- [ ] Auto-refresh every 30 seconds working
- [ ] Charts loading with data
- [ ] Filters working correctly
- [ ] CSV export working

---

## 🎉 Next Steps

After deployment:
1. Share dashboard URL with team
2. Monitor dashboard logs
3. Add more visualizations as needed
4. Set up alerts for anomalies
5. Collect feedback from users

Happy analyzing! 📈
