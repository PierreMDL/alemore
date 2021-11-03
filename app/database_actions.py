import sqlite3 as sl

from .models import Étiquette, AdminÉtiquette, Collection, Tableau


def définir_nouvelle_position(positions, id_collection, nouvelle):
    assert 0 <= nouvelle <= len(positions) - 1

    if positions[nouvelle][1] == id_collection:
        return positions[nouvelle][0]
    elif nouvelle == 0:
        return positions[0][0] - 1
    elif nouvelle == len(positions) - 1:
        return positions[-1][0] + 1
    else:
        return positions[nouvelle - 1][0] + (positions[nouvelle][0] - positions[nouvelle - 1][0]) / 2


def connecter_bdd(statement, many=True):
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


def obtenir_étiquettes():

    statement = f"SELECT titre, slug, id_collection, position FROM collections WHERE est_une_serie=True ORDER BY position;"
    coll_fetch = connecter_bdd(statement=statement, many=True)

    étiquettes = [Étiquette(titre_collection=titre, slug=slug, id_collection=id_collection, position=position) for titre, slug, id_collection, position in coll_fetch]

    return étiquettes


def obtenir_étiquettes_admin():

    statement = f"SELECT titre, description, id_collection, position FROM collections WHERE est_une_serie=True ORDER BY position;"
    coll_fetch = connecter_bdd(statement=statement, many=True)

    étiquettes = [AdminÉtiquette(titre_collection=titre, description_collection=description, id_collection=id_collection, position=position) for titre, description, id_collection, position in coll_fetch]

    return étiquettes


def obtenir_collection(id_collection: int = None, slug: str = None):
    assert id_collection or slug

    if id_collection:
        statement = f"SELECT id_collection, titre, description FROM collections WHERE id_collection={id_collection};"
    else:
        statement = f"SELECT id_collection, titre, description FROM collections WHERE slug='{slug}';"
    coll_fetch = connecter_bdd(statement=statement, many=False)

    if coll_fetch:
        coll = Collection(*coll_fetch)

    else:
        return None

    statement = f"SELECT id_tableau, titre, description, chemin FROM tableaux WHERE id_collection={coll.id} ORDER BY position;"
    paint_fetch = connecter_bdd(statement=statement, many=True)

    if coll_fetch:
        coll = Collection(*coll_fetch)
        
        for id_tableau, titre, description, nom_fichier in paint_fetch:
            coll.tableaux.append(Tableau(id_tableau=id_tableau, titre_tableau=titre, description_tableau=description, id_collection=coll.id, nom_fichier=nom_fichier))

        return coll


def modifier_collection(id_collection, titre, slug, description, position):
    statement = f"SELECT position, id_collection FROM collections WHERE est_une_serie=True ORDER BY position;"
    positions = connecter_bdd(statement, many=True)

    if position:
        définir_nouvelle_position(positions, id_collection, nouvelle=int(position))
    else:
        position = positions[-1][0] + 1

    statement = f"UPDATE collections SET titre='{titre}', slug='{slug}', description='{description}', position={position} WHERE id_collection={id_collection};"
    coll_update = connecter_bdd(statement, many=False)

    return coll_update


def modifier_tableau(id_collection, id_tableau, titre, description, position):
    statement = f"SELECT position, id_tableau FROM tableaux WHERE id_collection={id_collection} ORDER BY position;"
    positions = connecter_bdd(statement, many=True)

    if position:
        définir_nouvelle_position(positions, id_tableau, nouvelle=int(position))
    else:
        position = positions[-1][0] + 1

    statement = f"UPDATE tableaux SET titre='{titre}', description='{description}', position={position} WHERE id_tableau={id_tableau};"
    paint_update = connecter_bdd(statement, many=False)

    return paint_update


def créer_tableau(titre, description, id_collection, chemin):
    statement = f"INSERT INTO tableaux (titre, description, id_collection, chemin, position) VALUES ('{titre}', '{description}', {id_collection}, '{chemin}', 0);"
    paint_create = connecter_bdd(statement, many=False)

    return paint_create


def supprimer_tableau(id_tableau):
    statement = f"DELETE FROM tableaux WHERE id_tableau={id_tableau} RETURNING id_collection, chemin;"
    chemin = connecter_bdd(statement, many=False)

    return chemin


def supprimer_collection(id_collection):
    statement = f"DELETE FROM tableaux WHERE id_collection={id_collection};"
    connecter_bdd(statement, many=True)
    statement = f"DELETE FROM collections WHERE id_collection={id_collection};"
    coll_delete = connecter_bdd(statement, many=False)

    return coll_delete


def créer_collection(titre, slug, description):
    statement = f"SELECT MAX(position) FROM collections WHERE est_une_serie=True;"
    dernière_position = connecter_bdd(statement, many=False)
    position = dernière_position[0]  + 1

    statement = f"INSERT INTO collections (titre, description, slug, position) VALUES ('{titre}', '{description}', '{slug}', {position}) RETURNING id_collection;"
    id_collection = connecter_bdd(statement, many=False)
    return id_collection[0]
