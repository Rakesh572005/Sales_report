import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session
from layout import render_layout

render_layout()

session = get_active_session()

year = st.session_state.year
month = st.session_state.month
day = st.session_state.day

st.caption(f"📌 Showing data for → Year: {year}, Month: {month}, Day: {day}")

def apply_filters(q):
    if year != "All":
        q += f" AND year = {year}"
    if month != "All":
        q += f" AND month = {month}"
    if day != "All":
        q += f" AND day = {day}"
    return q

# -------- KPIs --------
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

orders = int(kpi.iloc[0]["ORDERS"])
revenue = float(kpi.iloc[0]["REVENUE"])
quantity = int(kpi.iloc[0]["QUANTITY"])

c1, c2, c3 = st.columns(3)

c1.metric("Total Orders", f"{orders:,}", delta="↑ vs prev")
c2.metric("Total Revenue", f"₹{revenue:,.0f}", delta="↑ vs prev")
c3.metric("Total Quantity", f"{quantity:,}", delta="↑ vs prev")

# -------- MONTHLY TREND --------
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

# -------- CUSTOMER SUMMARY --------
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

# -------- TOP 5 PRODUCTS --------
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
