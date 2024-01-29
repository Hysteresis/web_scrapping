from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from extract import Extract
import tkinter as tk
# import matplotlib.pyplot as plt
import subprocess
import pandas as pd

result = subprocess.run(["pytest", "tests/test.py"], capture_output=True, text=True)
test_result = ""
print(result.stdout)


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
    print(extractor.count_family())
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
    passed_count = df['result'].value_counts().get('PASSED', 0)
    print(f"Nombre de lignes où 'PASSED' est présent : {passed_count}")
    result_label.config(text=f"Pourcentage de test réussis : {passed_count}")



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

tk.mainloop()
