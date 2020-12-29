from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()

# This table's for many-to-many relationship (user-dish: upvote)
upvote = db.Table('upvote',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('dish_id', db.Integer, db.ForeignKey('dish.id'), primary_key=True)
)
savelist = db.Table('save',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('dish_id', db.Integer, db.ForeignKey('dish.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    save = db.relationship('Dish', secondary="save", backref="who_save")
    # This column is used to control one-to-many rela (user-dish: contributor)
    dishes = db.relationship('Dish', backref="contributor")
    
    def __repr__(self):
        return '<User %r>' % self.username

# This table is for many-to many relationship (dish-ingredient) 
relation = db.Table('relation',
    db.Column('dish_id', db.Integer, db.ForeignKey('dish.id'), primary_key=True),
    db.Column('ingre_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
)

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_name = db.Column(db.String(1000), nullable=False)

    # this column controls many to many relationship (upvote)
    # backref is not nessesary, we dont wanna know which dishes are upvoted by an user
    upvoters = db.relationship('User', secondary=upvote)
    upvote_count = db.Column(db.Integer, default=0)
    # this col is used to control one-to-many rela (user-dish: contributor)
    user_contri = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # this is used to control many-to-many rela Dish-Ingredient
    ingredients = db.relationship('Ingredient', secondary=relation, lazy='subquery', backref=db.backref('dishes', lazy = True))
    procedure = db.Column(db.String(3000), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'dish_name': self.dish_name,
            'contributor': {'name': self.contributor.username, 'uid': self.contributor.id},
            'upvote_count': self.upvote_count,
            'ingredient': [i.serialize for i in self.ingredients]
        }

    @property
    def serialize_many2many(self):
        return []

    def __repr__(self):
        return self.dish_name

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingre_name = db.Column(db.String(1000), nullable=False)
        # dishes = db.re

    @property
    def serialize(self):
        return {
            'id': self.id,
            'ingre_name': self.ingre_name,
        }

    def __repr__(self):
        return self.ingre_name