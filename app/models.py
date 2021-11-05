from . import db
from .filesystem_actions import construire_chemin_fichier


class Collection(db.Model):
    __tablename__ = "collections"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titre = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    slug = db.Column(db.String(255), nullable=False)
    position = db.Column(db.Float)
    est_une_série = db.Column(db.Boolean, default=True)
    tableaux = db.relationship("Tableau", cascade="all,delete", backref="collection", order_by="Tableau.position")

    def __repr__(self):
        return f"<Collection {self.titre} ({self.id})>"

    @property
    def src(self):
        if self.tableaux:
            return self.tableaux[0].src
        else:
            return construire_chemin_fichier("", "placeholder.jpg", from_root=False)


class Tableau(db.Model):
    __tablename__ = "tableaux"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titre = db.Column(db.String(255), nullable=True, default="Sans titre")
    description = db.Column(db.Text)
    position = db.Column(db.Float)
    collection_id = db.Column(db.Integer, db.ForeignKey(Collection.id), nullable=False)
    nom_fichier = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Tableau {self.titre} ({self.id})>"

    @property
    def src(self):
        return construire_chemin_fichier(self.collection_id, self.nom_fichier, from_root=False)
