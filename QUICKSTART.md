# ⚡ 5-MINUTE QUICKSTART

Get your dashboard running in 5 minutes!

## Step 1: Setup (2 minutes)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# OR: venv\Scripts\activate  # Windows

# Install packages
pip install -r requirements.txt

# Create config file
cp .env.example .env
```

## Step 2: Configure (1 minute)

Open `.env` and add your Neon database URL:

```
DATABASE_URL=postgresql://user:password@ep-xxxxx.neon.tech/dbname?sslmode=require
```

**Where to find it:**
1. Go to [console.neon.tech](https://console.neon.tech)
2. Select your project → "Connection Details"
3. Copy the Connection String
4. Paste in `.env`

## Step 3: Verify (1 minute)

```bash
# Check everything is working
python verify_setup.py
```

You should see:
```
✅ Python Version - OK
✅ Required Files - Found
✅ .env Configuration - OK
✅ Python Dependencies - Installed
✅ Database Connection - OK

🎉 All checks passed!
```

## Step 4: Run (1 minute)

```bash
streamlit run app.py
```

Dashboard opens at: **http://localhost:8501** 🎉

---

## 🌐 Deploy to Cloud (FREE)

### 1. Push to GitHub

```bash
git add .
git commit -m "Add dashboard"
git push origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign up with GitHub
3. Click "Create app"
4. Select your repo, branch, and `app.py`
5. Click "Deploy"

### 3. Add Secrets

In your Streamlit Cloud dashboard:
1. Click ☰ → Settings → Secrets
2. Add:
```
DATABASE_URL="postgresql://..."
```
3. Save

**Done! Your dashboard is live!** 🚀

---

## 📊 What You Get

- ✅ Real-time KPI cards
- ✅ 3 interactive charts
- ✅ Recent jobs table
- ✅ Sidebar filters
- ✅ Auto-refresh (30 seconds)
- ✅ CSV export
- ✅ Dark theme
- ✅ Mobile-responsive

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Database connection error | Check DATABASE_URL in .env |
| No data showing | Verify your database has data: `SELECT COUNT(*) FROM print_logs;` |
| Port already in use | Run `streamlit run app.py --server.port 8502` |

---

## 📚 Need Help?

- **Setup issues?** → See [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Features?** → See [README.md](README.md)
- **Code details?** → Check comments in `app.py`

---

## ✅ Quick Checklist

- [ ] Cloned/downloaded project
- [ ] Created virtual environment
- [ ] Installed requirements
- [ ] Created `.env` file
- [ ] Added DATABASE_URL
- [ ] Ran `verify_setup.py` ✅
- [ ] Ran `streamlit run app.py`
- [ ] Dashboard opened in browser
- [ ] Deployed to Streamlit Cloud (optional)

**You're all set!** Enjoy your dashboard! 🎉
