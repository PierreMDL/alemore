import os
from app import app
import shutil


def construire_chemin_dossier(id_collection, from_root=True):
    if from_root:
        chemin = os.path.join(app.config["IMAGES_ROOT"], str(id_collection))
    else:
        chemin = os.path.join(app.config["IMAGES_REL"], str(id_collection))

    chemin = os.path.normpath(chemin)

    return chemin


def construire_chemin_fichier(id_collection, nom_fichier, from_root=True):
    if from_root:
        chemin = os.path.join(app.config["IMAGES_ROOT"], str(id_collection), nom_fichier)
    else:
        chemin = os.path.join(app.config["IMAGES_REL"], str(id_collection), nom_fichier)

    chemin = os.path.normpath(chemin)

    return chemin


def créer_dossier(id_collection):
    os.mkdir(construire_chemin_dossier(id_collection))


def créer_fichier(id_collection, nom_fichier, fichier):
    fichier.save(construire_chemin_fichier(id_collection, nom_fichier))


def supprimer_dossier(id_collection):
    shutil.rmtree(construire_chemin_dossier(id_collection))


def supprimer_fichier(id_collection, nom_fichier):
    os.remove(construire_chemin_fichier(id_collection, nom_fichier))

