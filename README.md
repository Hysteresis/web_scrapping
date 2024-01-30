# Web Scrapping

## Description
Ce programme permet de scrapper la liste des fromages : [la boite du fromager](https://www.laboitedufromager.com/liste-des-fromages-par-ordre-alphabetique)
Il récupère : 
- Le nom du froamge
- La famille
- la pate
- L'url des l'image du fromage
- Le prix du fromage en € TTC
- La description
- Le nombre d’avis
- La moyenne des notes

## Installation
- Version Python: **3.10** ou sup
- Base de données: **SQLite** 
- GUI: Tkinter
- Librairies:
  - BeautifulSoup
  - Pandas
  - Matplotlib

## Projet : module 1 - Python
### Créer une interface utilisateur qui aura les fonctionnalités suivantes :
- Un bouton pour mettre à jour la BDD
- Un diagramme en camembert qui affichera le ratio de fromage par famille
- Un taux de fiabilité des résultats

### Récupérer de nouvelles informations :
- L’image du fromage
- Le prix du fromage
- La description
- Le nombre d’avis
- La moyenne des notes

## Utilisation
- Mettre à jour la BDD : cliquer sur le bouton **"Mettre à jour la Base de données"**
- Pour afficher le ratio de fromages par famille : cliquer sur le bouton **"Afficher le graphique"**
