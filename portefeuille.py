"""Classe de Portefeuille"""
from datetime import date
from marche_boursier import MarchéBoursier


class ErreurDate(Exception):
    """Erreur lorsque la date est postérieure à aujourd'hui"""
    pass


class ErreurQuantité(Exception):
    """Erreur lorsqu'on ne possède pas la quantité d'actions spécifiées à vendre"""
    pass


class LiquiditéInsuffisante(Exception):
    """Erreur lorsque pas assez de liquidité pour acheter les actions"""
    pass


class Portefeuille(MarchéBoursier):
    """Les différentes méthodes et fonctions de la classe portefeuille"""

    def __init__(self):
        self.marche = MarchéBoursier()
        self.argent = {}
        self.portefeuille = {}

    def déposer(self, montant, une_date=date.today()):
        """ Dépose le montant à la date spécifiée et
            enregistre la transaction dans self.argent
        """
        if une_date > date.today():
            raise ErreurDate("La date est postérieure à la date d'aujourd'hui")

        else:
            if une_date not in self.argent:
                self.argent[une_date] = float(montant)

            elif une_date in self.argent:
                self.argent[une_date] += float(montant)

    def solde(self, une_date=date.today()):
        """ Retourne la somme de toutes les transactions
            du début du portefeuille à aujourd'hui
        """

        if une_date > date.today():
            raise ErreurDate("La date est postérieure à la date d'aujourd'hui")

        else:
            somme = 0.0
            for les_jours in self.argent:
                if les_jours <= une_date:
                    somme += self.argent[les_jours]

            return somme

    def acheter(self, symbole, quantite, une_date=date.today()):
        """ Achète les actions si assez de liquidité
            enregistre la quantité d'actions achetée dans self.portefeuille
            enregistre le montant dépensé de la transation dans self.argent
        """
        if une_date > date.today():
            raise ErreurDate("La date est postérieure à la date d'aujourd'hui")

        else:
            cout = self.marche.prix(symbole, une_date) * quantite

            if self.solde(une_date) < cout:
                raise LiquiditéInsuffisante("Liquidité insuffisante pour acheter l'action")

            elif self.solde(une_date) > cout:
                if une_date in self.argent:
                    self.argent[une_date] -= float(cout)

                elif une_date not in self.argent:
                    self.argent[une_date] = - float(cout)

                if symbole in self.portefeuille:

                    if une_date in self.portefeuille[symbole]:
                        self.portefeuille[symbole][une_date] += quantite

                    if une_date not in self.portefeuille[symbole]:
                        self.portefeuille[symbole][une_date] = quantite

                elif symbole not in self.portefeuille:
                    self.portefeuille[symbole] = {}
                    self.portefeuille[symbole][une_date] = quantite

    def vendre(self, symbole, quantite, une_date=date.today()):
        """ Vend les actions si quantite suffisante
            enregistre la quantite de l'action vendu dans self.portefeuille
            enregistre le montant obtenu de la transaction dans self.argent"""

        if une_date > date.today():
            raise ErreurDate("La date est postérieure à la date d'aujourd'hui")

        else:
            if symbole in self.portefeuille:
                quantite_titre = 0.0

                for les_jours in self.portefeuille[symbole]:
                    if les_jours <= une_date:
                        quantite_titre += self.portefeuille[symbole][les_jours]

                if quantite_titre < quantite:
                    raise ErreurQuantité("Quantité insuffisante pour effectuer la vente")

                else:
                    if une_date in self.portefeuille[symbole]:
                        self.portefeuille[symbole][une_date] -= float(quantite)

                    elif une_date not in self.portefeuille[symbole]:
                        self.portefeuille[symbole][une_date] = - float(quantite)

                    cout = self.marche.prix(symbole, une_date) * quantite
                    if une_date in self.argent:
                        self.argent[une_date] += float(cout)

                    elif une_date not in self.argent:
                        self.argent[une_date] = float(cout)

            #Ca sert tu a de quoi ca ? Yes le chum
            else:
                raise ErreurQuantité("Le titre ne fait pas partie du portefeuille")

    def titres(self, une_date=date.today()):
        """ Retourne un dictionnaire
            clé = symbole
            valeur = quantité d'actions
        """
        if une_date > date.today():
            raise ErreurDate("La date est postérieure à la date d'aujourd'hui")
        else:
            dico = {}
            for symbole in self.portefeuille:
                quantite_titre = 0.0

                for les_dates in self.portefeuille[symbole]:
                    if les_dates <= une_date:
                        quantite_titre += self.portefeuille[symbole][les_dates]

                if quantite_titre == 0.0:
                    pass

                else:
                    dico[symbole] = quantite_titre

            return dico

    def valeur_totale(self, une_date=date.today()):
        """Méthode qui retourne la valeur totale du portefeuille selon une date spécifiée"""

        if une_date > date.today():
            raise ErreurDate("La date est postérieure à la date d'aujourd'hui")
        else:
            val_tot = 0.0
            les_titres = self.titres(une_date)
            for symbole, quantite in les_titres.items():
                val_tot += quantite * self.marche.prix(symbole, une_date)

        return val_tot + self.solde(une_date)

    def valeur_des_titres(self, symboles, une_date=date.today()):
        """Méthode qui retourne la valeur totale (additionne) des titres spécifiées selon une date
        précise"""

        if une_date > date.today():
            raise ErreurDate("La date est postérieure à la date d'aujourd'hui")
        else:
            val_du_titre = 0.0
            les_titre = self.titres(une_date)
            for symbole in symboles:
                if symbole in les_titre:
                    val_du_titre += les_titre[symbole] * self.marche.prix(symbole, une_date)

            return val_du_titre



