import streamlit as st
import pandas as pd
from db import get_connection
from layout import render_layout

render_layout()
conn = get_connection()

st.subheader("🏠 Executive View")

q = """
SELECT
    year,
    COUNT(DISTINCT order_id) AS orders,
    SUM(total_amount) AS revenue
FROM SALES_FACT
WHERE 1=1
"""

if st.session_state.year != "All":
    q += f" AND year = {st.session_state.year}"

q += " GROUP BY year ORDER BY year"

df = pd.read_sql(q, conn)

st.dataframe(df, use_container_width=True)
st.line_chart(df.set_index("YEAR")[["REVENUE"]])
