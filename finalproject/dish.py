from flask import (
    Blueprint, g, session, render_template, redirect, url_for, request, flash, jsonify
)
from .auth import login_required
from .models import Dish, Ingredient, db
import math

dish = Blueprint("dish", __name__)


@dish.route('/contribute', methods=("GET", "POST"))
@login_required
def contribute():
    if request.method == "POST":
        dish_name = request.form['dish_name']
        ingredients = request.form['ingredients']
        procedure = request.form['procedure']
        print(ingredients.split(','))
        print(g.user.id)
        new_dish = Dish(dish_name=dish_name.capitalize(), procedure=procedure, contributor=g.user)
        db.session.add(new_dish)
        db.session.commit()
        for ingredient in ingredients.split(','):
            ingredient = ingredient.strip().lower()
            ingre = Ingredient.query.filter_by(ingre_name=ingredient).first()
            if ingre is None:
                new_ingre = Ingredient(ingre_name=ingredient)
                db.session.add(new_ingre)
                # db.seesion.commit()
                new_dish.ingredients.append(new_ingre)
            else:
                new_dish.ingredients.append(ingre)
        db.session.commit()

        return redirect(url_for('dish.detail', dish_id=new_dish.id))

    return render_template('contribute.html')

@dish.route('/detail/<int:dish_id>')
def detail(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    # dish.upvote = len(dish.upvoters)
    return render_template('/dish/detail.html', dish=dish)

@dish.route('/detail/<int:dish_id>/upvote')
@login_required
def upvote(dish_id):
    dish = Dish.query.get(dish_id)
    if (g.user in dish.upvoters):
        return redirect(url_for('dish.detail', dish_id=dish_id))
    else:
        dish.upvoters.append(g.user)
        dish.upvote_count += 1
        db.session.commit()
        return redirect(url_for('dish.detail', dish_id=dish_id))

@dish.route('/ingredients')
def ingre():
    ingre = Ingredient.query.order_by('ingre_name').all()
    n = math.ceil(len(ingre)/4)
    print(n)    
    print(ingre[0:n], ingre[n:2*n], ingre[2*n:3*n], ingre[3*n:])
    return render_template('ingredients.html',
        ingre = [ingre[0:n], ingre[n:2*n], ingre[2*n:3*n], ingre[3*n:]],
        # ingre1 = ingre[0:n],
        # ingre2 = ingre[n:2*n],
        # ingre3 = 
        # ingre4 = ,
        page="Ingredients"
    )

@dish.route('/dishforingre/<int:ingre_id>')   
def dishforingre(ingre_id):
    ingre = Ingredient.query.get(ingre_id)
    return render_template('index.html', dishes=ingre.dishes, page=f"Dishes with: {ingre}")

@dish.route('/text')
def test():
    # dishes = Dish.query.all()
    # print(dishes)
    # newlist = [dish.serialize for dish in dishes]
    # hi = jsonify(newlist)
    # print(newlist)
    print(g.user.save)

    return redirect(url_for('index'))

@dish.route('/search')
def search():
    search_string = request.args.get('search_string').strip()
    search_type = request.args.get('type')
    filter_by = request.args.get('filter')
    print(search_string == "")
    print(search_type, filter_by)
    dishes = []
    error = None
    if search_string == "" or search_type == None or filter_by == None:
        flash('Please give us enough information for searching.')
    else:
        search_string = '%' + request.args['search_string'] + '%'
        if (search_type == "ingredient"):
            # dishes = Ingredient.query.filter(Ingredient.ingre_name.like(search_string)).order_by(Dish.upvote_count.desc()).all()
            ingredients = Ingredient.query.filter(Ingredient.ingre_name.ilike(search_string)).all()
            for i in ingredients:
                dishes = dishes + i.dishes
            if filter_by == "upvote":
                dishes.sort(reverse=True, key=lambda k: k.upvote_count)
            else:
                dishes.sort(reverse=True, key=lambda k: k.id)
        else:
            dishes = Dish.query.filter(Dish.dish_name.like(search_string)).all()
            if filter_by == "upvote":
                dishes.sort(reverse=True, key=lambda k: k.upvote_count)
            else:
                dishes.sort(reverse=True, key=lambda k: k.id)
        if len(dishes) == 0:
            error = "No match found"
            flash(error)
    return render_template('index.html', dishes=dishes)

# Loadmore API
@dish.route('/loadmore/<int:skip_number>', methods=['GET'])
def loadmore(skip_number):
    print(skip_number)
    dishes = Dish.query.order_by(Dish.id.desc()).offset(skip_number).limit(5).all()
    newlist = [dish.serialize for dish in dishes]

    print(dishes)
    if dishes:
        hihi = render_template('test.html', dishes=dishes)
        print(hihi)
        return (hihi)
    else:
        return "No more dish."

@dish.route('/save/<int:dish_id>', methods=["GET"])
@login_required
def save(dish_id):
    dish = Dish.query.get(dish_id)
    g.user.save.append(dish)
    db.session.commit()
    return redirect(url_for('dish.detail', dish_id=dish_id))

@dish.route('/unsave/<int:dish_id>', methods=["GET"])
@login_required
def unsave(dish_id):
    dish = Dish.query.get(dish_id)
    g.user.save.remove(dish)
    db.session.commit()
    return redirect(url_for('dish.detail', dish_id=dish_id))
@dish.route('/savelist')
@login_required
def savelist():
    return render_template('index.html', dishes=g.user.save, page="Saved Dishes")