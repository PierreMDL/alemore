import os
from app import filesystem_actions


class BaseÉtiquette:
    def __init__(self, id_collection: int, titre_collection: str, position: int):
        self.id = id_collection
        self.titre = titre_collection.replace("&#39;", "'")  # TODO - trouver comment déséchapper caractères spéciaux
        self.position = position
        toutes_les_images = os.listdir(filesystem_actions.construire_chemin_dossier(id_collection))
        if len(toutes_les_images) > 0:
            self.src = filesystem_actions.construire_chemin_fichier(id_collection, toutes_les_images[0], from_root=False)
        else:
            self.src = filesystem_actions.construire_chemin_fichier(id_collection, "placeholder.jpg", from_root=False)


class Étiquette(BaseÉtiquette):
    def __init__(self, id_collection: int, titre_collection: str, position: int, slug: str):
        self.slug = slug
        super().__init__(id_collection=id_collection, titre_collection=titre_collection, position=position)


class AdminÉtiquette(BaseÉtiquette):
    def __init__(self, titre_collection: str, description_collection: str, id_collection: int, position: int):
        self.description = description_collection.replace("&#39;", "'").split("\n") if description_collection else []  # TODO - idem
        super().__init__(titre_collection=titre_collection, id_collection=id_collection, position=position)


class Collection:
    def __init__(self, id_collection, titre_collection, description_collection):
        self.id = id_collection
        self.titre = titre_collection.replace("&#39;", "'")  # TODO - idem
        self.description = description_collection.replace("&#39;", "'").split("\n") if description_collection else []  # TODO - idem
        self.tableaux = []


class Tableau:
    def __init__(self, id_tableau, titre_tableau, description_tableau, id_collection, nom_fichier):
        self.id = id_tableau
        self.titre = titre_tableau.replace("&#39;", "'")  # TODO - idem
        self.description = description_tableau.replace("&#39;", "'").split("\n") if description_tableau else []  # TODO - idem
        self.src = filesystem_actions.construire_chemin_fichier(id_collection, nom_fichier, from_root=False)
