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

# 📌 Reload latest data after submission
df = load_data()

# -------------------------------
# 🗑️ Delete an Expense Section
# -------------------------------
st.subheader("🗑️ Delete an Expense")

if df.empty:
    st.info("No expenses to delete.")
else:
    # Reset index to reference rows by number
    df_reset = df.reset_index(drop=True)
    st.dataframe(df_reset)

    # Let user pick an index to delete
    index_to_delete = st.number_input(
        "Enter the index number of the expense to delete:",
        min_value=0,
        max_value=len(df_reset) - 1,
        step=1,
        format="%d"
    )

    if st.button("Delete Selected Expense"):
        df_updated = df_reset.drop(index=index_to_delete)
        df_updated.to_csv("expenses.csv", index=False)
        st.success(f"Deleted expense at index {index_to_delete}.")
