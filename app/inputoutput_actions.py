from flask import escape


def slugifier(titre: str):
    slug = titre.replace(".", "").translate(str.maketrans(" éèà", "-eeà")).lower()
    return slug


def échapper(texte: str):
    return escape(texte)


# TODO - trouver comment déséchapper efficacement les caractères spéciaux
def déséchapper(texte: str):
    texte = texte.replace("&#39;", "'")
    return texte


def formater_description(description: str):
    description = description.strip()
    description = échapper(description)
    return description


def formater_titre(titre: str):
    titre = échapper(titre)
    return titre


def déformater_description(description: str):
    description = déséchapper(description)
    description = description.split("\n")
    return description


def déformater_titre(titre: str):
    titre = déséchapper(titre)
    return titre
