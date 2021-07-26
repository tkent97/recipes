from flask import render_template, redirect, request
from recipe_app import app
from flask import Bcrypt
from recipe_app.models.recipe import Recipe

@app.route('/recipes/<int:id>')
def show_recipe(id):
    selected = Recipe.get_recipe(id)
    return render_template('show.html', selected_recipe=selected)


@app.route('/recipes/edit/<int:id>')
def edit(id):
    selected = Recipe.get_one(id)
    return render_template('show.html', selected_recipe=selected)


@app.route('/edit/<int:id>', methods=['POST'])
def edit_recipe(id):
    data = {
        'id': id,
        'name': request.form['name'],
        'instructions': request.form['instructions'],
        'description': request.form['description'],
        'time_limit': request.form['time_limit'],
        'created_at': request.form['created_at']
    }
    Recipe.edit_recipe(data)
    return redirect('/recipes/%i' % id)
