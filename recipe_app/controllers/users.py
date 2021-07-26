from recipe_app import app
from flask import render_template, request, redirect, session
from flask_bcrypt import Bcrypt
from recipe_app.models.user import User

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')

    hashed_password = bcrypt.generate_password_hash(request.form['password'])

    data = {
    "first_name": request.form["first_name"],
    "last_name": request.form["last_name"],
    "email": request.form["email"],
    "password": hashed_password
    }

    session['userid']= User.save(data)
    return redirect('/main_page')

@app.route('/login', methods=['POST'])
def login():
    login_validation = User.validate_login(request.form)

    if not login_validation:
        return redirect('/')

    session['user_id'] = login_validation.id
    return redirect('/main_page')

@app.route('/main_page')
def main_page():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : session['user_id']
    }

    logged_in_user = User.get_user_by_id(data)
    if logged_in_user == False:
        return redirect ('/')
    
    return render_template('main.html', user=logged_in_user)


