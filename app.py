from flask import Flask, flash, render_template, redirect, request, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import base64
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, instance_path='/database.db')
app.secret_key = "something_secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['INSTANCE_FOLDER'] = None
app.config.update(TEMPLATES_AUTO_RELOAD=True)
db = SQLAlchemy(app)

class Credentials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(30),nullable=False)
    age = db.Column(db.String(30),nullable=False)
    gender = db.Column(db.String(30),nullable=False)

    def __init__(self,username,password,email,age,gender):
        self.username = username
        self.password = password
        self.email = email
        self.age = age
        self.gender = gender

    def __repr__():
        return f"<Credentials {self.username}>"

class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),nullable=False)
    recipe_name = db.Column(db.String(500),nullable=False) 
    ingredients = db.Column(db.String(500),nullable=False)
    photo = db.Column(db.LargeBinary)
    comments = db.Column(db.String(500))
    def __init__(self,username,recipe_name,ingredients,photo,comments):
        self.username = username 
        self.recipe_name = recipe_name 
        self.ingredients = ingredients
        self.photo = photo
        self.comments = comments 

    def __repr__(self):
        return f"<Recipes {self.recipe_name}>"

@app.route('/', methods=["POST","GET"])
def index():
    if request.method == "GET":
        recipes_show = Recipes.query.all()
        # print(recipes_show)
        images = []
        for recipe in recipes_show:
            image_base64 = base64.b64encode(recipe.photo).decode('utf-8')
            images.append(image_base64)
        username = ''  
        if 'username' in session:  
            username = session['username']
        if 'username' in session:
            if recipes_show:
                return render_template('index.html',recipes_show=recipes_show,images=images,username=username)
            else:
                return render_template('index.html',username=username)
        else:
            if recipes_show:
                return render_template('index.html',recipes_show=recipes_show,images=images)
            else:
                return render_template('index.html')
    else:
        return render_template("add_recipe")
        
@app.route('/login', methods=["POST","GET"])
def login():
    if request.method == "POST":
        session.pop('username', None)
        username = request.form.get('username')
        password = request.form.get('password')
        user = Credentials.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                session['username'] = username
                return redirect(url_for('account'))
            else:
                flash('wrong password!')
                return redirect(url_for("login"))
        else:
            flash('user not found!')
            return redirect(url_for('login'))                
    else:
        return render_template('login.html')

@app.route('/sign_up', methods=["POST","GET"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        age = request.form.get('age')
        gender = request.form.get('gender')
        user = Credentials(username=username, password=password, email=email, age=age, gender=gender)
        db.session.add(user)
        db.session.commit()
        # print(username,password,email,age,gender)
        flash('basariyla kaydedildi!')
        return redirect(url_for('login'))
    else:
        return render_template('sign_up.html')

@app.route('/account', methods=["GET"])
def account():
    username = ''
    images = []
    if 'username' in session:
        username = session['username']
    your_recipes = Recipes.query.filter_by(username=username)
    for recipe in your_recipes:
        image_base64 = base64.b64encode(recipe.photo).decode('utf-8')
        images.append(image_base64)
    if your_recipes:
        return render_template('account.html',username=username,your_recipes=your_recipes,images=images)
    else:
        return render_template('account.html',username=username,images=images)


@app.route('/add_recipe', methods=["POST","GET"])
def add_recipe():
    if request.method == "POST":
        if 'username' in session:
            username = session['username']
        recipe_name = request.form.get('name')
        comments = request.form.get('comments')
        ingredients = request.form.get('ingredients')
        file = request.files['file']
        recipe = Recipes(username=username, recipe_name=recipe_name, ingredients=ingredients, comments=comments, photo=file.read())
        db.session.add(recipe)
        db.session.commit()

        return redirect(url_for('index'))
    else:
        if 'username' in session:
            return render_template('add_recipe.html')
        else:
            return redirect(url_for('login'))

@app.route('/delete_recipe', methods=['GET','POST'])
def delete_recipe():
    if request.method == 'GET':
        return render_template('delete_recipe.html') 
    else:
        username = ''
        recipe_name = request.form.get('query')
        if 'username' in session:
            username = session['username']
        recipe_to_delete = Recipes.query.filter_by(recipe_name=recipe_name).first()
        db.session.delete(recipe_to_delete)
        db.session.commit()
        return redirect(url_for('account'))

@app.route('/update_recipe', methods=['GET','POST'])
def update_recipe():
    if request.method == 'GET':
        return render_template('update_recipe.html')
    else:
        username = session['username']
        query = request.get_json()
        #  = searchTerm['query']
        recipe_to_update = Recipes.query.filter_by(recipe_name=query).first()
        # print(recipe_to_update.recipe_name)        
        images = base64.b64encode(recipe_to_update.photo).decode('utf-8')

        if recipe_to_update.username == username:
            return render_template('update_recipe.html', recipe_to_update=recipe_to_update, images=images)
        else:
            return 'some other text'
    return 'some text'

@app.route('/search', methods=["POST"])
def search():
    query = request.get_json()
    # print(query)
    query_recipe = Recipes.query.filter_by(recipe_name=query).first()  
    # print(type(query_recipe))
    recipe_data = {
        'name': query_recipe.recipe_name,
        'ingredients': query_recipe.ingredients,
        'image' : base64.b64encode(query_recipe.photo).decode('utf-8')
    }
    return recipe_data


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)

