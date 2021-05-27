import logging

from flask import request
from flask_restplus import Resource
from sentiment.api.rest import api
from sentiment.db.model.dataset import Dataset, Model
from sentiment.api.data.controller.serializers import dataset, page_of_dataset, model, page_of_dataset_with_model, page_of_dataset_with_category
from sentiment.api.data.controller.parser import pagination_arguments, pagination_arguments_with_model, pagination_arguments_with_category
from sentiment.api.data.controller.dataset_controller import add_new_dataset, update_dataset, delete_dataset

log = logging.getLogger(__name__)

ns = api.namespace('db', description='DB Operations')


@ns.route('/dataset')
class DatasetCollection(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_dataset)
    def get(self):
        """
        Returns list of datasets with pagination.
        * Get a pagination json for

        ```
        curl -X GET "http://localhost:5001/api/db/dataset?page=1&bool=true&per_page=20" -H "accept: application/json"
        ```
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        dataset_query = Dataset.query
        dataset_page = dataset_query.paginate(page, per_page, error_out=False)
        return dataset_page

    @api.response(201, 'Dataset successfully created.')
    @api.expect(dataset)
    def post(self):
        """
        Creates a new dataset.
         Use this method to change the name of a dataset.

        * Send a JSON object with the new dataset in the request body.

        ```
        {
          "text": "sinyal problemi yaşıyorum",
          "model": "store",
          "category": "teknik",
          "label": "positive"
        }
        ```
        """

        add_new_dataset(request.json)
        return None, 201


@ns.route('/dataset/<int:id>')
@api.response(404, 'Dataset not found.')
class CategoryItem(Resource):

    @api.marshal_with(dataset)
    def get(self, id):
        """
        Returns a dataset with a list of datasets table according to id.
        """
        return Dataset.query.filter(Dataset.id == id).one()

    @api.expect(dataset)
    @api.response(204, 'Dataset successfully updated.')
    def put(self, id):
        """
        Updates a dataset.

        Use this method to update the values of a dataset.

        * Send a JSON object with the new value in the request body.

        ```
        {
          "text": "sinyal problemi yaşıyorum",
          "model": "store",
          "category": "teknik",
          "label": "positive"
        }
        ```
        * Specify the ID of the dataset to modify in the request URL path.
        """
        data = request.json
        update_dataset(id, data)
        return None, 204

    @api.response(204, 'Dataset successfully deleted.')
    def delete(self, id):
        """
        Deletes dataset.
        """
        delete_dataset(id)
        return None, 204


@ns.route('/dataset/findbymodel')
@api.response(404, 'Dataset not found.')
class ModelItem(Resource):

    @api.expect(pagination_arguments_with_model)
    @api.marshal_with(page_of_dataset_with_model)
    def get(self):
        """
        Returns a dataset with a list of datasets table according to model.
        """
        args = pagination_arguments_with_model.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        model_name = args.get('model')
        dataset_query = Dataset.query.filter(Dataset.model == model_name).paginate(page, per_page, error_out=False)
        return dataset_query


@ns.route('/dataset/findbycategory')
@api.response(404, 'Dataset not found.')
class CategoryItem(Resource):

    @api.expect(pagination_arguments_with_category)
    @api.marshal_with(page_of_dataset_with_category)
    def get(self):
        """
        Returns a dataset with a list of datasets table according to category.
        """
        args = pagination_arguments_with_category.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        category = args.get('category')
        dataset_query = Dataset.query.filter(Dataset.category == category).paginate(page, per_page, error_out=False)
        return dataset_query


@ns.route('/model')
@api.response(404, 'Model not found.')
class ModelCollection(Resource):

    @api.marshal_with(model)
    def get(self):
        """
        Returns list of models.
        """
        return Model.query.order_by(Model.model_name).all()

