from recipe_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from recipe_app import app
bcrypt = Bcrypt(app)
import re

LETTERS_ONLY_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, updated_at, created_at) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('login').query_db(query,data)
        

    @classmethod
    def is_email_not_in_database(cls, data):
        query = "SELECT * FROM users WHERE email =%(email)s;"

        results = connectToMySQL('login').query_db(query, data)

        return len(results) == 0

    @classmethod 
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;" 
        results = connectToMySQL('login').query_db(query, data)

        if len(results) > 0:
            return cls(results[0])
        else:
            return False

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('login').query_db(query, data)
        if len(results) == 0:
            return False
        else:
            return cls(results[0])
    
    @staticmethod 
    def validate_registration(user):
        is_valid = True

        if len(user['first_name']) == 0:
            flash("first name is required.", "first_name")
            is_valid = False

        elif len(user['first_name']) < 2:
            flash("first name has to be at least 2 charachters in length.", "first_name")
            is_valid = False
        
        elif not LETTERS_ONLY_REGEX.match(user['first_name']):
            flash("first name can not have non-alphabetic charachters.", "first_name")
            is_valid = False
            
        if len(user['last_name']) == 0:
            flash("must have last name.", "email")
            is_valid = False

        elif len(user['last_name']) < 2:
            flash("Last name has to be more than 2 characters.", "last_name")
            is_valid = False
        
        elif not LETTERS_ONLY_REGEX.match(user['last_name']):
            flash("first name can not have non-alphabetic charachters.","last_name")

        if len(user['email']) == 0:
            flash("Email is  required.", "email")
            is_valid = False

        elif not EMAIL_REGEX.match(user['email']):
            flash("email format is not correct. Must meet name@emaildomain.com style.", "email")
            is_valid = False

        elif not User.is_email_not_in_database(user):
            flash("A user has an existing email.", "email")
            is_valid = False

        elif not User.is_email_not_in_database(user):
            flash("A user has an existing email.", "email")
            is_valid = False
        
        if len(user['password']) == 0:
            flash("you must hav a password.", "password")
            is_valid = False

        elif len(user['password']) < 8:
            flash("you must have a password.", "password")
            is_valid = False
        
        elif user['password'] != user['confirm_password']:
            flash("password and confirm password do not match.", "password")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(login_user):
        user_in_db = User.get_user_by_email(login_user)
        if not user_in_db:
            flash("email and password incorrect", "login_email")
            return False

        if not bcrypt.check_password_hash(user_in_db.password, login_user['password']):
            flash("email and password incorrect", "login_email")
            return False

        return user_in_db