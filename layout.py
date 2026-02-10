import streamlit as st

def render_layout():

    st.set_page_config(
        page_title="Sales Analytics Dashboard",
        layout="wide"
    )

    st.title("📊 Sales Analytics Dashboard")

    # -------- HEADER NAVIGATION --------
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("🏠 Executive"):
            st.switch_page("pages/1_Executive_Overview.py")

    with c2:
        if st.button("📅 Time"):
            st.switch_page("pages/2_Time_Analysis.py")

    with c3:
        if st.button("📦 Product"):
            st.switch_page("pages/3_Product_Analysis.py")

    st.divider()

    # -------- GLOBAL FILTER STATE --------
    if "year" not in st.session_state:
        st.session_state.year = "All"
    if "month" not in st.session_state:
        st.session_state.month = "All"
    if "day" not in st.session_state:
        st.session_state.day = "All"

    # -------- SIDEBAR FILTERS --------
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
