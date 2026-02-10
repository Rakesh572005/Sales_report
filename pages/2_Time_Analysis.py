import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session
from layout import render_layout

render_layout()

session = get_active_session()

st.subheader("📅 Time Analysis")

q = """
SELECT
    order_date,
    COUNT(DISTINCT order_id) AS orders,
    SUM(total_amount) AS revenue
FROM SALES_FACT
WHERE 1=1
"""

if st.session_state.year != "All":
    q += f" AND year = {st.session_state.year}"
if st.session_state.month != "All":
    q += f" AND month = {st.session_state.month}"

q += " GROUP BY order_date ORDER BY order_date"

df = session.sql(q).to_pandas()

st.line_chart(df.set_index("ORDER_DATE")[["REVENUE"]])
st.dataframe(df, use_container_width=True)
