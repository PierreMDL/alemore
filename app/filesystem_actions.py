from PIL import Image
import os, shutil, piexif
from app import app


def construire_chemin_dossier(id_collection, from_root=True):
    if from_root:
        chemin = os.path.join(app.config["IMAGES_FOLDER"], str(id_collection))
    else:
        chemin = os.path.join(app.config["IMAGES_SRC"], str(id_collection))

    chemin = os.path.normpath(chemin)

    return chemin


def construire_chemin_fichier(id_collection, nom_fichier, from_root=True):
    if from_root:
        chemin = os.path.join(app.config["IMAGES_FOLDER"], str(id_collection), nom_fichier)
    else:
        chemin = os.path.join(app.config["IMAGES_SRC"], str(id_collection), nom_fichier)

    chemin = os.path.normpath(chemin)

    return chemin


def générer_exif(titre, exif=None):
    tags = {
        270: titre.encode(),  # ExifTags id pour ImageDescription
        315: "Arlette Le More",  # ExifTags id pour Artist
    }

    if exif:
        exif.get("0th").update(tags)
    else:
        exif = {"0th": tags}
    return piexif.dump(exif)


def resize_image(image):
    hauteur_max, largeur_max = app.config.get("MAX_CONTENT_SIZE")
    largeur, hauteur = image.size
    if (hauteur >= largeur) and (hauteur > hauteur_max):
        ratio = (largeur/hauteur)*100
        return image.resize((int(hauteur_max*(ratio/100)), hauteur_max))
    elif (largeur >= hauteur) and (largeur > largeur_max):
        ratio = (hauteur/largeur)*100
        return image.resize((largeur_max, int(largeur_max*(ratio/100))))
    else:
        return image


def créer_dossier(id_collection):
    os.mkdir(construire_chemin_dossier(id_collection))


def créer_fichier(tableau, image_handle):
    with Image.open(image_handle, "r") as image:
        image = resize_image(image)
        chemin = construire_chemin_fichier(tableau.collection_id, tableau.nom_fichier)
        exif = image.info.get("exif")
        exif = générer_exif(tableau.titre, piexif.load(exif) if exif else None)
        image.save(chemin, "jpeg", exif=exif)


def supprimer_dossier(id_collection):
    shutil.rmtree(construire_chemin_dossier(id_collection))


def supprimer_fichier(id_collection, nom_fichier):
    os.remove(construire_chemin_fichier(id_collection, nom_fichier))


def mettre_à_jour_fichier(tableau, nouveau_nom_fichier):
    chemin = construire_chemin_fichier(tableau.collection_id, tableau.nom_fichier)
    nouveau_chemin = construire_chemin_fichier(tableau.collection_id, nouveau_nom_fichier)

    with Image.open(chemin) as image:
        exif = générer_exif(tableau.titre, piexif.load(image.info["exif"]))
        image.save(chemin, "jpeg", exif=exif)
        os.rename(chemin, nouveau_chemin)
