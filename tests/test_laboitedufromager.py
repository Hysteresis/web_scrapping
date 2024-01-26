import pandas as pd
import sqlite3
import os
import pytest
import requests


@pytest.mark.parametrize("url", ["https://www.laboitedufromager.com/liste-des-fromages-par-ordre-alphabetique/"])
def test_1_connexion_website(url):
    """
    test connexion to website laboitedufromager.com
    :return:
    """
    response = requests.get(url)

    assert response.status_code == 200


def test_2_database_exists():
    """
    Test if the sqlite file exists
    """
    assert os.path.exists("../DATA/boitedufromager.sqlite")


def test_3_columns_exist():
    """
    Test if 4 columns exist
    """
    con = sqlite3.connect("../DATA/boitedufromager.sqlite")
    data = pd.read_sql_query("SELECT * FROM ODS", con)
    con.close()
    expected_columns = ['Fromage', 'Famille', 'Pate', 'creation_date']

    assert all(col in data.columns for col in expected_columns)


def test_4_extraction_data():
    """
    Test 1st row of file boitedufromager.sqlite
    """
    con = sqlite3.connect("../DATA/boitedufromager.sqlite")
    data = pd.read_sql_query("SELECT Fromage FROM ODS", con)
    con.close()
    print(data['Fromage'].values[0])

    assert "A" in data['Fromage'].values[0]


def test_5_total_rows_in_database():
    """
    test number of total rows
    :return:
    """
    con = sqlite3.connect("../DATA/boitedufromager.sqlite")

    data = pd.read_sql_query("SELECT * FROM ODS", con)
    con.close()

    assert len(data) == 353


def test_6_cheese_with_letter_A():
    """
    test number of cheese with words that start with the letter A
    :return:
    """
    con = sqlite3.connect("../DATA/boitedufromager.sqlite")
    query = "SELECT * FROM ODS WHERE Fromage LIKE 'A%'"
    data = pd.read_sql_query(query, con)
    row_count = data.shape[0]
    print(row_count)

    con.close()

    assert row_count == 8


def test_7_famille_column_has_expected_values():
    """
    test some values are in column 'Famille'
    :return:
    """
    con = sqlite3.connect("../DATA/boitedufromager.sqlite")
    data = pd.read_sql_query("SELECT DISTINCT Famille FROM ODS", con)
    con.close()

    expected_values = ['Vache', 'Chèvre', 'Brebis']
    assert (value in expected_values for value in data['Famille'])
    # assert all(value in expected_values for value in data['Famille'])


def test_8_format_date_creation():
    """
    Test format of column 'date_creation'
    :return:
    """
    con = sqlite3.connect("../DATA/boitedufromager.sqlite")
    data = pd.read_sql_query("SELECT creation_date FROM ODS", con)
    con.close()

    # Vérifier le format 'AAAA-MM-JJ HH:MM:SS.SSSSSS'
    assert all(pd.to_datetime(data['creation_date'],  format='%Y-%m-%d %H:%M:%S.%f').notnull())

@pytest.mark.parametrize("fromage, famille, pate", [('Abbaye de la Pierre-qui-Vire', 'Vache', 'Molle à croûte lavée'),
            ('Banon', 'Chèvre', 'Molle à croûte naturelle')])
def test_9_insertion(fromage, famille, pate):
    """
    test number of total rows for column 'date_creation'
    :return:
    """
    con = sqlite3.connect("../DATA/boitedufromager.sqlite")
    data = pd.read_sql_query("SELECT * FROM ODS", con)
    expected_row = (fromage, famille, pate)
    con.close()
    print(f"\n\n\n\nexpected_row : {expected_row}")
    existing_row = data[(data['Fromage'] == fromage) & (data['Famille'] == famille) & (data['Pate'] == pate)]
    print(f"\n\n\nexisting_row {existing_row} ")

    assert not existing_row.empty


def test_10_total_cheese_count():
    """
    test number of total rows for column 'Fromage'
    :return:
    """
    con = sqlite3.connect("../DATA/boitedufromager.sqlite")
    data = pd.read_sql_query("SELECT * FROM ODS", con)
    con.close()

    total_rows = data.shape[0]
    expected_total_rows = 353

    assert total_rows == expected_total_rows

# faire un groupby() .count compter le nombre de fromage par famille creer une colone qui recupere la
# 1ere lettre fonction substring

def test_11_count_family():
    """
    test number of total rows for column 'Fromage'
    :return:
    """
    con = sqlite3.connect("../DATA/boitedufromager.sqlite")
    data = pd.read_sql_query("SELECT *,SUBSTR(Famille, 1, 1) AS animal FROM ODS", con)
    columns = ['animal', 'Famille']
    count_by_family = data[columns].groupby('Famille').count()
    con.close()
    print(count_by_family)



