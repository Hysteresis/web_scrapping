from extract import Extract
import tkinter as tk

window = tk.Tk()
window.title("Webscrapping Fromages")






url = "https://www.laboitedufromager.com/liste-des-fromages-par-ordre-alphabetique/"






extractor = Extract(url)
extractor.read_website()
extractor.count_family()

# tk.mainloop()
