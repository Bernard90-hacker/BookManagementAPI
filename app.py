from datetime import date, datetime
import json
import os
import string
from tkinter.messagebox import NO
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from dotenv import load_dotenv
load_dotenv()

#Démarrage de l'application
app = Flask(__name__)

motdepasse = os.getenv(quote_plus('password'))
hostname = os.getenv('host')

#Configuration de la chaîne de connexion
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:{}@{}:5432/mini_projet_flask".format(motdepasse, hostname)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Création d'une instance de la base de données
db = SQLAlchemy(app)

#Création des classes

class Livre(db.Model):
    __tablename__ = 'livres'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), unique=True) #J'ai choisi 13 cacractères car le code isbn est composé de 13 caractères
    titre = db.Column(db.String(40), nullable=False)
    date_publication = db.Column(db.Date, nullable=False)
    auteur = db.Column(db.String(120), nullable=False)
    editeur = db.Column(db.String(80), nullable=False)
    categorie = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    def __init__(self, isbn, titre, date_publication, auteur, editeur, categorie):
        self.isbn = isbn
        self.titre = titre
        self.date_publication = date_publication
        self.auteur = auteur
        self.editeur = editeur
        self.categorie = categorie
        
    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def format(self):
        return {
            'id'                  : self.id,
            'isbn'                : self.isbn,
            'titre'               : self.titre,
            'date de publication' : self.date_publication,
            'Nom de l\'auteur'    : self.auteur,
            'Nom de l\'éditeur'   : self.editeur,
            'Catégorie'           : self.categorie
        }
    
class Categorie(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    libelle_categorie = db.Column(db.String(80), nullable=False)
    categorie = db.relationship('Livre', backref='categories', lazy=True)
    
    def __init__(self, libelle):
        self.libelle_categorie = libelle
        
    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
    
    def delete(self) :
        db.session.delete(self)
        db.session.commit()
        
    def format(self) :
        return {
            'id' : self.id,
            'Libellé'  : self.libelle_categorie
        }
db.create_all() 

@app.route('/livres', methods=['GET'])
def getAllBooks():
    livres = Livre.query.all()
    livre_formated = [livre.format() for livre in livres]
    return jsonify({
        'Success' : True,
        'livres'  : livre_formated
        
    })
    
@app.route('/livres/<int:id>', methods=['GET'])
def get_one_book(id):
    selected_book = Livre.query.get(id)
    if selected_book is None :
        abort(404)
    else :
        return jsonify({
            'success'       : True,
            'selected_id'   : selected_book.id,
            'selected_book' : selected_book.format()
        })
        
@app.route('/livres', methods=['POST'])
def add_book():
        body=request.get_json()
        new_isbn = body.get('isbn', None)
        new_title = body.get('titre', None)
        new_author = body.get('auteur', None)
        x = body.get("date de publication").split("-")
        new_date = datetime(int(x[0]), int(x[1]), int(x[2])).date()
        new_author = body.get('auteur')
        new_editor = body.get('editeur', None)
        new_category = body.get('categorie', None)
        livre = Livre(isbn=new_isbn, titre=new_title, date_publication= new_date, auteur= new_author, editeur=new_editor, categorie= new_category)
        livre.insert()
        livres = Livre.query.all()
        livre_formated = [i.format() for i in livres]
        return jsonify({
                    'success'   : True,
                    'created_book'  : livre.format(),
                    'Total'         : livre.query.count(),
                    'livres'        : livre_formated
            })

    
@app.route('/categories/<int:id>/livres', methods=['GET'])
def get_books_per_category(id):
        books = Livre.query.filter(Livre.categorie == id)
        book = Categorie.query.get(id)
        found = 0
        for i in Livre.query.all():
            if i.categorie == id:
                found = 1
                break
        if book is None or found == 0:
            abort(404)
        else:
            selected_books = [selected_book.format() for selected_book in books]
            return jsonify({
                'success'        : True,
                'selected_books' : selected_books
            })

        
@app.route('/categories')
def getAllCategories():
    Categories =  Categorie.query.all()
    Cat = [i.format() for i in Categories]
    return jsonify({
        'Success'  : True,
        'categories' : Cat,
        'Total'      :  Categorie.query.count()
    })     

@app.route('/categories/<int:id>')
def get_one_category(id):
    categorie = Categorie.query.get(id)
    if categorie is None:
        abort(404)
    else:
        return jsonify({
                'selected_id'   : categorie.id,
                'success'       : True,
                'Categories'    : categorie.format()
        })
@app.route('/livres/<int:id>', methods=['DELETE'])
def drop_book(id):
    book = Livre.query.get(id)
    if book is None:
        abort(404)
    else:
        book.delete()
        books = Livre.query.all()
        formated_books = [i.format() for i in books]
        return jsonify({
            'deleted_id'       : book.id,
            'Total'            : Livre.query.count(),
            'Livres'           : formated_books
        })
@app.route('/categories/<int:id>', methods=['DELETE'])
def drop_categorie(id):
    drop_categorie = Categorie.query.get(id)
    livre = Livre.query.filter(Livre.categorie == id)
    if drop_categorie is None :
        abort(404) #Category not found
    elif livre is not None:
        return jsonify({
            'Message'  : 'Can not drop this category there are books inside'
        })
    else :
        for i in livre:
            drop_book(i.categorie)
        drop_categorie.delete()
        AllBooks = Categorie.query.all()
        books = [book.format() for book in AllBooks]
        return jsonify({
            'success'   : True,
            'Deleted_book'  : drop_categorie.format(),
            'Total'         : Categorie.query.count(),
            'Books'         : books
        })
        
@app.route('/categories', methods = ['POST'])
def add_category():
        body = request.get_json()
        Libelle = body.get('libelle')
        category = Categorie(libelle=Libelle)
        category.insert()
        return jsonify({
            'categorie' : category.format(),
            'Total'     : Categorie.query.count()
        })
    
    
@app.route('/livres/<int:id>', methods=['PATCH'])
def modify_book(id):
    getBook = Livre.query.get(id)
    body = request.get_json()
    getBook.isbn = body.get('isbn', None)
    getBook.titre = body.get('titre', None)
    getBook.date_publication = body.get('date_publication', None)
    getBook.auteur = body.get('auteur', None)
    getBook.editeur = body.get('editeur', None)
    getBook.categorie = body.get('categorie', None)
    
    if getBook.isbn is None or getBook.titre is None or getBook.date_publication is None or getBook.auteur is None or getBook.editeur is None or getBook.categorie is None :
        abort(400) #Bad request
    else :
        getBook.update() 
        return jsonify({
            'updated_book'  : getBook.format(),
            'success'       : True
        })
        
@app.route('/categories/<int:id>', methods=['PATCH'])
def setLibelle(id):
        selected_category = Categorie.query.get(id)
        body = request.get_json()
        selected_category.libelle_categorie = body.get('libelle', None)
        if selected_category is None:
            abort(404)
        else :
            selected_category.update()
            return jsonify({
                'success'     : True,
                'setted_book' : selected_category.format()
            })
            
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success' : False,
        'Ressource'  : 'Bad Request',
    }), 400
    
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success' : False,
        'Ressource' : 'Not Found'
    }), 404

        
    
