from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from extract import Extract
import tkinter as tk
from tkinter import ttk
import subprocess
import pandas as pd
import sqlite3
import os

result = subprocess.run(["pytest", "tests/test.py"], capture_output=True, text=True)
test_result = ""
# print(result.stdout)


for index, elt in enumerate(result.stdout):
    if '%' in elt:
        if index >= 3:
            three_chars_before = result.stdout[index - 3:index]
            test_result = f"Pourcentage de tests (pytest) : {three_chars_before} %"


window = tk.Tk()
window.title("Webscrapping Fromages")

url = "https://www.laboitedufromager.com/liste-des-fromages-par-ordre-alphabetique/"
extractor = Extract(url)


def update_db():
    extractor.read_website()
    return extractor.count_family()


def show_pie_chart():
    """
        Display a pie chart of cheese family
        :return: None
        """
    extractor.draw_pie_chart()


def percentage_test():
    file_path = 'report.xlsx'
    df = pd.read_excel(file_path)
    total_rows = len(df)
    passed_count = df['result'].value_counts().get('PASSED', 0)
    success_percentage = (passed_count / total_rows) * 100

    result_label.config(text=f"Pourcentage de tests réussis : {success_percentage:.2f}%")


def show_cheeses():
    db_path = os.path.join(os.getcwd(), 'DATA', 'boitedufromager.sqlite')
    con = sqlite3.connect(db_path)
    data = pd.read_sql_query("SELECT * FROM ODS", con)
    con.close()

    # Create a new window for displaying cheeses
    cheese_window = tk.Toplevel(window)
    cheese_window.title("Liste des fromages")

    # Create a Treeview widget
    tree = ttk.Treeview(cheese_window)
    tree["columns"] = ("Fromage", "Famille", "Pate", "URL_Image", "Creation_Date")
    tree.heading("#0", text="Fromage")
    tree.heading("Fromage", text="Fromage")
    tree.heading("Famille", text="Famille")
    tree.heading("Pate", text="Pate")
    tree.heading("URL_Image", text="URL Image")
    tree.heading("Creation_Date", text="Date de création")

    # Insert data into the Treeview
    for index, row in data.iterrows():
        tree.insert("", "end", values=(row["Fromage"], row["Famille"], row["Pate"], row["url_image"], row["creation_date"]))

    tree.pack()


update_db_btn = tk.Button(window, text="Mettre à jour la base de données", command=update_db)
update_db_btn.pack()

show_chart_btn = tk.Button(window, text="Afficher le graphique", command=show_pie_chart)
show_chart_btn.pack()

# Création d'un bouton dans la fenêtre
calculate_percentage_btn = tk.Button(window, text="Calculer et afficher le pourcentage", command=percentage_test)
calculate_percentage_btn.pack()

# Création d'une étiquette pour afficher le résultat
result_label = tk.Label(window, text="")
result_label.pack()

show_cheeses_btn = tk.Button(window, text="Afficher les fromages", command=show_cheeses)
show_cheeses_btn.pack()

tk.mainloop()
