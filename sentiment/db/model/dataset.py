from datetime import datetime
from sentiment.db import db, ma
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sentiment.api.nlp.controller.nlp_controller import clean_text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(4000), nullable=False, unique=False)
    clean_text = db.Column(db.String(4000), nullable=False, unique=False)
    model = db.Column(db.String(80), nullable=True)
    category = db.Column(db.String(80), nullable=True, unique=False)
    label = db.Column(db.String(80), nullable=True, unique=False)
    pub_date = db.Column(db.DateTime)

    def __init__(self, text, model, category, label, pub_date=None):
        self.text = text
        self.clean_text = clean_text(text)['result']
        self.model = model
        self.label = label
        self.category = category
        if pub_date is None:
            self.pub_date = datetime.utcnow()


class DatasetSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('text', 'model', 'category', 'label', 'pub_date')


class Model(db.Model):
    model_name = db.Column(db.String(80), primary_key=True)
    model_type = db.Column(db.String(80))
    score = db.Column(db.Float, nullable=True, unique=False)
    threshold = db.Column(db.Float, nullable=True, unique=False)
    pub_date = db.Column(db.DateTime)

    def __init__(self, model_name, model_type, score, threshold, pub_date=None):
        self.model_name = model_name
        self.model_type = model_type
        self.score = score
        self.threshold = threshold
        if pub_date is None:
            self.pub_date = datetime.utcnow()


class ModelSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('model_name', 'model_type', 'score', 'threshold', 'pub_date')
