import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import pandas as pd
from datetime import date

# Matplotlib imports
import matplotlib
matplotlib.use("TkAgg") # Ensure correct backend
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- DATABASE HANDLER ---
def init_db():
    """Initializes the SQLite database and creates the table if it doesn't exist."""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_expense_to_db(date, category, amount, description):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)',
                   (date, category, amount, description))
    conn.commit()
    conn.close()

def fetch_expenses():
    conn = sqlite3.connect('expenses.db')
    try:
        df = pd.read_sql_query("SELECT * FROM expenses", conn)
    except Exception:
        df = pd.DataFrame(columns=["id", "date", "category", "amount", "description"])
    conn.close()
    return df

# --- GUI APPLICATION ---
class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Expense Tracker")
        self.root.geometry("900x600")

        # Variables
        self.date_var = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        self.category_var = tk.StringVar()
        self.amount_var = tk.DoubleVar()
        self.desc_var = tk.StringVar()

        # UI Setup
        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        # 1. Input Frame
        input_frame = tk.LabelFrame(self.root, text="Add New Expense", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.date_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5)
        categories = ["Food", "Transport", "Rent", "Entertainment", "Utilities", "Other"]
        self.combo_cat = ttk.Combobox(input_frame, textvariable=self.category_var, values=categories, state="readonly")
        self.combo_cat.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.amount_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Description:").grid(row=1, column=2, padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.desc_var).grid(row=1, column=3, padx=5, pady=5)

        tk.Button(input_frame, text="Add Expense", command=self.add_expense, bg="#dddddd").grid(row=2, column=0, columnspan=4, pady=10)

        # 2. Visualization Button
        tk.Button(self.root, text="Show Expenses Chart", command=self.show_chart, bg="#dddddd").pack(pady=5)

        # 3. Data Table (Treeview)
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("ID", "Date", "Category", "Amount", "Description")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
            
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar for the table
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def add_expense(self):
        try:
            date_val = self.date_var.get()
            cat_val = self.category_var.get()
            # Handle potential error if user types text in amount field
            try:
                amt_val = self.amount_var.get()
            except tk.TclError:
                messagebox.showerror("Error", "Amount must be a number.")
                return
            
            desc_val = self.desc_var.get()

            if not cat_val or amt_val <= 0:
                messagebox.showerror("Error", "Please enter a valid category and amount greater than 0.")
                return

            add_expense_to_db(date_val, cat_val, amt_val, desc_val)
            messagebox.showinfo("Success", "Expense Added!")
            self.update_table()
            
            # Clear inputs
            self.amount_var.set(0.0)
            self.desc_var.set("")
            
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {e}")

    def update_table(self):
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Fetch and insert new data
        df = fetch_expenses()
        if not df.empty:
            for _, row in df.iterrows():
                self.tree.insert("", "end", values=(row['id'], row['date'], row['category'], row['amount'], row['description']))

    def show_chart(self):
        df = fetch_expenses()
        if df.empty:
            messagebox.showinfo("Info", "No data to show.")
            return

        # Group data by Category using Pandas
        category_data = df.groupby("category")["amount"].sum()

        # Create a new window for the plot
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Expense Breakdown")
        chart_window.geometry("600x500")

        # Generate the Matplotlib Figure (Using Figure instead of pyplot for GUI safety)
        fig = Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)
        ax.pie(category_data, labels=category_data.index, autopct='%1.1f%%', startangle=90)
        ax.set_title("Expenses by Category")

        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    init_db()  # Ensure DB exists
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()