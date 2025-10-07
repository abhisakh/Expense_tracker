# app.py

import streamlit as st
import pandas as pd
from datetime import datetime

from data_handler import init_file, load_data, save_expense  # 🧠 Import here

# Initialize file
init_file()

# Load existing data
df = load_data()

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
        save_expense(new_expense)  # ⬅️ Use modular function
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

#------------------Delete if wrongly added -----------------
st.subheader("🗑️ Delete an Expense")

# Reload the data to reflect any new additions
df = load_data()

if not df.empty:
    # Add row indices for selection
    df_with_index = df.reset_index()
    selected_index = st.selectbox("Select an expense to delete:", df_with_index["index"])

    if st.button("Delete Selected Expense"):
        df = df.drop(index=selected_index)
        df.to_csv("expenses.csv", index=False)
        st.success("Expense deleted successfully.")
else:
    st.info("No expenses to delete.")