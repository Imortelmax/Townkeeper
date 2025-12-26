import random

class Document:
    def __init__(self, owner_name, country, role, seal, expiration_day):
        self.owner_name = owner_name
        self.country = country
        self.role = role
        self.seal = seal
        self.expiration_day = expiration_day
        self.is_forgery = False # Par defaut le document est authentique

    def create_forgery(self):
        """Crée une contrefaçon en altérant une info"""
        self.is_forgery = True
        options = ["name", "country", "seal"]
        ftype = random.choice(options)
        if ftype == "name": self.owner_name+= random.choice(["o", "a"])
        elif ftype == "country": self.country = "Royaume Inconnu"
        elif ftype == "seal": self.seal = "Sceau Brisé"