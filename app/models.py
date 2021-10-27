import os


class Étiquette:
    def __init__(self, titre_collection: str, id_collection: int, position: int):
        self.titre = titre_collection
        self.slug = self.titre.replace(".", "").translate(str.maketrans(" éèà", "-eeà")).lower()
        self.id = id_collection
        self.position = position
        self.src = os.path.normpath(os.path.join("/static/images/", str(id_collection), os.listdir("app/static/images/" + str(id_collection) + "/")[0]))


class AdminÉtiquette(Étiquette):
    def __init__(self, titre_collection: str, description_collection: str, id_collection: int, position: int):
        self.description = description_collection
        super().__init__(titre_collection=titre_collection, id_collection=id_collection, position=position)


class Collection:
    def __init__(self, id_collection, titre_collection, description_collection):
        self.id = id_collection
        self.titre = titre_collection
        self.description = description_collection.split("\n") if description_collection else []
        self.tableaux = []


class Tableau:
    def __init__(self, id_tableau, titre_tableau, description_tableau, chemin):
        self.id = id_tableau
        self.titre = titre_tableau
        self.description = description_tableau.split("\n") if description_tableau else []
        self.src = os.path.normpath(os.path.join("/static", chemin))