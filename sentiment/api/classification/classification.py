import logging

from flask_restplus import Resource

from sentiment.api.data.controller.serializers import text, model, model_text
from sentiment.api.classification.controller.classification_controller import predict_sentiment, create_model_classification, delete_old_model
from sentiment.api.rest import api

log = logging.getLogger(__name__)

ns = api.namespace('classification', description='Classification Operations')


@ns.route('/predict/')
class TextPredictCollection(Resource):
    @api.expect(model_text)
    def post(self):
        """
            This service can be used computational tools to determine the emotional tone behind words.
        ```
            {
              "text": "yine yayın kesil yine mağdur edildik",
              "model_name": "store_v1"
            }
         ```
        """
        result = predict_sentiment(model_text)
        return result


@ns.route('/create_subjectivity_model/')
@api.response(201, 'Model successfully created.')
class TextCreateModelCollection(Resource):
    @api.expect(model)
    def post(self):
        """
            This service can be used create a ML model.

            * Send a JSON object with the new model in the request body.
            * WARNING: model_type must be included in dataset because model use just related model types

        ```
        {
          "model_name": "btk_v1",
          "model_type": "btk",
          "threshold": 0.3
        }
         ```
        """
        create_model_classification(model,"subjectivity")
        return None, 201

@ns.route('/create_polarity_model/')
@api.response(201, 'Model successfully created.')
class TextCreateModelCollection(Resource):
    @api.expect(model)
    def post(self):
        """
            This service can be used create a ML model.

            * Send a JSON object with the new model in the request body.
            * WARNING: model_type must be included in dataset because model use just related model types

        ```
        {
          "model_name": "store_v1",
          "model_type": "store",
          "threshold": 0.3
        }
         ```
        """
        create_model_classification(model,"polarity")
        return None, 201


@ns.route('/delete_model/')
@api.response(201, 'Model successfully deleted.')
class TextCreateModelCollection(Resource):
    @api.expect(model)
    def post(self):
        """
            This service can be used create a ML model.

            * Send a JSON object with the new model in the request body.

        ```
        {
          "model_name": "store_v1"
        }
         ```
        """
        delete_old_model(model)
        return None, 201
