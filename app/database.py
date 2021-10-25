import sqlite3 as sl
import os


def connect_to_db(statement, many=True):
    with sl.connect("alemore.db") as conn:
        try:
            cur = conn.cursor()
            if many:
                res = cur.execute(statement).fetchall()
            else:
                res = cur.execute(statement).fetchone()
        except Exception as e:
            print(e)

    return res


class Étiquette:
    def __init__(self, titre_collection: str, id_collection: int):
        self.titre_collection = titre_collection
        self.slug = self.titre_collection.replace(".", "").translate(str.maketrans(" éèà", "-eeà")).lower()
        self.id_collection = id_collection
        self.src = os.path.normpath(os.path.join("/static/images/", str(id_collection), os.listdir("app/static/images/" + str(id_collection) + "/")[0]))


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


def fetch_collections():

    statement = f"SELECT titre, id_collection FROM collections WHERE est_une_serie=True;"
    coll_fetch = connect_to_db(statement=statement, many=True)

    étiquettes = [Étiquette(titre_collection=titre, id_collection=id) for titre, id in coll_fetch]

    return étiquettes


def fetch_collection(id_collection):

    statement = f"SELECT titre, description FROM collections WHERE id_collection={id_collection};"
    coll_fetch = connect_to_db(statement=statement, many=False)
    statement = f"SELECT titre, description, chemin FROM tableaux WHERE id_collection={id_collection};"
    paint_fetch = connect_to_db(statement=statement, many=True)

    if coll_fetch:
        coll = Collection(*coll_fetch)
        
        for titre, description, chemin in paint_fetch:
            coll.tableaux.append(Tableau(titre_tableau=titre, description_tableau=description, chemin=chemin))

        return coll

    else:
        return None
