from recipe_app.models.user import User
from recipe_app.config.mysqlconnection import connectToMySQL

class Recipe:
    def get_recipe(self, data):
        self.id = data["id"],
        self.name = data["name"],
        self.instructions = data["instructions"]
        self.time_limit = data["time_limit"]
        self.description = data["description"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_recipe(cls, id):
        query = "SELECT * FROM recipes WHERE id=%(id)s;"
        data = {
            "id": id
        }
        results = connectToMySQL('login').query_db(query, data)
        recipe = cls(results[0])
        return recipe

    @classmethod
    def get_all_recipe(cls, data):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('login').query_db(query, data)
        recipes = []
        for recipe in recipes:
            results.append(cls(recipe))
        return 

    @classmethod
    def save_recipe(cls, data):
        query = "INSERT INTO recipes(name, instructions, time_limit, intructions, descriptions, user_id, updated_at, created_at) VALUES (%(name)s, %(instructions)s, %(time_limit)s, %(description)s, %(user_id)s, NOW(), NOW());"
        return connectToMySQL("login").query_db(query, data)
    
    @classmethod
    def edit_recipe(cls, data):
        query = "UPDATE recipes SET name=%(name)s, instructions=%(instructions), time_limit=%(time_limit)s, description=%(descriptions)s, created_at=%(created_at)s;"
        results = connectToMySQL('recipes').query_db(query,data)
        return results