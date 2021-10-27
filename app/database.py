import sqlite3 as sl

from .models import Étiquette, AdminÉtiquette, Collection, Tableau


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
            return e

    return res


def fetch_collections():

    statement = f"SELECT titre, slug, id_collection, position FROM collections WHERE est_une_serie=True ORDER BY position;"
    coll_fetch = connect_to_db(statement=statement, many=True)

    étiquettes = [Étiquette(titre_collection=titre, slug=slug, id_collection=id_collection, position=position) for titre, slug, id_collection, position in coll_fetch]

    return étiquettes


def fetch_admin_collections():

    statement = f"SELECT titre, description, id_collection, position FROM collections WHERE est_une_serie=True ORDER BY position;"
    coll_fetch = connect_to_db(statement=statement, many=True)

    étiquettes = [AdminÉtiquette(titre_collection=titre, description_collection=description, id_collection=id_collection, position=position) for titre, description, id_collection, position in coll_fetch]

    return étiquettes


def fetch_collection(id_collection: int = None, slug: str = None):
    assert id_collection or slug

    if id_collection:
        statement = f"SELECT id_collection, titre, description FROM collections WHERE id_collection={id_collection};"
    else:
        statement = f"SELECT id_collection, titre, description FROM collections WHERE slug='{slug}';"
    coll_fetch = connect_to_db(statement=statement, many=False)

    if coll_fetch:
        coll = Collection(*coll_fetch)

    else:
        return None

    statement = f"SELECT id_tableau, titre, description, chemin FROM tableaux WHERE id_collection={coll.id};"
    paint_fetch = connect_to_db(statement=statement, many=True)

    if coll_fetch:
        coll = Collection(*coll_fetch)
        
        for id_tableau, titre, description, chemin in paint_fetch:
            coll.tableaux.append(Tableau(id_tableau=id_tableau, titre_tableau=titre, description_tableau=description, chemin=chemin))

        return coll


def update_collection(id_collection, titre, description):

    slug = titre.replace(".", "").translate(str.maketrans(" éèà", "-eeà")).lower()
    statement = f"UPDATE collections SET titre='{titre}', slug='{slug}', description='{description}' WHERE id_collection={id_collection};"
    coll_update = connect_to_db(statement, many=False)

    return coll_update


def update_painting(id_tableau, titre, description):
    statement = f"UPDATE tableaux SET titre='{titre}', description='{description}' WHERE id_tableau={id_tableau};"
    paint_update = connect_to_db(statement, many=False)

    return paint_update
