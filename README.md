# Turkish Text Classification API

You can easily build custom turkish text classifiers through this API for more accurate insights, and start detecting topics, sentiment, intent, and more


## Installation

To download application the following commands.

```sh
git clone https://github.com/osmanuygar/turkish-text-classification-api.git
cd turkish-text-classification-api
```

Create a virtual Python environment in a directory named venv, activate the virtualenv and install required dependencies using pip.

```sh
cd <related-path>/turkish-text-classification-api/
virtualenv -p `which python3` venv
source venv/bin/activate
pip install -r requirements.txt
```

## Start the app

Install packages
```sh
cd <related-path>/turkish-text-classification-api/
python setup.py develop
```

Activate the virtual enviroment
Start the application with Gunicorn (you can remove workers and threads in gunicorn, if you want)
```sh
source <related-virtualenv-path>/venv/bin/activate
cd <related-path>/turkish-text-classification-api/sentiment/

gunicorn \
--bind 0.0.0.0:5001 app:app \
--log-file /opt/log/advanced_analytic_platform.log \
--error-logfile /opt/log/advanced_analytic_platform/error.log \
--access-logfile /opt/log/advanced_analytic_platform/access.log  \
--log-level=info \
--timeout 7200 \
--workers 2 \
--threads 4 &
```

Kill the application 
```sh
ps -ef | grep "gunicorn"
kill -9 xxxx
```

## Usage

Swagger document helps you to use API, with examples and test screens.

http://localhost:5001/api/

### Dataset

Add Datasets first
http://<span></span>localhost:5001/api/db/dataset/
```json
{
  "text": "sinyal problemi yaşıyorum",
  "model": "chatbot",
  "category": "teknik problem",
  "label": "negative"
}
```

### Model
Create model with added datasets

POST: http://<span></span>localhost:5001/api/classification/create_subjectivity_model/
```json
{
  "model_name": "chatbot",
  "model_type": "chatbot"
}
```

### Predict
Predict any text data with created models.

POST: http://<span></span>localhost:5001/api/classification/predict/
```json
{
  "text": "Uygulamada problemler oluştu. Hiç bağlanamadım.",
  "model_name": "chatbot"
}
```

### Density
you can find the terms that are the most correlated with each of the feature of related dataset

POST: http://<span></span>localhost:5001/api/density/get_density/
```json
{
  "model_name": "string",
  "quantity": 0
}
```

## Development Tools
* [Python] - Programing language
* [SQLite] - SQL database engine
* [Scikit-learn] - Python ML library
* [Flask] - Python based web development microframework
* [Swagger] - API development framework
* [NLTK] - Language processing library
* [Zemberek] - Language processing tool
* [Gunicorn] - Python WSGI HTTP Server for UNIX

