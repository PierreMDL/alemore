from app import app, filesystem_actions, db
from flask import render_template, request, session, redirect, escape, url_for
from werkzeug.utils import secure_filename
from functools import wraps
from .models import Collection, Tableau


@app.errorhandler(404)
def page_non_trouvée(e):
    return render_template("page_inexistante.html")


@app.route("/présentation")
def présentation():
    return render_template("présentation.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/")
@app.route("/collections")
def collections():
    colls = Collection.query.filter_by(est_une_série=True).order_by(Collection.position).all()

    return render_template("collections.html", collections=colls)


@app.route("/collections/<int:id_collection>")
@app.route("/collections/<string:slug>")
def carousel(id_collection: int = None, slug: str = None):

    if slug:
        coll = Collection.query.filter_by(slug=slug).first_or_404()
    else:
        coll = Collection.query.get_or_404(id_collection)

    return render_template("carousel.html", collection=coll)


@app.route("/publications")
def publications():
    return render_template("publications.html")


@app.route("/publications/cabotage-en-armor")
def carousel_cabotage():
    coll = Collection.query.filter_by(slug="cabotage-en-armor").first_or_404()

    return render_template("carousel.html", collection=coll)


@app.route("/connexion", methods=["GET", "POST"])
def connexion():
    if request.method == "POST":
        mot_de_passe = request.form.get("mot_de_passe")
        if mot_de_passe == app.config["PASSWORD"]:
            session["connecté"] = True
            return redirect(url_for("administration"))

        return redirect(url_for("connexion"))

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


@app.route("/administration/collection", methods=["GET", "POST"])
@auth_demandée
def admin_collections():
    if request.method == "POST":
        assert request.form["action"]

        id_collection = request.form.get("id_collection", None)
        position = request.form.get("position", None)
        titre = formater_texte(request.form["titre"]) or "Sans titre"
        description = formater_texte(request.form["description"])
        slug = slugifier(titre)

        if request.form["action"] == "Mettre à jour":
            assert id_collection

            collection = Collection.query.get_or_404(id_collection)
            positions = Collection.query.filter_by(est_une_série=True).with_entities(Collection.position, Collection.id).order_by(Collection.position).all()

            mettre_à_jour(collection, titre, description, position, positions, slug=slug)

        elif request.form["action"] == "Supprimer":
            assert id_collection

            coll = Collection.query.get_or_404(id_collection)

            db.session.delete(coll)
            filesystem_actions.supprimer_dossier(coll.id)
            db.session.commit()

        elif request.form["action"] == "Ajouter":

            dernière_position = Collection.query.filter_by(est_une_série=True).with_entities(Collection.position).order_by(Collection.position.desc()).first()
            dernière_position = (dernière_position[0] if dernière_position else 0) + 1
            coll = Collection(titre=titre, slug=slug, description=description, position=dernière_position)

            db.session.add(coll)
            filesystem_actions.créer_dossier(coll.id)
            db.session.commit()

    colls = Collection.query.filter_by(est_une_série=True).order_by(Collection.position).all()

    return render_template("admin_collections.html", collections=colls)


@app.route("/administration/collections/<int:id_collection>", methods=["GET", "POST"])
@auth_demandée
def admin_tableaux(id_collection: int):
    if request.method == "POST":
        assert request.form["action"]

        id_tableau = request.form.get("id_tableau", None)
        position = request.form.get("position", None)
        titre = formater_texte(request.form.get("titre", "Sans titre"))
        description = formater_texte(request.form.get("description", ""))

        if request.form["action"] == "Mettre à jour":
            assert id_tableau

            tableau = Tableau.query.get_or_404(id_tableau)
            positions = Tableau.query.filter_by(collection_id=id_collection).with_entities(Tableau.position, Tableau.id).order_by(Tableau.position).all()

            mettre_à_jour(tableau, titre, description, position, positions)

        elif request.form["action"] == "Supprimer":
            assert id_tableau

            tableau = Tableau.query.get_or_404(id_tableau)

            db.session.delete(tableau)
            filesystem_actions.supprimer_fichier(tableau.collection_id, tableau.nom_fichier)
            db.session.commit()

        elif request.form["action"] == "Ajouter":
            assert "tableau" in request.files
            assert request.files["tableau"].filename.lower().endswith((".jpg", ".jpeg"))

            image = request.files["tableau"]

            nom_fichier = secure_filename(image.filename)

            dernière_position = Tableau.query.filter_by(collection_id=id_collection).with_entities(Tableau.position).order_by(Tableau.position.desc()).first()
            dernière_position = (dernière_position[0] if dernière_position else 0) + 1
            tableau = Tableau(titre=titre, description=description, collection_id=id_collection, nom_fichier=nom_fichier, position=dernière_position)

            db.session.add(tableau)
            filesystem_actions.créer_fichier(id_collection, nom_fichier, image)
            db.session.commit()

    coll = Collection.query.get_or_404(id_collection)

    return render_template("admin_tableaux.html", collection=coll)


def définir_nouvelle_position(positions: list, id_collection: int, nouvelle: int) -> float:
    assert 0 <= nouvelle <= len(positions) - 1

    if positions[nouvelle][1] == id_collection:
        return positions[nouvelle][0]
    elif nouvelle == 0:
        return positions[0][0] - 1
    elif nouvelle == len(positions) - 1:
        return positions[-1][0] + 1
    else:
        return positions[nouvelle - 1][0] + (positions[nouvelle][0] - positions[nouvelle - 1][0]) / 2


def mettre_à_jour(élément, titre: str, description: str, position: str, positions: list, slug: str = None):
    if titre != élément.titre:
        élément.titre = titre
    if description != élément.description:
        élément.description = description
    if slug and (slug != élément.slug):
        élément.slug = slug
    if position:
        nouvelle = int(position)
        élément.position = définir_nouvelle_position(positions, élément.id, nouvelle)
    else:
        élément.position = positions[-1][0] + 1
    db.session.commit()


def formater_texte(texte: str) -> str:
    return escape(texte).strip()


def slugifier(titre: str) -> str:
    slug = titre.replace(".", "").translate(str.maketrans(" éèà", "-eeà")).lower()
    return slug

