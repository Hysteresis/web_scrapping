from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sqlite3
import os
import matplotlib.pyplot as plt
from slugify import slugify


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
                if link_tag:
                    url_cheese = link_tag['href']
                    # img_url = self.get_url_images(url_cheese)
                    print(url_cheese)
                    cheese_list.append({'Fromage': cheese, 'url_cheese': url_cheese, 'Famille': family, 'Pate': paste,
                                        })
                else:
                    url_cheese = None
                cheese_list.append({'Fromage': cheese, 'url_cheese': url_cheese, 'Famille': family, 'Pate': paste,
                                   })

        return cheese_list

    def get_url_images(self, url_cheese):
        full_url = "https://www.laboitedufromager.com/" + url_cheese
        # data = urlopen(full_url)
        # soup = BeautifulSoup(data, features="html.parser")
        # img_tags = soup.findAll('img', {'data-large_image': True})
        #
        # if img_tags:
        #     first_img_tag = img_tags[0]
        #     img_url = first_img_tag['data-large_image']
        #     # print(img_url)
        #     return img_url
        # else:
        #     print("pas d'url")
        #     return None



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

        axis.pie(sizes, labels=labels, autopct="%1.1f%%", shadow=True, startangle=90)
        axis.axis('equal')

        axis.set_title("Famille")

        plt.show()


