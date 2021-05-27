import logging
import json

from flask_restplus import Resource

from sentiment.api.data.controller.serializers import model_density_count
from sentiment.api.density.controller.density_controller import get_word_density
from sentiment.api.rest import api

log = logging.getLogger(__name__)

ns = api.namespace('density', description='Density Operations')


@ns.route('/get_density/')
class DensityCollection(Resource):
    @api.expect(model_density_count)
    def post(self):
        """
            This operation used for word Density Explorer
        ```
            {
              "model_name": "npsV4",
              "quantity": 5
            }
         ```
        """
        result = get_word_density(model_density_count)
        resultJson = json.loads(result)
        return resultJson

