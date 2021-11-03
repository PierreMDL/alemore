import os
from app import filesystem_actions, inputoutput_actions


class BaseÉtiquette:
    def __init__(self, id_collection: int, titre_collection: str, position: int):
        self.id = id_collection
        self.titre = inputoutput_actions.déformater_titre(titre_collection)
        self.position = position
        toutes_les_images = os.listdir(filesystem_actions.construire_chemin_dossier(id_collection))
        if len(toutes_les_images) > 0:
            self.src = filesystem_actions.construire_chemin_fichier(id_collection, toutes_les_images[0], from_root=False)
        else:
            self.src = filesystem_actions.construire_chemin_fichier("", "placeholder.jpg", from_root=False)


class Étiquette(BaseÉtiquette):
    def __init__(self, id_collection: int, titre_collection: str, position: int, slug: str):
        self.slug = slug
        super().__init__(id_collection=id_collection, titre_collection=titre_collection, position=position)


class AdminÉtiquette(BaseÉtiquette):
    def __init__(self, titre_collection: str, description_collection: str, id_collection: int, position: int):
        self.description = inputoutput_actions.déformater_description(description_collection) if description_collection else []
        super().__init__(titre_collection=titre_collection, id_collection=id_collection, position=position)


class Collection:
    def __init__(self, id_collection, titre_collection, description_collection):
        self.id = id_collection
        self.titre = inputoutput_actions.déformater_titre(titre_collection)
        self.description = inputoutput_actions.déformater_description(description_collection) if description_collection else []
        self.tableaux = []


class Tableau:
    def __init__(self, id_tableau, titre_tableau, description_tableau, id_collection, nom_fichier):
        self.id = id_tableau
        self.titre = inputoutput_actions.déformater_titre(titre_tableau)
        self.description = inputoutput_actions.déformater_description(description_tableau) if description_tableau else []
        self.src = filesystem_actions.construire_chemin_fichier(id_collection, nom_fichier, from_root=False)
