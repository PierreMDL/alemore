import sqlite3 as sl

from app.models import Étiquette, AdminÉtiquette, Collection, Tableau


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


def fetch_collections():

    statement = f"SELECT titre, id_collection, position FROM collections WHERE est_une_serie=True ORDER BY position;"
    coll_fetch = connect_to_db(statement=statement, many=True)

    étiquettes = [Étiquette(titre_collection=titre, id_collection=id_collection, position=position) for titre, id_collection, position in coll_fetch]

    return étiquettes


def fetch_admin_collections():

    statement = f"SELECT titre, description, id_collection, position FROM collections WHERE est_une_serie=True ORDER BY position;"
    coll_fetch = connect_to_db(statement=statement, many=True)

    étiquettes = [AdminÉtiquette(titre_collection=titre, description_collection=description, id_collection=id_collection, position=position) for titre, description, id_collection, position in coll_fetch]

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


def update_collection(id_collection, titre, description):
    statement = f"UPDATE collections SET titre='{titre}', description='{description}' WHERE id_collection={id_collection};"
    coll_update = connect_to_db(statement, many=False)

    return coll_update
