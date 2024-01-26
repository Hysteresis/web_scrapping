from extract import Extract


url = "https://www.laboitedufromager.com/liste-des-fromages-par-ordre-alphabetique/"

extractor = Extract(url)
extractor.read_website()
extractor.count_family()
