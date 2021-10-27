import os


class Étiquette:
    def __init__(self, titre_collection: str, id_collection: int, position: int):
        self.titre_collection = titre_collection
        self.slug = self.titre_collection.replace(".", "").translate(str.maketrans(" éèà", "-eeà")).lower()
        self.id_collection = id_collection
        self.position = position
        self.src = os.path.normpath(os.path.join("/static/images/", str(id_collection), os.listdir("app/static/images/" + str(id_collection) + "/")[0]))


class AdminÉtiquette(Étiquette):
    def __init__(self, titre_collection: str, description_collection: str, id_collection: int, position: int):
        self.description_collection = description_collection
        super().__init__(titre_collection=titre_collection, id_collection=id_collection, position=position)


class Collection:
    def __init__(self, titre_collection, description_collection):
        self.titre_collection = titre_collection
        self.description_collection = description_collection.split("\n")
        self.tableaux = []


class Tableau:
    def __init__(self, titre_tableau, description_tableau, chemin):
        self.titre_tableau = titre_tableau
        self.description_tableau = description_tableau.split("\n")
        self.src = os.path.normpath(os.path.join("/static", chemin))