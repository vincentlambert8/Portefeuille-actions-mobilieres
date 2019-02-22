"""Importation des modules"""
import json
from datetime import timedelta, date
import requests


def information(symbole, jour):
    """Fonction qui retourne le dictionnaire de l'API Alpha Vintage"""

    size = temps(jour)
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbole,
        'apikey': 'ZLZ91TZRGZ6VHTUD',
        'outputsize': size,
        }

    response = requests.get(url='https://www.alphavantage.co/query', params=params)

    response = json.loads(response.text)
    return response['Time Series (Daily)']


def temps(jour):
    """Fonction qui regarde s'il y a plus de 100 jours entre aujourd'hui et la date entrée"""
    return 'compact' if jour >= (date.today() - timedelta(100)) else 'full'


def jours_semaine(symbole, jour):
    """Fonction qui regarde si une date est présente dans le dictionnaire. Si elle ne l'est
    pas, la fonction retourne la date antérieure la plus récente qui l'est."""

    info = information(symbole, jour)
    loop = True

    while loop is True:
        if str(jour) in info:
            loop = False
        else:
            jour -= timedelta(1)

    return jour
