from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "todo.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
print(database_file)
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.Text)
    location_id = db.Column(db.Integer)
    dateAdded = db.Column(db.DateTime, default=datetime.now())


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_name = db.column(db.text)


def create_note(text):
    product = Product(product_name=text)
    db.session.add(product)
    db.session.commit()
    db.session.refresh(product)


def create_location(text):
    location = Location(location_name=text)
    db.session.add(location)
    db.session.commit()
    db.session.refresh(location)


def read_notes():
    return db.session.query(Product).all()


def read_locations():
    return db.session.query(Location).all()


def update_note(product_id, text, done):
    db.session.query(Product).filter_by(id=product_id).update({
        "product_name": text
    })
    db.session.commit()


def delete_note(product_id):
    db.session.query(Product).filter_by(id=product_id).delete()
    db.session.commit()


def update_location(location_id, text, done):
    db.session.query(Location).filter_by(id=location_id).update({
        "location_name": text
    })
    db.session.commit()


def delete_location(location_id):
    db.session.query(Location).filter_by(id=location_id).delete()
    db.session.commit()


@app.route("/", methods=["POST", "GET"])
def view_index():
    if request.method == "POST":
        create_note(request.form['text'])
    return render_template("index.html", products=read_notes())


@app.route("/addLocation", methods=["POST", "GET"])
def view_index2():
    if request.method == "POST":
        create_location(request.form['locationtext'])
    return render_template("index.html", locations=read_locations())


@app.route("/edit/<product_id>", methods=["POST", "GET"])
def edit_note(product_id):
    if request.method == "POST":
        update_note(product_id, text=request.form['text'], done=request.form['done'])
    elif request.method == "GET":
        delete_note(product_id)
    return redirect("/", code=302)


@app.route("/editLocation/<location_id>", methods=["POST", "GET"])
def edit_location(location_id):
    if request.method == "POST":
        update_location(location_id, text=request.form['text'], done=request.form['done'])
    elif request.method == "GET":
        delete_location(location_id)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.app_context().push()
    db.create_all()
    app.run(debug=True)
