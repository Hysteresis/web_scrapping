from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sqlite3
import os


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
            if cheese and not tds_list[i].find('h2'):  # Check if h2 tag is not present
                family = tds_list[i + 1].text.strip()
                paste = tds_list[i + 2].text.strip()
                cheese_list.append({'Fromage': cheese, 'Famille': family, 'Pate': paste})
        print(cheese_list)
        return cheese_list

    def create_dataframe(self, cheese_list):
        """
        Create dataframe
        :param cheese_list:list of information about cheese
        :return:dataframe with cheese information and create date
        """
        data = pd.DataFrame(cheese_list)
        data['creation_date'] = datetime.now()
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
        # print(data['Famille'])
        count_by_family = data['Fromage'].groupby(data['Famille']).count()
        con.close()
        # print(count_by_family)
