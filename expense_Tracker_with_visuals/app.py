import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# File path
FILE = "data/expenses.csv"

st.set_page_config(page_title="Expense Tracker", layout="wide")

st.title("💸 Expense Tracker with Visuals")


# Load
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=["date", "category", "amount", "description"])
    df.to_csv(FILE, index=False)

# Convert date
df['date'] = pd.to_datetime(df['date'])

# -------------------------------
# Sidebar Input
# -------------------------------
st.sidebar.header("➕ Add Expense")

date = st.sidebar.date_input("Date", datetime.today())
category = st.sidebar.selectbox("Category",
                               ["Food", "Transport", "Shopping",
                                "Bills", "Entertainment", "Other"])
amount = st.sidebar.number_input("Amount", min_value=0.0)
description = st.sidebar.text_input("Description")

if st.sidebar.button("Add"):
    new_data = pd.DataFrame({
        "date": [date],
        "category": [category],
        "amount": [amount],
        "description": [description]
    })
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(FILE, index=False)
    st.sidebar.success("Expense Added!")


# Display Data
st.subheader("📋 Expense Data")
st.dataframe(df)


# Grouping
category_sum = df.groupby("category")["amount"].sum()
date_sum = df.groupby("date")["amount"].sum()


# Charts
st.subheader("📊 Visual Insights")

col1, col2 = st.columns(2)

# Pie Chart
with col1:
    st.write("### Category Distribution")
    fig1, ax1 = plt.subplots()
    ax1.pie(category_sum, labels=category_sum.index, autopct='%1.1f%%')
    st.pyplot(fig1)

# Bar Chart
with col2:
    st.write("### Daily Expenses")
    fig2, ax2 = plt.subplots()
    date_sum.plot(kind='bar', ax=ax2)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

# Budget Alert
st.subheader("⚠️ Budget Alert")

budget = st.number_input("Set Monthly Budget", min_value=0.0)

total_expense = df["amount"].sum()

st.write(f"Total Expense: ₹{total_expense}")

if budget > 0:
    if total_expense > budget:
        st.error("🚨 Budget Exceeded!")
    else:
        st.success("✅ Within Budget")


# Export to Excel
st.subheader("📥 Export")

if st.button("Download Excel"):
    df.to_excel("expenses_report.xlsx", index=False)
    st.success("File saved as expenses_report.xlsx")