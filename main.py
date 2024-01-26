from extract import Extract
import tkinter as tk
import matplotlib.pyplot as plt

window = tk.Tk()
window.title("Webscrapping Fromages")

url = "https://www.laboitedufromager.com/liste-des-fromages-par-ordre-alphabetique/"

extractor = Extract(url)


def update_db():
    extractor.read_website()
    extractor.count_family()


update_db_btn = tk.Button(window, text="Mettre à jour la base de données", command=update_db)
update_db_btn.pack()



tk.mainloop()
