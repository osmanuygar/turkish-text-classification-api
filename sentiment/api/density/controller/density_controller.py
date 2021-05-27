import logging
import sqlite3
import json
import pandas as pd
import traceback
import numpy as np

from flask import request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2

log = logging.getLogger(__name__)


def get_word_density(model_name):
    data = request.json
    model_name = data.get('model_name')
    word_count = data.get('quantity')
    cnx = sqlite3.connect('test.db')
    sql = "select d.clean_text as clean_text, d.category as category from dataset as d where d.model='{}'"\
        .format(model_name)
    try:
        df = pd.read_sql_query(sql, cnx)
    except Exception as e:
        log.warning(traceback.format_exc())
        return {'message': 'A data result was required but none was found.'}, 404
    df = df[df.clean_text != 'NoTurkishContent']
    df = df[df.clean_text != 'NoContent']

    df['category_id'] = df['category'].factorize()[0]
    category_id_df = df[['category', 'category_id']].drop_duplicates().sort_values('category_id')
    category_to_id = dict(category_id_df.values)
    id_to_category = dict(category_id_df[['category_id', 'category']].values)

    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=0.001, max_df=0.20, encoding='UTF-8',
                            ngram_range=(1, 2))
    features = tfidf.fit_transform(df.clean_text).toarray()
    labels = df.category_id

    counter=0
    mylist = {}
    appneded = []

    N = word_count
    for category, category_id in sorted(category_to_id.items()):
        mylist["category"]=category
        features_chi2 = chi2(features, labels == category_id)
        indices = np.argsort(features_chi2[0])
        feature_names = np.array(tfidf.get_feature_names())[indices]
        unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
        mylist["unigram"]=unigrams[-N:]
        bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
        mylist["bigram"]=bigrams[-N:]
        counter = counter + 1
        # print("# '{}':".format(category))
        # print("  . Most correlated unigrams:\n       . {}".format('\n       . '.join(unigrams[-N:])))
        # print("  . Most correlated bigrams:\n       . {}".format('\n       . '.join(bigrams[-N:])))
        mylistCopy = mylist.copy()
        appneded.append(mylistCopy)
    jsonObje = json.dumps(appneded)

    return jsonObje

