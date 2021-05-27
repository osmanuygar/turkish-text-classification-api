from flask_restplus import fields
from sentiment.api.rest import api

dataset = api.model('dataset', {
    'text': fields.String(required=True, description='Text'),
    'clean_text': fields.String(required=False, description='Clean Text'),
    'model': fields.String(required=False, description='Model Name'),
    'category': fields.String(required=False, description='Category Name (billing,HR ...)'),
    'label': fields.String(required=False, description='Label Name (positive/negative/neutral)')
})

dataset_all = api.model('dataset all', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a Dataset'),
    'text': fields.String(required=True, description='Text'),
    'clean_text': fields.String(required=False, description='Clean Text'),
    'model': fields.String(required=False, description='Model Name'),
    'category': fields.String(required=False, description='Category Name (billing,HR ...)'),
    'label': fields.String(required=False, description='Label Name (positive/negative/neutral)'),
    'pub_date': fields.DateTime,
})

model = api.model('model', {
    'model_name': fields.String(required=False, description='Model Name'),
    'model_type': fields.String(required=False, description='Model Type'),
    'score': fields.Float(required=False, description='Model Name'),
    'threshold': fields.Float(required=False, description='Threshold'),
    'pub_date': fields.String(required=False, description='Pub Date')
})

pagination = api.model('a page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results')
})

pagination_with_model = api.model('a page of results with model', {
    'model': fields.String(required=True, description='Model Name'),
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results')
})

pagination_with_category = api.model('a page of results with category', {
    'category': fields.String(required=True, description='Category'),
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results')
})

page_of_dataset = api.inherit('page of dataset', pagination, {
    'items': fields.List(fields.Nested(dataset_all))
})

page_of_dataset_with_model = api.inherit('page of dataset according to model', pagination_with_model, {
    'items': fields.List(fields.Nested(dataset_all))
})

page_of_dataset_with_category = api.inherit('page of dataset according to category', pagination_with_category, {
    'items': fields.List(fields.Nested(dataset_all))
})

text = api.model('text', {
    'text': fields.String(required=True, description='Posted Text')
})

model_text = api.model('model and text', {
    'text': fields.String(required=True, description='Posted Text'),
    'model_name': fields.String(required=True, description='Scored Model Name')
})

model_name = api.model('model name', {
    'model_name': fields.String(required=True, description='Model Name')
})

model_density_count = api.model('model name', {
    'model_name': fields.String(required=True, description='Model Name'),
    'quantity': fields.Integer(required=True, description='Count of words for density measure')
})
