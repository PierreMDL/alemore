from . import db
from .filesystem_actions import *


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

    def ajouter(self):
        db.session.add(self)
        db.session.flush()
        try:
            créer_dossier(self.id)
        except Exception as e:
            db.session.rollback()
            raise
        else:
            db.session.commit()

    def supprimer(self):
        db.session.delete(self)
        db.session.flush()
        try:
            supprimer_dossier(self.id)
        except Exception as e:
            db.session.rollback()
            raise
        else:
            db.session.commit()

    def sauvegarder(self):
        db.session.commit()

    @property
    def toutes_les_positions(self):
        q = Collection.query \
            .filter_by(est_une_série=True) \
            .with_entities(Collection.position, Collection.id) \
            .order_by(Collection.position) \
            .all()
        return q

    def dernière_position(self):
        q = Collection.query \
            .filter_by(est_une_série=True) \
            .with_entities(Collection.position) \
            .order_by(Collection.position.desc()) \
            .first()
        return q[0] if q else 0


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

    def ajouter(self, image_handle):
        db.session.add(self)
        db.session.flush()

        try:
            créer_fichier(self, image_handle)
        except Exception as e:
            db.session.rollback()
            raise
        else:
            db.session.commit()

    def mettre_à_jour(self, nouveau_nom_fichier):
        mettre_à_jour_fichier(self, nouveau_nom_fichier)

    def supprimer(self):
        db.session.delete(self)
        db.session.flush()
        try:
            supprimer_fichier(self.collection_id, self.nom_fichier)
        except Exception as e:
            db.session.rollback()
            raise
        else:
            db.session.commit()

    def sauvegarder(self):
        db.session.commit()

    @property
    def toutes_les_positions(self):
        q = Tableau.query \
            .filter_by(collection_id=self.collection_id) \
            .with_entities(Tableau.position, Tableau.id) \
            .order_by(Tableau.position) \
            .all()
        return q

    @property
    def dernière_position(self):
        q = self.query \
            .filter_by(collection_id=self.collection_id) \
            .with_entities(Tableau.position) \
            .order_by(Tableau.position.desc()) \
            .first()
        return q[0] if q else 0
