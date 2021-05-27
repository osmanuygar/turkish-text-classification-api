import logging.config

import os
from flask import Flask, Blueprint
from sentiment import settings
from sentiment.api.data.datasets import ns as sentiment_datasets_namespaces
from sentiment.api.classification.classification import ns as classification_namespaces
from sentiment.api.nlp.nlp import ns as nlp_namespaces
from sentiment.api.density.density import ns as density_namespace
from sentiment.api.rest import api
from sentiment.db.model.dataset import db


app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)
app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
blueprint = Blueprint('api', __name__, url_prefix='/api')
db.create_all()
api.init_app(blueprint)
api.add_namespace(sentiment_datasets_namespaces)
api.add_namespace(classification_namespaces)
api.add_namespace(nlp_namespaces)
api.add_namespace(density_namespace)
app.register_blueprint(blueprint)
db.init_app(app)
print('>>>>> Configured Application <<<<<')


def main():
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)


if __name__ != "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


if __name__ == "__main__":
    main()