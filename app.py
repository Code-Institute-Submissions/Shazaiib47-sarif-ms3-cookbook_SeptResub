import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# Code below gets the recipes for the "Home" page also known as "get_recipes"

@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    recipes = list(mongo.db.recipes.find())
    return render_template("recipes.html", recipes=recipes)


# Search Bar code to allow users to search using the index

@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    return render_template("recipes.html", recipes=recipes)


# Registering an account is shown here with various verification methods

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Done to verify if the username already exists within the DB
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # places the new user into a session with the cookie on website
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


# Login functionality to check it differs from registered/unregistered users


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # This checks to see if the username already exists in the DB
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # Validates that the hashed password matches what the user has.
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}.".format(
                        request.form.get("username")))
                return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # triggers if password is matched incorrectly
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # triggers if username does not exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


# This retrieves the user's username if they have a session active

@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # retrieves the session user's username from mongoDB
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


# Logout functionality with a flash message also shown

@app.route("/logout")
def logout():
    # this function ensures the user is removed from session cookie
    flash("You have successfully been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Adds a recipe to the Database with the variables retrieved from mongoDB

@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        recipe_made = "on" if request.form.get("recipe_made") else "off"
        recipe = {
            "recipe_category": request.form.get("recipe_category"),
            "recipe_name": request.form.get("recipe_name"),
            "recipe_description": request.form.get("recipe_description"),
            "image_url": request.form.get("image_url"),
            "recipe_made": recipe_made,
            "recipe_added": request.form.get("recipe_added"),
            "created_by": session["user"]
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe Successfully Added!")
        return redirect(url_for("get_recipes"))

    recipes = mongo.db.recipe_categories.find().sort("recipe_categories", 1)
    return render_template("add_recipe.html", recipes=recipes)


# Functionality to edit recipes

@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):

    if request.method == "POST":
        recipe_made = "on" if request.form.get("recipe_made") else "off"
        submit = {
            "recipe_category": request.form.get("recipe_category"),
            "recipe_name": request.form.get("recipe_name"),
            "recipe_description": request.form.get("recipe_description"),
            "image_url": request.form.get("image_url"),
            "recipe_made": recipe_made,
            "recipe_added": request.form.get("recipe_added"),
            "created_by": session["user"]
        }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, submit)
        flash("Recipe Successfully Updated!")

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories = mongo.db.recipe_categories.find().sort("recipe_category", 1)
    return render_template("edit_recipe.html", recipe=recipe,
                           categories=categories)


# Functionality to delete recipes

@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe Successfully Deleted!")
    return redirect(url_for("get_recipes"))


@app.route("/get_categories")
def get_categories():
    categories = list(mongo.db.recipe_categories.find().sort
                      ("recipe_category", 1))
    return render_template("categories.html", categories=categories)


# Adding a recipe category to database

@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = {
            "recipe_category": request.form.get("recipe_category")
        }
        mongo.db.recipe_categories.insert_one(category)
        flash("New Recipe Category Added!")
        return redirect(url_for("get_recipes"))

    return render_template("add_recipe_category.html")


# Edit recipe category functionality

@app.route("/edit_recipe_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        submit = {
            "recipe_category": request.form.get("recipe_category")
        }
        mongo.db.recipe_categories.update({"_id": ObjectId
                                          (category_id)}, submit)
        flash("Recipe Category Successfully Updated!")
        return redirect(url_for("get_categories"))

    category = mongo.db.recipe_categories.find_one(
                        {"_id": ObjectId(category_id)})
    return render_template("edit_recipe_category.html", category=category)


# Delete recipe functionality

@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    mongo.db.recipe_categories.remove({"_id": ObjectId(category_id)})
    flash("Recipe Category Successfully Deleted!")
    return redirect(url_for("get_categories"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
