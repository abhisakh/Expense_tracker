# app.py

import streamlit as st
import pandas as pd
from datetime import datetime
import os

# CSV file to store expenses
FILENAME = "expenses.csv"

# Create the file if it doesn't exist
if not os.path.exists(FILENAME):
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    df.to_csv(FILENAME, index=False)

# Load existing data
df = pd.read_csv(FILENAME)

st.title("💸 Expense Tracker")

# Add new expense
st.subheader("➕ Add New Expense")
with st.form("expense_form"):
    amount = st.number_input("Amount", min_value=0.01, step=0.01)
    category = st.selectbox("Category", ["Food", "Transport", "Utilities", "Entertainment", "Other"])
    description = st.text_input("Description (optional)")
    date = st.date_input("Date", value=datetime.today())
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_expense = pd.DataFrame({
            "Date": [date.strftime("%Y-%m-%d")],
            "Category": [category],
            "Amount": [amount],
            "Description": [description]
        })
        new_expense.to_csv(FILENAME, mode="a", header=False, index=False)
        st.success("Expense added successfully!")

# Show all expenses
st.subheader("📊 Expense History")
st.dataframe(df)

# Summary
st.subheader("📈 Summary")
total_spent = df["Amount"].sum()
st.write(f"**Total Spent:** ${total_spent:.2f}")

category_summary = df.groupby("Category")["Amount"].sum()
st.bar_chart(category_summary)
