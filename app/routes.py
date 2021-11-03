from app import app, database_actions, filesystem_actions, inputoutput_actions
from flask import render_template, request, session, redirect, escape
from werkzeug.utils import secure_filename


@app.route("/")
@app.route("/collections/")
def collections():
    étiquettes = database_actions.obtenir_étiquettes()

    return render_template("collections.html", étiquettes=étiquettes)


@app.route("/collections/<int:id_collection>")
@app.route("/collections/<string:slug>")
def carousel(id_collection: int = None, slug: str = None):

    coll = database_actions.obtenir_collection(id_collection=id_collection, slug=slug)

    if coll:
        return render_template("carousel.html", carousel=coll, titre_page=coll.titre)
    else:
        return render_template("page_inexistante.html", titre_page="Page inexistante")


@app.route("/contact/")
def contact():
    return render_template("contact.html")


@app.route("/publications/")
def publications():
    return render_template("publications.html")


@app.route("/publications/cabotage-en-armor")
def carousel_cabotage():
    coll = database_actions.obtenir_collection(slug="cabotage-en-armor")

    if coll:
        return render_template("carousel.html", carousel=coll, titre_page=coll.titre)
    else:
        return render_template("page_inexistante.html")


@app.route("/présentation/")
def présentation():
    return render_template("présentation.html")


@app.route("/connexion/", methods=["POST", "GET"])
def connexion():
    if request.method == "POST":
        password = request.form.get("password")
        if password == app.config.get("PASSWORD"):
            session["user"] = "admin"
            return redirect("/administration")
        return redirect("/connexion")

    return render_template("connexion.html")


@app.route("/déconnexion/")
def déconnexion():
    if "user" in session:
        session.pop("user")

    return redirect("/connexion/")


@app.route("/administration/")
def administration():
    if not ("user" in session and session["user"] == "admin"):
        return redirect("/connexion/")

    return render_template("administration.html")


@app.route("/administration/collections/", methods=["GET", "POST"])
def admin_collections():
    if not ("user" in session and session["user"] == "admin"):
        return redirect("/connexion/")

    if request.method == "POST":
        assert request.form["action"]

        titre = inputoutput_actions.formater_titre(request.form["titre"])
        description = inputoutput_actions.formater_description(request.form["description"])
        slug = inputoutput_actions.slugifier(titre)

        if request.form["action"] == "Mettre à jour":
            id_collection = request.form["id_collection"]
            position = request.form["position"]
            database_actions.modifier_collection(id_collection=id_collection, titre=titre, slug=slug, description=description, position=position)

        elif request.form["action"] == "Supprimer":
            id_collection = request.form["id_collection"]
            database_actions.supprimer_collection(id_collection)
            filesystem_actions.supprimer_dossier(id_collection)

        elif request.form["action"] == "Ajouter":
            id_collection = database_actions.créer_collection(titre, slug, description)
            filesystem_actions.créer_dossier(id_collection)

    étiquettes = database_actions.obtenir_étiquettes_admin()

    return render_template("admin_collections.html", étiquettes=étiquettes)


@app.route("/administration/collections/<int:id_collection>", methods=["GET", "POST"])
def admin_tableaux(id_collection):

    if not ("user" in session and session["user"] == "admin"):
        return render_template("administration.html")

    if request.method == "POST":
        assert request.form["action"]

        titre = inputoutput_actions.formater_titre(request.form["titre"]) or "Sans titre"
        description = inputoutput_actions.formater_description(request.form["description"])

        if request.form["action"] == "Mettre à jour":
            id_tableau = request.form["id_tableau"]
            position = request.form["position"]
            database_actions.modifier_tableau(id_collection=id_collection, id_tableau=id_tableau, titre=titre, description=description, position=position)

        elif request.form["action"] == "Supprimer":
            id_tableau = request.form["id_tableau"]
            id_collection, nom_fichier = database_actions.supprimer_tableau(id_tableau)
            filesystem_actions.supprimer_fichier(id_collection, nom_fichier)

        elif request.form["action"] == "Ajouter":
            assert "tableau" in request.files
            assert request.files["tableau"].filename.lower().endswith((".jpg", ".jpeg"))

            tableau = request.files["tableau"]

            nom_fichier = secure_filename(tableau.filename)

            filesystem_actions.créer_fichier(id_collection, nom_fichier, tableau)

            database_actions.créer_tableau(titre=titre, description=description, id_collection=id_collection, chemin=nom_fichier)

    coll = database_actions.obtenir_collection(id_collection=id_collection)

    return render_template("admin_tableaux.html", collection=coll)
