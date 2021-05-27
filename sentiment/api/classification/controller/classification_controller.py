import logging
import sqlite3
import json
import pandas as pd
import os
import traceback

from flask import request
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import sklearn.linear_model as lm
from sklearn.model_selection import train_test_split
from sentiment.api.nlp.controller.nlp_controller import clean_text
from sentiment.api.data.controller.dataset_controller import add_new_model, delete_model

log = logging.getLogger(__name__)

path = os.path.join(os.getcwd(), "model")
a = list(filter(lambda x: 'tfidf.pkl' in x, os.listdir(path)))

c = [y.rsplit(".", 1)[0] for y in a]

for name in c:
    globals()[name] = joblib.load(os.path.join(path, "{}.pkl".format(name)))

def predict_sentiment(text):
    result = {}
    data = request.json
    input_data = data.get('text')
    model_name = data.get('model_name')
    result['input_text'] = input_data
    c_text = clean_text(input_data)['result']
    if c_text == 'NoTurkishContent':
        result['cleaned_text'] = 'NoTurkishContent'
        result['prediction'] = ''
        result['predicted_category'] = ''
        result['predicted_score'] = ''
        result['all_category'] = ''
        result['all_scores'] = ''
        return result
    if c_text == 'NoContent':
        result['cleaned_text'] = 'NoContent'
        result['prediction'] = ''
        result['predicted_category'] = ''
        result['predicted_score'] = ''
        result['all_category'] = ''
        result['all_scores'] = ''
        return result
    result['cleaned_text'] = c_text
    clf_load = joblib.load("model/{}.pkl".format(model_name))
    tfidf = globals()["{}_tfidf".format(model_name)]
    with open("model/{}.json".format(model_name)) as f:
        id_to_category = json.load(f)
    c_text = [c_text]
    text_features = tfidf.transform(c_text).toarray()
    my_prediction = clf_load.predict(text_features)
    result['prediction'] = str(my_prediction[0])
    predict_score = clf_load.predict_proba(text_features)[0][my_prediction[0]]
    result['predicted_category'] = id_to_category[str(my_prediction[0])]
    result['predicted_score'] = predict_score
    result['all_category'] = id_to_category
    #result['all_scores'] = json.dumps(clf_load.n(text_features)[0].tolist())

    cnx = sqlite3.connect('test.db')
    sql = "select d.threshold as threshold from model as d where d.model_name='{}'".format(
        model_name)
    try:
        df = pd.read_sql_query(sql, cnx)
    except Exception as e:
        log.warning(traceback.format_exc())
        return {'message': 'A data result was required but none was found.'}, 404
    if predict_score < df.threshold[0]:
        result['prediction'] = ''
    return result


def create_model_classification(text, type):
    data = request.json
    model_name = data.get('model_name')
    model_type = data.get('model_type')
    threshold = data.get('threshold')
    cnx = sqlite3.connect('test.db')
    if type == "polarity":
        sql = "select d.clean_text as clean_text, d.label as category from dataset as d where d.model='{}'".format(
            model_type)
    else:
        sql = "select d.clean_text as clean_text, d.category as category from dataset as d where d.model='{}'".format(
            model_type)
    try:
        df = pd.read_sql_query(sql, cnx)
    except Exception as e:
        log.warning(traceback.format_exc())
        return {'message': 'A data result was required but none was found.'}, 404
    df = df[df.clean_text != 'NoTurkishContent']
    df = df[df.clean_text != 'NoContent']
    tfidf = TfidfVectorizer(sublinear_tf=True, norm='l2', min_df=0.001, max_df=0.20, encoding='UTF-8',
                            ngram_range=(1, 2))
    features = tfidf.fit_transform(df.clean_text).toarray()
    df['category_id'] = df['category'].factorize()[0]
    category_id_df = df[['category', 'category_id']].drop_duplicates().sort_values('category_id')
    id_to_category = dict(category_id_df[['category_id', 'category']].values)
    labels = df.category_id
    model = lm.LogisticRegression(random_state=0)
    X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, df.index,
                                                                                     test_size=0.33, random_state=0)
    model.fit(X_train, y_train)
    model.fit(features, labels)
    score = model.score(X_test, y_test)
    with open("model/{}.json".format(model_name), 'w') as outfile:
        json.dump(id_to_category, outfile, ensure_ascii=False)
    model_path = "model/{}.pkl".format(model_name)
    joblib.dump(model, model_path)
    joblib.dump(tfidf, "model/{}_tfidf.pkl".format(model_name))
    globals()["{}_tfidf".format(model_name)] = joblib.load(
        os.path.join(os.getcwd(), "model", "{}_tfidf.pkl".format(model_name)))

    add_new_model(model_name, model_type, float(score), threshold)


def delete_old_model(text):
    data = request.json
    model_name = data.get('model_name')
    model_path = os.path.join(os.getcwd(), "model", "{}.pkl".format(model_name))
    tfidf_path = os.path.join(os.getcwd(), "model", "{}_tfidf.pkl".format(model_name))
    json_path = os.path.join(os.getcwd(), "model", "{}.json".format(model_name))
    # As file at filePath is deleted now, so we should check if file exists or not not before deleting them
    if os.path.exists(model_path):
        os.remove(model_path)
    if os.path.exists(tfidf_path):
        os.remove(tfidf_path)
    if os.path.exists(json_path):
        os.remove(json_path)
    delete_model(model_name)
