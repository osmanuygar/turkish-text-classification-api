import logging

from flask_restplus import Resource
from flask import request
from sentiment.api.rest import api
from sentiment.api.data.controller.serializers import text
from sentiment.api.nlp.controller.nlp_controller import clean_text,lemma_text,understandable_text

log = logging.getLogger(__name__)

ns = api.namespace('nlp', description='NLP Operations')

@ns.route('/understandable_text/')
class TextCollection(Resource):
    @api.expect(text)
    def post(self):
        """
        This service can be used correcting words written incorrectly or informal speech from noisy texts.
        ```
            {
              "text": "yine yayin kesildi yine magdur edildik"
            }
         ```
        """
        data = request.json
        input_data = data.get('text')
        result = understandable_text(input_data)
        return result


@ns.route('/clean/')
class TextCollection(Resource):
    @api.expect(text)
    def post(self):
        """
        This service can be used correcting words written incorrectly or informal speech from noisy texts.
        ```
            {
              "text": "yine yayin kesildi yine magdur edildik"
            }
         ```
        """
        data = request.json
        input_data = data.get('text')
        result = clean_text(input_data)
        return result


@ns.route('/lemma/')
class TextCollection(Resource):
    @api.expect(text)
    def post(self):
        """
        This service can be used correcting words written incorrectly or informal speech from noisy texts and return lemmas
        ```
            {
              "text": "yine yayin kesildi yine magdur edildik"
            }
         ```
        """
        data = request.json
        input_data = data.get('text')
        result = lemma_text(input_data)
        return result
