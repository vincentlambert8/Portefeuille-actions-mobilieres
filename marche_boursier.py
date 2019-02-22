"""Importation des modules"""
from datetime import date
import apiSetup as api


class ErreurDate(Exception):
    """Erreur lorsque la date est postérieure à aujourd'hui"""
    pass


class MarchéBoursier:
    """Initialisation de la classe MarchéBoursier"""
    def __init__(self):
        pass

    def prix(self, symbole, jour):

        info = api.information(symbole, jour)
        jour = api.jours_semaine(symbole, jour)

        if jour > date.today():
            raise ErreurDate("La date est postérieure à la date d'aujourd'hui")

        return float(info[str(jour)]['4. close'])
