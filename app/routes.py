from app import app
from flask import render_template_string, render_template
from app.database import fetch_collections, fetch_collection


@app.route("/")
@app.route("/collections/")
def collections():
    étiquettes = fetch_collections()

    return render_template("oeuvres.html", étiquettes=étiquettes)


@app.route("/collections/<int:id_collection>")
@app.route("/collections/<int:id_collection>-<string:slug>")
def carousel(id_collection, slug=""):

    coll = fetch_collection(id_collection=id_collection)

    if coll:
        return render_template("carousel.html", carousel=coll, titre_page=coll.titre_collection)
    else:
        return render_template("page_inexistante.html", titre_page="Page inexistante")


@app.route("/contact/")
def contact():
    return render_template("contact.html")


@app.route("/publications/")
def publications():
    return render_template("publications.html")


@app.route("/publications/cabotageenarmor")
def carousel_cabotage():
    coll = fetch_collection(id_collection=8)

    if coll:
        return render_template("carousel.html", carousel=coll, titre_page=coll.titre_collection)
    else:
        return render_template("page_inexistante.html")


@app.route("/présentation/")
def présentation():
    return render_template("présentation.html")
