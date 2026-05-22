import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from streamlit_autorefresh import rerun_if_updated
import time

# Load environment variables
load_dotenv()

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Print Dashboard | Analytics",
    page_icon="🖨️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== DARK THEME STYLING ====================
st.markdown("""
<style>
    :root {
        --primary-color: #00d4ff;
        --secondary-color: #1f1f1f;
        --text-color: #ffffff;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #00d4ff;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        color: #a0a0a0;
    }
    
    .block-container {
        padding: 1rem;
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 100%);
    }
    
    h1, h2, h3 {
        color: #00d4ff;
        font-weight: 700;
    }
    
    .stPlotlyChart {
        background: #1a1a2e;
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATABASE CONNECTION ====================
@st.cache_resource
def get_db_connection():
    """Create and cache database connection"""
    try:
        # Try using DATABASE_URL first, then individual parameters
        db_url = os.getenv("DATABASE_URL")
        
        if db_url:
            conn = psycopg2.connect(db_url)
        else:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT", 5432)),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                sslmode=os.getenv("DB_SSLMODE", "require")
            )
        return conn
    except Exception as e:
        st.error(f"❌ Database Connection Error: {str(e)}")
        st.stop()

# ==================== QUERY FUNCTIONS ====================
@st.cache_data(ttl=30)
def get_kpi_data():
    """Get KPI metrics - cached for 30 seconds"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Total prints
        cursor.execute("SELECT COUNT(*) as total_prints FROM print_logs;")
        total_prints = cursor.fetchone()['total_prints']
        
        # Active printers (printers with prints in last 7 days)
        cursor.execute("""
            SELECT COUNT(DISTINCT printer_id) as active_printers 
            FROM print_logs 
            WHERE print_time >= NOW() - INTERVAL '7 days';
        """)
        active_printers = cursor.fetchone()['active_printers']
        
        # Total employees
        cursor.execute("SELECT COUNT(*) as total_employees FROM employees;")
        total_employees = cursor.fetchone()['total_employees']
        
        # Pages printed
        cursor.execute("SELECT COALESCE(SUM(pages_printed), 0) as total_pages FROM print_logs;")
        total_pages = cursor.fetchone()['total_pages']
        
        cursor.close()
        conn.close()
        
        return {
            'total_prints': total_prints,
            'active_printers': active_printers,
            'total_employees': total_employees,
            'total_pages': total_pages
        }
    except Exception as e:
        st.error(f"Error fetching KPI data: {str(e)}")
        return {}

@st.cache_data(ttl=30)
def get_daily_print_trends(days=30):
    """Get daily print trends - cached for 30 seconds"""
    try:
        conn = get_db_connection()
        query = """
            SELECT 
                DATE(print_time) as print_date,
                COUNT(*) as print_count,
                SUM(pages_printed) as total_pages
            FROM print_logs
            WHERE print_time >= NOW() - INTERVAL '%s days'
            GROUP BY DATE(print_time)
            ORDER BY print_date DESC;
        """
        df = pd.read_sql(query % days, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching daily trends: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=30)
def get_top_employees(limit=10):
    """Get top employees by print count - cached for 30 seconds"""
    try:
        conn = get_db_connection()
        query = f"""
            SELECT 
                e.employee_name,
                COUNT(pl.id) as print_count,
                SUM(pl.pages_printed) as total_pages
            FROM print_logs pl
            JOIN employees e ON pl.employee_id = e.id
            GROUP BY e.id, e.employee_name
            ORDER BY print_count DESC
            LIMIT {limit};
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching top employees: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=30)
def get_printer_usage(limit=10):
    """Get printer usage statistics - cached for 30 seconds"""
    try:
        conn = get_db_connection()
        query = f"""
            SELECT 
                p.printer_name,
                p.location,
                COUNT(pl.id) as print_count,
                SUM(pl.pages_printed) as total_pages,
                AVG(pl.pages_printed) as avg_pages_per_print
            FROM print_logs pl
            JOIN printers p ON pl.printer_id = p.id
            GROUP BY p.id, p.printer_name, p.location
            ORDER BY print_count DESC
            LIMIT {limit};
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching printer usage: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=30)
def get_recent_print_jobs(limit=50, employee_id=None, printer_id=None, days=7):
    """Get recent print jobs with optional filters - cached for 30 seconds"""
    try:
        conn = get_db_connection()
        
        query = """
            SELECT 
                pl.id,
                e.employee_name,
                p.printer_name,
                pl.document_name,
                pl.pages_printed,
                pl.print_time::text,
                p.location
            FROM print_logs pl
            JOIN employees e ON pl.employee_id = e.id
            JOIN printers p ON pl.printer_id = p.id
            WHERE pl.print_time >= NOW() - INTERVAL '%s days'
        """
        params = [days]
        
        if employee_id:
            query += " AND pl.employee_id = %s"
            params.append(employee_id)
        
        if printer_id:
            query += " AND pl.printer_id = %s"
            params.append(printer_id)
        
        query += f" ORDER BY pl.print_time DESC LIMIT {limit};"
        
        df = pd.read_sql(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching print jobs: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=60)
def get_employees_list():
    """Get list of employees for filters"""
    try:
        conn = get_db_connection()
        df = pd.read_sql("SELECT id, employee_name FROM employees ORDER BY employee_name;", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching employees: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=60)
def get_printers_list():
    """Get list of printers for filters"""
    try:
        conn = get_db_connection()
        df = pd.read_sql("SELECT id, printer_name FROM printers ORDER BY printer_name;", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching printers: {str(e)}")
        return pd.DataFrame()

# ==================== AUTO REFRESH ====================
rerun_if_updated(seconds=30)

# ==================== MAIN LAYOUT ====================
st.title("🖨️ Print Analytics Dashboard")
st.markdown("Real-time printing analytics and monitoring system")

# Last updated timestamp
col1, col2 = st.columns([3, 1])
with col2:
    st.caption(f"🔄 Last updated: {datetime.now().strftime('%H:%M:%S')}")

st.divider()

# ==================== SIDEBAR FILTERS ====================
st.sidebar.title("⚙️ Filters")
st.sidebar.markdown("---")

# Date range filter
date_range = st.sidebar.slider(
    "📅 Select Date Range (Days)",
    1, 90, 7,
    help="View data from the last N days"
)

# Employee filter
employees_df = get_employees_list()
employee_options = ["All Employees"] + employees_df['employee_name'].tolist()
selected_employee = st.sidebar.selectbox("👤 Employee", employee_options)
selected_employee_id = None
if selected_employee != "All Employees":
    selected_employee_id = employees_df[employees_df['employee_name'] == selected_employee]['id'].values[0]

# Printer filter
printers_df = get_printers_list()
printer_options = ["All Printers"] + printers_df['printer_name'].tolist()
selected_printer = st.sidebar.selectbox("🖨️ Printer", printer_options)
selected_printer_id = None
if selected_printer != "All Printers":
    selected_printer_id = printers_df[printers_df['printer_name'] == selected_printer]['id'].values[0]

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Refresh Now", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

# ==================== KPI CARDS ====================
st.subheader("📊 Key Performance Indicators")

kpi_data = get_kpi_data()

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4, gap="medium")

with kpi_col1:
    st.metric(
        label="Total Prints",
        value=f"{kpi_data.get('total_prints', 0):,}",
        delta=None,
        help="Total number of print jobs"
    )

with kpi_col2:
    st.metric(
        label="Active Printers",
        value=f"{kpi_data.get('active_printers', 0)}",
        delta=None,
        help="Printers active in last 7 days"
    )

with kpi_col3:
    st.metric(
        label="Total Employees",
        value=f"{kpi_data.get('total_employees', 0)}",
        delta=None,
        help="Total registered employees"
    )

with kpi_col4:
    st.metric(
        label="Total Pages",
        value=f"{kpi_data.get('total_pages', 0):,}",
        delta=None,
        help="Total pages printed"
    )

st.divider()

# ==================== CHARTS ====================
st.subheader("📈 Analytics")

chart_col1, chart_col2 = st.columns(2, gap="medium")

# Daily Print Trends
with chart_col1:
    st.markdown("#### Daily Print Trends")
    daily_trends = get_daily_print_trends(date_range)
    
    if not daily_trends.empty:
        daily_trends = daily_trends.sort_values('print_date')
        
        fig_daily = go.Figure()
        fig_daily.add_trace(go.Scatter(
            x=daily_trends['print_date'],
            y=daily_trends['print_count'],
            mode='lines+markers',
            name='Print Count',
            line=dict(color='#00d4ff', width=3),
            marker=dict(size=8),
            hovertemplate='<b>Date:</b> %{x}<br><b>Prints:</b> %{y}<extra></extra>'
        ))
        
        fig_daily.update_layout(
            template='plotly_dark',
            hovermode='x unified',
            height=350,
            margin=dict(l=40, r=40, t=30, b=30),
            showlegend=False,
            font=dict(family="Arial, sans-serif", size=11, color='#ffffff')
        )
        fig_daily.update_yaxes(gridcolor='#2a2a3e')
        fig_daily.update_xaxes(gridcolor='#2a2a3e')
        
        st.plotly_chart(fig_daily, use_container_width=True)
    else:
        st.info("No data available for the selected period")

# Top Employees
with chart_col2:
    st.markdown("#### Top 10 Employees")
    top_employees = get_top_employees(10)
    
    if not top_employees.empty:
        fig_employees = px.bar(
            top_employees,
            x='print_count',
            y='employee_name',
            orientation='h',
            color='total_pages',
            color_continuous_scale='Blues',
            labels={'print_count': 'Print Count', 'employee_name': 'Employee'},
            title_text=None
        )
        
        fig_employees.update_layout(
            template='plotly_dark',
            hovermode='y',
            height=350,
            margin=dict(l=150, r=40, t=30, b=30),
            showlegend=False,
            font=dict(family="Arial, sans-serif", size=11, color='#ffffff')
        )
        fig_employees.update_yaxes(gridcolor='#2a2a3e')
        fig_employees.update_xaxes(gridcolor='#2a2a3e')
        
        st.plotly_chart(fig_employees, use_container_width=True)
    else:
        st.info("No employee data available")

# Printer Usage
st.markdown("#### Printer Usage Analysis")
printer_usage = get_printer_usage(10)

if not printer_usage.empty:
    fig_printers = px.bar(
        printer_usage,
        x='print_count',
        y='printer_name',
        orientation='h',
        color='total_pages',
        color_continuous_scale='Greens',
        hover_data=['location', 'avg_pages_per_print'],
        labels={'print_count': 'Print Count', 'printer_name': 'Printer Name'},
        title_text=None
    )
    
    fig_printers.update_layout(
        template='plotly_dark',
        hovermode='y',
        height=320,
        margin=dict(l=150, r=40, t=30, b=30),
        showlegend=False,
        font=dict(family="Arial, sans-serif", size=11, color='#ffffff')
    )
    fig_printers.update_yaxes(gridcolor='#2a2a3e')
    fig_printers.update_xaxes(gridcolor='#2a2a3e')
    
    st.plotly_chart(fig_printers, use_container_width=True)
else:
    st.info("No printer data available")

st.divider()

# ==================== RECENT PRINT JOBS TABLE ====================
st.subheader("📋 Recent Print Jobs")

recent_jobs = get_recent_print_jobs(
    limit=100,
    employee_id=selected_employee_id,
    printer_id=selected_printer_id,
    days=date_range
)

if not recent_jobs.empty:
    # Format the dataframe for display
    display_df = recent_jobs.copy()
    display_df['print_time'] = pd.to_datetime(display_df['print_time']).dt.strftime('%Y-%m-%d %H:%M:%S')
    display_df = display_df[['employee_name', 'printer_name', 'location', 'document_name', 'pages_printed', 'print_time']]
    display_df.columns = ['Employee', 'Printer', 'Location', 'Document', 'Pages', 'Print Time']
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    # Download button
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"print_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
else:
    st.info("📭 No print jobs found for the selected filters and date range")

st.divider()

# ==================== FOOTER ====================
st.markdown("""
<div style='text-align: center; color: #666; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #333;'>
    <small>🖨️ Print Analytics Dashboard | Real-time monitoring system | Last updated: Every 30 seconds</small>
</div>
""", unsafe_allow_html=True)
