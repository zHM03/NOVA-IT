import json
import os
from datetime import datetime

DATA_FILE = 'data/finance_data.json'


class BudgetManager:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'w') as f:
                json.dump({"income": [], "expense": []}, f)
        self.data = self.load_data()

    def load_data(self):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)

    def save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_income(self, amount, description=""):
        entry = {
            "amount": float(amount),
            "description": description,
            "date": datetime.now().isoformat()
        }
        self.data["income"].append(entry)
        self.save_data()

    def add_expense(self, amount, category, description=""):
        entry = {
            "amount": float(amount),
            "category": category,
            "description": description,
            "date": datetime.now().isoformat()
        }
        self.data["expense"].append(entry)
        self.save_data()

    def get_summary(self):
        total_income = sum(i["amount"] for i in self.data["income"])
        total_expense = sum(e["amount"] for e in self.data["expense"])
        balance = total_income - total_expense
        return total_income, total_expense, balance

    def get_expenses_by_category(self):
        categories = {}
        for e in self.data["expense"]:
            categories[e["category"]] = categories.get(e["category"], 0) + e["amount"]
        return categories

    def get_all_income(self):
        return self.data["income"]

    def get_all_expense(self):
        return self.data["expense"]

    def delete_income(self, index):
        if 0 <= index < len(self.data["income"]):
            del self.data["income"][index]
            self.save_data()

    def delete_expense(self, index):
        if 0 <= index < len(self.data["expense"]):
            del self.data["expense"][index]
            self.save_data()

