import os

import click
from flask.cli import with_appcontext

from flask import Flask, render_template, g, request, session

from .models import db, User, Dish, Ingredient
from . import dbcontrol
from flask_migrate import Migrate, MigrateCommand



migrate = Migrate(compare_type=True)
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # Prepare for SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:asdasd123@localhost:5432/dishes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
)
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register Blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    from . import dish
    app.register_blueprint(dish.dish)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def index():
        dishes = Dish.query.order_by(Dish.id.desc()).limit(5).all()
        count = len(dishes)
        # print(g.user.dishes)
        # hihi = Ingredient.query.get(3)
        # print(hihi.dishes)
        # print(hi.ingredients)
        # print(hi.contributor)
        return render_template('index.html', dishes=dishes, count=count)
        # return 'render_template('

    # Start and clear DB connection?
    from . import dbcontrol
    dbcontrol.init_app(app)

    # @click.command(name="create")
    # @with_appcontext
    # def create():
    #     db.create_all()

    # app.cli.add_command(create)


    return app

