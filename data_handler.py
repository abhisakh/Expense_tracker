# data_handler.py

import pandas as pd
import os

FILENAME = "expenses.csv"

def init_file():
    if not os.path.exists(FILENAME):
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
        df.to_csv(FILENAME, index=False)

def load_data():
    return pd.read_csv(FILENAME)

def save_expense(new_expense):
    new_expense.to_csv(FILENAME, mode="a", header=False, index=False)
