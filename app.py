import streamlit as st
import pandas as pd
from db import get_connection
from layout import render_layout

render_layout()
st.caption(
    "💡 Use the buttons in the header to navigate to detailed analysis pages."
)

conn = get_connection()

def format_number(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)



year = st.session_state.year
month = st.session_state.month
day = st.session_state.day

st.caption(
    f"📌 Showing data for → "
    f"Year: {year}, Month: {month}, Day: {day}"
)


def apply_filters(q):
    if year != "All":
        q += f" AND year = {year}"
    if month != "All":
        q += f" AND month = {month}"
    if day != "All":
        q += f" AND day = {day}"
    return q

# -------- KPI SECTION --------
q = """
SELECT
    COUNT(DISTINCT order_id) AS orders,
    SUM(quantity) AS quantity,
    SUM(total_amount) AS revenue
FROM SALES_FACT
WHERE 1=1
"""
q = apply_filters(q)

kpi = pd.read_sql(q, conn)

orders = int(kpi.iloc[0]["ORDERS"])     
revenue = float(kpi.iloc[0]["REVENUE"])
quantity = int(kpi.iloc[0]["QUANTITY"])

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Orders",
    f"{orders:,}",
    delta="↑ vs previous period"
)

c2.metric(
    "Total Revenue",
    f"₹{revenue:,.0f}",
    delta="↑ vs previous period"
)

c3.metric(
    "Total Quantity",
    f"{quantity:,}",
    delta="↑ vs previous period"
)


# -------- TIME TREND --------
st.subheader("📈 Monthly Revenue Trend")

q = """
SELECT month, SUM(total_amount) AS revenue
FROM SALES_FACT
WHERE 1=1
"""
q = apply_filters(q)
q += " GROUP BY month ORDER BY month"

df = pd.read_sql(q, conn)
st.line_chart(df.set_index("MONTH"))

# -------- CUSTOMER SUMMARY --------
st.subheader("👥 Orders by Customer Type")

q = """
SELECT customer_type, COUNT(DISTINCT order_id) AS orders
FROM SALES_FACT
WHERE 1=1
"""
q = apply_filters(q)
q += " GROUP BY customer_type"

df = pd.read_sql(q, conn)
st.bar_chart(df.set_index("CUSTOMER_TYPE"))

# -------- PRODUCT SUMMARY --------
st.subheader("📦 Revenue by Product")

q = """
SELECT product_id, SUM(total_amount) AS revenue
FROM SALES_FACT
WHERE 1=1
"""
q = apply_filters(q)
q += " GROUP BY product_id ORDER BY revenue DESC"

df = pd.read_sql(q, conn)
st.bar_chart(df.set_index("PRODUCT_ID"))
