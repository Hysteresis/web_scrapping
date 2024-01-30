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
        cheese_list = self.extract_data_from_website()
        data = self.create_dataframe(cheese_list)
        print(data.columns)
        number_of_lines = data['url_cheese'].count()
        print(number_of_lines)
        # self.store_data_in_database(data)

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
                if url_cheese:
                    details = list(self.get_cheese_details(url_cheese))
                    details[2] = details[2].replace('\xa0', '')
                    details = tuple(details)

                    cheese_info = {'Fromage': cheese,
                                   'Famille': family,
                                   'Pate': paste,
                                   'Prix_TTC': details[1],
                                   'Description': details[2],
                                   'Moyenne': details[4],
                                   'Nombre_avis': details[3],
                                   'Url_fromage': url_cheese,
                                   'Url_image': details[0]
                                   }

                    cheese_list.append(cheese_info)
                    print(cheese_list)
        return cheese_list

    def get_cheese_details(self,url_cheese):
        # < div
        #
        # class ="woocommerce-product-rating" >
        #
        # < div
        #
        # class ="star-rating" role="img" aria-label="Note 4.21 sur 5" > < span style="width:84.2%" > Noté < strong class ="rating" > 4.21 < / strong > sur 5 basé sur < span class ="rating" > 29 < / span > notations client < / span > < / div > < a href="#reviews" class ="woocommerce-review-link" rel="nofollow" > ( < span
        #
        # class ="count" > 29 < / span > avis client) < / a >
        # < / div >
        if url_cheese is not None:
            full_url = "https://www.laboitedufromager.com/" + url_cheese
            data = urlopen(full_url)
            soup = BeautifulSoup(data, features="html.parser")

            img_tags = soup.findAll('img', {'data-large_image': True})
            if img_tags:
                first_img_tag = img_tags[0]
                img_url = first_img_tag['data-large_image']

            prices = soup.find('p', {'class': "price"})
            if prices:
                cheese_price = prices.get_text(strip=True)
                cheese_price = cheese_price.replace('€', '')
                cheese_price = cheese_price.replace('TTC', '')

            description = soup.find('meta', {'property': 'og:description'})
            if description:
                description = description.get('content')

            count_star_rating = soup.find('span', {'class': 'rating'})
            if count_star_rating:
                count_star_rating = count_star_rating.getText()

            average_star_rating = soup.find('strong', {'class': 'rating'})
            if average_star_rating:
                average_star_rating = average_star_rating.getText()

        return img_url, cheese_price, description, count_star_rating, average_star_rating


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
