from app import app
from flask import render_template, request, session, redirect
from app.database import fetch_collections, fetch_collection, update_collection, update_painting, fetch_admin_collections


@app.route("/")
@app.route("/collections/")
def collections():
    étiquettes = fetch_collections()

    return render_template("collections.html", étiquettes=étiquettes)


@app.route("/collections/<int:id_collection>")
@app.route("/collections/<string:slug>")
def carousel(id_collection: int = None, slug: str = None):

    coll = fetch_collection(id_collection=id_collection, slug=slug)

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
    coll = fetch_collection(slug="cabotage-en-armor")

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
        assert request.form["titre"]
        assert request.form["id_collection"]

        update_collection(request.form["id_collection"], request.form["titre"], request.form["description"])

    étiquettes = fetch_admin_collections()

    return render_template("admin_collections.html", étiquettes=étiquettes)


@app.route("/administration/collections/<int:id_collection>", methods=["GET", "POST"])
def admin_collection(id_collection):

    if not ("user" in session and session["user"] == "admin"):
        return render_template("administration.html")

    if request.method == "POST":
        assert request.form["titre"]
        assert request.form["id_tableau"]

        update_painting(request.form["id_tableau"], request.form["titre"], request.form["description"])

    coll = fetch_collection(id_collection=id_collection)

    return render_template("admin_collection.html", collection=coll)
