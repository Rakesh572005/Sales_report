import streamlit as st
import pandas as pd
from db import get_connection
from layout import render_layout

render_layout()
conn = get_connection()

st.subheader("📦 Product Analysis")

q = """
SELECT
    product_id,
    SUM(quantity) AS quantity,
    SUM(total_amount) AS revenue
FROM SALES_FACT
WHERE 1=1
"""

if st.session_state.year != "All":
    q += f" AND year = {st.session_state.year}"

q += " GROUP BY product_id ORDER BY revenue DESC"

df = pd.read_sql(q, conn)

st.bar_chart(df.set_index("PRODUCT_ID")[["REVENUE"]])
st.dataframe(df, use_container_width=True)
