from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sqlite3
import os
import matplotlib.pyplot as plt


class Extract:
    def __init__(self, url):
        self.url = url

    def read_website(self):
        """
        Extract data from website and store data in DB
        :return: None
        """
        tds_list = self.extract_data_from_website()
        data = self.create_dataframe(tds_list)
        self.store_data_in_database(data)

    def extract_data_from_website(self):
        """
        extract data from website
        :return: list of information about cheese
        """
        cheese_list = []
        data = urlopen(self.url)
        soup = BeautifulSoup(data, features="html.parser")
        tds_list = soup.find_all('td')

        for i in range(3, len(tds_list), 3):
            cheese = tds_list[i].text.strip()
            if cheese and not tds_list[i].find('h2'):
                family = tds_list[i + 1].text.strip()
                paste = tds_list[i + 2].text.strip()
                link_tag = tds_list[i].find('a')
                url_cheese = link_tag['href'] if link_tag else None
                img_url = self.get_url_images(url_cheese) if url_cheese else None
                price = self.get_cheese_price(url_cheese)
                description = self.get_description(url_cheese)

                cheese_info = {'Fromage': cheese, 'Famille': family, 'Pate': paste, 'Prix_TTC': price,
                               'Description': description, 'Url_fromage': url_cheese, 'Url_image': img_url}
                cheese_list.append(cheese_info)

        return cheese_list

    def get_description(self, url_cheese):
        """
        get the description of a cheese
        :return : price of cheese TTC
        """
        # <meta property="og:description" content="L’Abondance est un fromage au lait cru de vache de race Abondance, Tarine et Montbéliarde. À pâte demi-cuite, il se présente sous la forme d’une meule de 6 à 12 kg, à talon concave. Il a une pâte souple et fondante de couleur ivoire à jaune pâle, avec un taux de matière grasse de 33 %.
    # La durée d’affinage est d’au moins 3 mois sur des planches d’épicéa et en cave fraîche et humide au cours desquels il est régulièrement frotté à l’eau salée et retourné. L’Abondance est produite uniquement dans la Haute-Savoie. Il est apprécié tel quel, fondu ou cuisiné dans de nombreux plats salés pour ses notes de noisette et sa saveur fruitée.
    # Lorsque l’Abondance est fermier, il comporte une plaque de caséine ovale et verte sur son talon. S’il est fabriqué en fromagerie (laitier), la plaque est carrée et rouge.
    # Prix au kilo : 39,50€ (soit 11,85€ pour 300g)">
        if url_cheese != None:
            full_url = "https://www.laboitedufromager.com/" + url_cheese
            data = urlopen(full_url)
            soup = BeautifulSoup(data, features="html.parser")
            description = soup.find('meta', {'property': 'og:description'})
            print(description)
            description = description.get('content')
            print(description)

            return description

    def get_cheese_price(self, url_cheese):
        """
        get the price of a cheese
        :return : price of cheese TTC

        """
        if url_cheese != None:
            full_url = "https://www.laboitedufromager.com/" + url_cheese
            data = urlopen(full_url)
            soup = BeautifulSoup(data, features="html.parser")
            prices = soup.find('p', {'class': "price"})
            cheese_price = prices.get_text(strip=True)
            cheese_price = cheese_price.replace('€', '')
            cheese_price = cheese_price.replace('TTC', '')

            return cheese_price

    def get_url_images(self, url_cheese):
        """
        get url of images
        :return : url of image (string)
        """
        full_url = "https://www.laboitedufromager.com/" + url_cheese
        data = urlopen(full_url)
        soup = BeautifulSoup(data, features="html.parser")
        img_tags = soup.findAll('img', {'data-large_image': True})

        if img_tags:
            first_img_tag = img_tags[0]
            img_url = first_img_tag['data-large_image']

            return img_url


    def create_dataframe(self, cheese_list):
        """
        Create dataframe
        :param cheese_list:list of information about cheese
        :return:dataframe with cheese information and create date
        """
        data = pd.DataFrame(cheese_list)
        data['creation_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['Famille'].replace({
            'Vache Bufflonne': 'Vache ou Bufflonne',
            'Vache ou Bufflonne': 'Vache ou Bufflonne',
            'Vache Brebis': 'Vache ou Brebis',
            'Vache/Brebis': 'Vache ou Brebis',
            'Vache / Chèvre': 'Vache ou Chèvre',
            'Chèvre Brebis': 'Chèvre ou Brebis',
        })

        return data

    def store_data_in_database(self, data):
        """
        store data in DB SQLite
        :param data:dataframe with cheese information
        :return:None
        """
        root = os.getcwd()
        path = os.path.join(root, 'DATA')
        db_path = os.path.join(path, 'boitedufromager.sqlite')
        con = sqlite3.connect(db_path)
        data.to_sql("ODS", con, if_exists="replace", index=False)
        con.close()

    def count_family(self):
        """
        Count the occurrences of each family in the database
        :return: None
        """
        db_path = os.path.join(os.getcwd(), 'DATA', 'boitedufromager.sqlite')
        con = sqlite3.connect(db_path)

        data = pd.read_sql_query("SELECT * FROM ODS", con)
        count_by_family = data['Fromage'].groupby(data['Famille']).count()
        con.close()

        return count_by_family

    def draw_pie_chart(self):
        """
        Dessiner un diagramme circulaire (pie chart) pour la famille des fromages
        :return: None
        """
        labels = []
        sizes = []

        count_by_family = self.count_family()

        other = 0
        for family, number in count_by_family.items():
            if number < 5:
                other += number
            else:
                labels.append(family)
                sizes.append(number)
        if other > 0:
            labels.append("Autres")
            sizes.append(other)

        figure, axis = plt.subplots()

        axis.set_title("Famille")
        axis.pie(sizes, labels=labels, autopct="%1.1f%%", shadow=True, startangle=90)
        axis.axis('equal')

        plt.show()
