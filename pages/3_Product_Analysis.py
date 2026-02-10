import streamlit as st
import pandas as pd
from layout import render_layout
from snowflake.snowpark.context import get_active_session

session = get_active_session()
df = session.sql(q).to_pandas()

render_layout()

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


st.bar_chart(df.set_index("PRODUCT_ID")[["REVENUE"]])
st.dataframe(df, use_container_width=True)
