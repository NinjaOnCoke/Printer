#!/usr/bin/env python3
"""
Print Dashboard - Setup Verification Script
Checks all dependencies and database connection
Run this before deploying: python verify_setup.py
"""

import sys
import os
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_python_version():
    """Check Python version"""
    print("📌 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} - Need 3.9+")
        return False

def check_files():
    """Check required files exist"""
    print("📌 Checking required files...")
    required_files = [
        'app.py',
        'requirements.txt',
        '.env.example',
        'README.md'
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} - Found")
        else:
            print(f"❌ {file} - NOT found")
            all_exist = False
    
    return all_exist

def check_env_file():
    """Check .env file exists"""
    print("📌 Checking .env configuration...")
    if Path('.env').exists():
        print("✅ .env file found")
        return True
    elif Path('.env.example').exists():
        print("⚠️  .env file not found (but .env.example exists)")
        print("   Run: cp .env.example .env")
        return False
    else:
        print("❌ Neither .env nor .env.example found")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("📌 Checking Python dependencies...")
    
    required_packages = {
        'streamlit': 'Streamlit web framework',
        'psycopg2': 'PostgreSQL driver',
        'pandas': 'Data manipulation',
        'plotly': 'Interactive charts',
        'dotenv': 'Environment variables',
    }
    
    all_installed = True
    for package, description in required_packages.items():
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} - Installed ({description})")
        except ImportError:
            print(f"❌ {package} - NOT installed")
            all_installed = False
    
    if not all_installed:
        print("\n💡 Install missing packages with:")
        print("   pip install -r requirements.txt")
    
    return all_installed

def check_database_connection():
    """Check database connection"""
    print("📌 Checking database connection...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        import psycopg2
        
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            print("⚠️  DATABASE_URL not set in .env")
            print("   Add your Neon PostgreSQL connection string to .env")
            return False
        
        print(f"   Connecting to: {db_url[:50]}...")
        
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT COUNT(*) FROM employees;")
        emp_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM printers;")
        printer_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM print_logs;")
        logs_count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        print(f"✅ Database connection successful")
        print(f"   └─ Employees: {emp_count}")
        print(f"   └─ Printers: {printer_count}")
        print(f"   └─ Print logs: {logs_count}")
        
        return True
        
    except ImportError:
        print("❌ psycopg2 not installed - skipping database test")
        return False
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

def print_summary(results):
    """Print summary of checks"""
    print_header("VERIFICATION SUMMARY")
    
    checks = [
        ("Python Version", results.get('python', False)),
        ("Required Files", results.get('files', False)),
        (".env Configuration", results.get('env', False)),
        ("Python Dependencies", results.get('deps', False)),
        ("Database Connection", results.get('db', False)),
    ]
    
    all_passed = all(status for _, status in checks)
    
    for check_name, status in checks:
        symbol = "✅" if status else "⚠️ "
        print(f"{symbol} {check_name}")
    
    print()
    
    if all_passed:
        print("🎉 All checks passed! You're ready to run:")
        print("   streamlit run app.py")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("   See SETUP_GUIDE.md for detailed instructions.")
    
    return all_passed

def main():
    """Main verification function"""
    print_header("🖨️  PRINT DASHBOARD - SETUP VERIFICATION")
    print("Checking your installation and configuration...\n")
    
    results = {}
    
    results['python'] = check_python_version()
    results['files'] = check_files()
    results['env'] = check_env_file()
    results['deps'] = check_dependencies()
    results['db'] = check_database_connection()
    
    success = print_summary(results)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
