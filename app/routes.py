from . import app
from flask import render_template, request, session, redirect, escape, url_for
from werkzeug.utils import secure_filename
from functools import wraps
from .models import Collection, Tableau


@app.errorhandler(404)
def ressource_inexistante(e):
    return render_template("page_inexistante.html"), 404


@app.route("/présentation")
def présentation():
    return render_template("présentation.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/")
@app.route("/collections")
def collections():
    colls = Collection.query\
        .filter_by(est_une_série=True)\
        .order_by(Collection.position)\
        .all()

    return render_template("collections.html", collections=colls)


@app.route("/collections/<int:id_collection>")
@app.route("/collections/<string:slug>")
def carousel(id_collection: int = None, slug: str = None):

    if slug:
        coll = Collection.query\
            .filter_by(slug=slug, est_une_série=True)\
            .first_or_404()
    else:
        coll = Collection.query.get_or_404(id_collection)

    return render_template("carousel.html", collection=coll)


@app.route("/publications")
def publications():
    return render_template("publications.html")


@app.route("/publications/<int:id_collection>")
@app.route("/publications/<string:slug>")
def carousel_publications(id_collection: int = None, slug: str = None):

    if slug:
        coll = Collection.query\
            .filter_by(slug=slug, est_une_série=False)\
            .first_or_404()
    else:
        coll = Collection.query.get_or_404(id_collection)

    return render_template("carousel.html", collection=coll)


@app.route("/connexion", methods=["GET", "POST"])
def connexion():
    if request.method == "POST":
        mot_de_passe = request.form.get("mot_de_passe")
        if mot_de_passe == app.config["PASSWORD"]:
            session["connecté"] = True
            return redirect(url_for("administration"))

        return redirect(request.url)

    return render_template("connexion.html")


def auth_demandée(page):
    @wraps(page)
    def vérifier(*args, **kwargs):
        if 'connecté' not in session:
            return redirect(url_for("connexion"))
        return page(*args, **kwargs)
    return vérifier


@app.route("/administration")
@auth_demandée
def administration():
    return render_template("administration.html")


@app.route("/administration/collections", methods=["GET"])
@auth_demandée
def admin_collections():

    colls = Collection.query\
        .filter_by(est_une_série=True)\
        .order_by(Collection.position)\
        .all()

    return render_template("admin_collections.html", collections=colls)


@app.route("/administration/collections/ajouter", methods=["POST"])
@auth_demandée
def admin_ajouter_collection():
    id_collection, position, titre, description, slug = formater_requête()

    coll = Collection(titre=titre,
                      slug=slug,
                      description=description)
    coll.position = coll.dernière_position() + 1
    coll.ajouter()

    return redirect(url_for("admin_collections"))


@app.route("/administration/collections/modifier", methods=["POST"])
@auth_demandée
def admin_modifier_collection():
    assert request.form["id_élément"]

    id_collection, position, titre, description, slug = formater_requête()

    coll = Collection.query.get_or_404(id_collection)

    if titre != coll.titre:
        coll.titre = titre
    if description != coll.description:
        coll.description = description
    if slug != coll.slug:
        coll.slug = slug

    positions = coll.toutes_les_positions
    if position:
        nouvelle = int(position)
        coll.position = définir_nouvelle_position(positions, coll.id, nouvelle)
    else:
        coll.position = positions[-1][0] + 1

    coll.sauvegarder()

    return redirect(url_for("admin_collections"))


@app.route("/administration/collections/supprimer", methods=["POST"])
@auth_demandée
def admin_supprimer_collection():
    assert request.form["id_élément"]

    coll = Collection.query.get_or_404(request.form["id_élément"])
    coll.supprimer()

    return redirect(url_for("admin_collections"))


@app.route("/administration/collections/<int:id_collection>", methods=["GET"])
@auth_demandée
def admin_tableaux(id_collection: int):

    coll = Collection.query.get_or_404(id_collection)

    return render_template("admin_tableaux.html", collection=coll)


@app.route("/administration/collections/<int:id_collection>/ajouter", methods=["POST"])
@auth_demandée
def admin_ajouter_tableau(id_collection: int):
    assert "tableau" in request.files
    assert request.files["tableau"].filename.lower().endswith(tuple(app.config.get("ALLOWED_EXTENSIONS")))

    id_tableau, position, titre, description, slug = formater_requête()
    nom_fichier = secure_filename(slug + ".jpg")

    tab = Tableau(titre=titre,
                  description=description,
                  collection_id=id_collection,
                  nom_fichier=nom_fichier)
    tab.position = tab.dernière_position + 1

    tab.ajouter(image_handle=request.files["tableau"])

    return redirect(url_for("admin_tableaux", id_collection=id_collection))


@app.route("/administration/collections/<int:id_collection>/modifier", methods=["POST"])
@auth_demandée
def admin_modifier_tableau(id_collection: int):
    assert request.form["id_élément"]

    id_tableau, position, titre, description, slug = formater_requête()

    tab = Tableau.query.get_or_404(id_tableau)

    if titre != tab.titre:
        tab.titre = titre
        nom_fichier = secure_filename(slug + ".jpg")
        tab.mettre_à_jour(nom_fichier)
        tab.nom_fichier = nom_fichier
    if description != tab.description:
        tab.description = description

    positions = tab.toutes_les_positions
    if position:
        nouvelle = int(position)
        tab.position = définir_nouvelle_position(positions, tab.id, nouvelle)
    else:
        tab.position = positions[-1][0] + 1

    tab.sauvegarder()

    return redirect(url_for("admin_tableaux", id_collection=id_collection))


@app.route("/administration/collections/<int:id_collection>/supprimer", methods=["POST"])
@auth_demandée
def admin_supprimer_tableau(id_collection: int):
    assert request.form["id_élément"]

    tab = Tableau.query.get_or_404(request.form["id_élément"])
    tab.supprimer()

    return redirect(url_for("admin_tableaux", id_collection=id_collection))


def définir_nouvelle_position(positions: list, id_élément: int, nouvelle: int) -> float:
    assert 0 <= nouvelle <= len(positions) - 1

    if positions[nouvelle][1] == id_élément:
        return positions[nouvelle][0]
    elif nouvelle == 0:
        return positions[0][0] - 1
    elif nouvelle == len(positions) - 1:
        return positions[-1][0] + 1
    else:
        return positions[nouvelle - 1][0] + (positions[nouvelle][0] - positions[nouvelle - 1][0]) / 2


def slugifier(titre: str) -> str:
    correspondances = {
        "é": "e", "è": "e", "à": "a", "ù": "u",
        "ê": "e", "î": "i", "â": "a", "û": "u", "ô": "o",
        "ï": "i", "ë": "e", "ü": "u",
        "œ": "oe", "æ": "ae", "ç": "c",
    }
    slug = titre
    slug = slug.lower()
    slug = slug.translate(str.maketrans(correspondances))
    slug = "".join(filter(lambda letter: letter.isascii() and (letter.isalnum() or letter.isspace()), slug))
    slug = slug.replace(" ", "-")
    return slug


def formater_requête():
    id_élément = request.form.get("id_élément", None)
    position = request.form.get("position", None)
    titre = escape(request.form.get("titre", "Sans titre").strip())
    description = escape(request.form.get("description", "").strip())
    slug = slugifier(request.form.get("titre", "Sans titre").strip())

    return id_élément, position, titre, description, slug
