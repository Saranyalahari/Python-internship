import streamlit as st
from parse_coverage import get_coverage_data

st.set_page_config(page_title="Coverage Dashboard", layout="wide")

st.title("📊 Test Coverage Dashboard")

df = get_coverage_data()

# Display Table
st.subheader("📄 Coverage Table")
st.dataframe(df)

# Highlight Low Coverage
st.subheader("⚠️ Low Coverage Files (<50%)")
low = df[df["Coverage (%)"] < 50]

if not low.empty:
    st.write(low)
else:
    st.success("All files have good coverage!")

# Bar Chart
st.subheader("📊 Coverage Visualization")
st.bar_chart(df.set_index("File")["Coverage (%)"])