from db import db


class RecipeModel(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    ingredients = db.Column(db.String(80))
    method = db.Column(db.String(80))

    def __init__(self, name, ingredients, method):
        self.name = name
        self.ingredients = ingredients
        self.method = method

    def json(self):
        return {'name': self.name, 'ingredients': self.ingredients, 'method': self.method}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
