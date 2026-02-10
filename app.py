import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    layout="wide"
)

st.title("📊 Sales Analytics Dashboard")

session = get_active_session()

# ------------------ SESSION STATE ------------------
if "section" not in st.session_state:
    st.session_state.section = "Dashboard"

if "year" not in st.session_state:
    st.session_state.year = "All"
if "month" not in st.session_state:
    st.session_state.month = "All"
if "day" not in st.session_state:
    st.session_state.day = "All"

# ------------------ HEADER NAVIGATION ------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("📊 Dashboard"):
        st.session_state.section = "Dashboard"

with c2:
    if st.button("🏠 Executive"):
        st.session_state.section = "Executive"

with c3:
    if st.button("📅 Time"):
        st.session_state.section = "Time"

with c4:
    if st.button("📦 Product"):
        st.session_state.section = "Product"

st.divider()

# ------------------ SIDEBAR FILTERS ------------------
st.sidebar.header("Filters")

years = ["All", 2021, 2022, 2023, 2024, 2025]
months = ["All"] + list(range(1, 13))
days = ["All"] + list(range(1, 32))

st.session_state.year = st.sidebar.selectbox(
    "Year", years, index=years.index(st.session_state.year)
)

st.session_state.month = st.sidebar.selectbox(
    "Month", months, index=months.index(st.session_state.month)
)

st.session_state.day = st.sidebar.selectbox(
    "Day", days, index=days.index(st.session_state.day)
)

year = st.session_state.year
month = st.session_state.month
day = st.session_state.day

st.caption(f"📌 Showing data for → Year: {year}, Month: {month}, Day: {day}")

# ------------------ FILTER HELPER ------------------
def apply_filters(q):
    if year != "All":
        q += f" AND year = {year}"
    if month != "All":
        q += f" AND month = {month}"
    if day != "All":
        q += f" AND day = {day}"
    return q

# ==================================================
# =============== DASHBOARD SECTION =================
# ==================================================
if st.session_state.section == "Dashboard":

    # ---- KPIs ----
    q = """
    SELECT
        COUNT(DISTINCT order_id) AS orders,
        SUM(quantity) AS quantity,
        SUM(total_amount) AS revenue
    FROM SALES_FACT
    WHERE 1=1
    """
    q = apply_filters(q)
    kpi = session.sql(q).to_pandas()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Orders", f"{int(kpi.iloc[0]['ORDERS']):,}")
    c2.metric("Total Revenue", f"₹{float(kpi.iloc[0]['REVENUE']):,.0f}")
    c3.metric("Total Quantity", f"{int(kpi.iloc[0]['QUANTITY']):,}")

    # ---- Monthly Trend ----
    st.subheader("📈 Monthly Revenue Trend")

    q = """
    SELECT month, SUM(total_amount) AS revenue
    FROM SALES_FACT
    WHERE 1=1
    """
    q = apply_filters(q)
    q += " GROUP BY month ORDER BY month"

    df = session.sql(q).to_pandas()
    st.line_chart(df.set_index("MONTH"))

    # ---- Customer Summary ----
    st.subheader("👥 Orders by Customer Type")

    q = """
    SELECT customer_type, COUNT(DISTINCT order_id) AS orders
    FROM SALES_FACT
    WHERE 1=1
    """
    q = apply_filters(q)
    q += " GROUP BY customer_type"

    df = session.sql(q).to_pandas()
    st.bar_chart(df.set_index("CUSTOMER_TYPE"))

    # ---- Top Products ----
    st.subheader("📦 Top 5 Products by Revenue")

    q = """
    SELECT product_id, SUM(total_amount) AS revenue
    FROM SALES_FACT
    WHERE 1=1
    """
    q = apply_filters(q)
    q += " GROUP BY product_id ORDER BY revenue DESC LIMIT 5"

    df = session.sql(q).to_pandas()
    st.bar_chart(df.set_index("PRODUCT_ID"))

# ==================================================
# =============== EXECUTIVE SECTION =================
# ==================================================
elif st.session_state.section == "Executive":

    st.subheader("🏠 Executive Summary")

    q = """
    SELECT year,
           COUNT(DISTINCT order_id) AS orders,
           SUM(total_amount) AS revenue
    FROM SALES_FACT
    WHERE 1=1
    """
    q = apply_filters(q)
    q += " GROUP BY year ORDER BY year"

    df = session.sql(q).to_pandas()
    st.dataframe(df, use_container_width=True)
    st.line_chart(df.set_index("YEAR")[["REVENUE"]])

# ==================================================
# ================= TIME SECTION ====================
# ==================================================
elif st.session_state.section == "Time":

    st.subheader("📅 Time Analysis")

    q = """
    SELECT order_date,
           COUNT(DISTINCT order_id) AS orders,
           SUM(total_amount) AS revenue
    FROM SALES_FACT
    WHERE 1=1
    """
    q = apply_filters(q)
    q += " GROUP BY order_date ORDER BY order_date"

    df = session.sql(q).to_pandas()
    st.line_chart(df.set_index("ORDER_DATE")[["REVENUE"]])
    st.dataframe(df, use_container_width=True)

# ==================================================
# =============== PRODUCT SECTION ===================
# ==================================================
elif st.session_state.section == "Product":

    st.subheader("📦 Product Analysis")

    q = """
    SELECT product_id,
           SUM(quantity) AS quantity,
           SUM(total_amount) AS revenue
    FROM SALES_FACT
    WHERE 1=1
    """
    q = apply_filters(q)
    q += " GROUP BY product_id ORDER BY revenue DESC"

    df = session.sql(q).to_pandas()
    st.bar_chart(df.set_index("PRODUCT_ID")[["REVENUE"]])
    st.dataframe(df, use_container_width=True)
