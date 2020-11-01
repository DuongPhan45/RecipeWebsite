from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
application  = app
app.config['SECRET_KEY'] = "DuongXinh"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ingredients.db'

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class AddForm(FlaskForm):
    igr = StringField("Enter new ingredient", validators=[DataRequired()])
    amount = StringField("Amount")
    add = SubmitField("Add")
    update = SubmitField("Update amount")
    delete = SubmitField("Delete")


class Ingredients(db.Model):
    # __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key = True)
    ing = db.Column(db.String(200), unique = True, nullable = False)
    amount= db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __rep__(self):
        return '<Ingredient %r>' %self.ing

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Ingredients = Ingredients)
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods = ['POST', 'GET'])
def index(): 
    form = AddForm()
   
    if request.method == "POST":
        ing = form.igr.data
        amount = form.amount.data
        updateIn= Ingredients.query.filter_by(ing=ing).first()
        if form.add.data:
             # Update if the ingredient is in the db
            if updateIn is not None:
                updateIn.amount = amount
            else: # Add if the ingredient is new
                newIngredient = Ingredients(ing = ing, amount=amount)
                db.session.add(newIngredient)
        elif form.update.data:
            # Update if the ingredient is in the db
            if updateIn is not None:
                updateIn.amount = amount
        else:
            deleteIn = Ingredients.query.filter_by(ing=ing).all()
            for ing in deleteIn:
                db.session.delete(ing)

        db.session.commit()
       
    ingredients = Ingredients.query.order_by(Ingredients.date_created).all()
    form.igr.data = ''
    form.amount.data=''
    return render_template('index.html', form = form, ingredients = ingredients)

