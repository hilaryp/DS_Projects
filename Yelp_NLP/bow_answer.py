import gzip
import simplejson as json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.externals import joblib
from sklearn import cross_validation
from nltk.corpus import stopwords


def BagOfWords(X, y):
    X_review = [i['text'] for i in X]
    pipeline = Pipeline([
        ('vect', CountVectorizer(stop_words=stopwords.words('english'),
                                 min_df=150, max_df=.7)), #, max_features=6000)
        ('clf', LinearRegression())
    ])

    #param_grid = {#'vect__min_df': (50, 100, 150),
    #              'vect__max_df': (0.3, 0.4, 0.5)
    #              #'vect__max_features': (1000, 1100),
    #              #'clf__alphas': (0.1, 0.5, 1.0)
    #              }

    #BOW_cv = GridSearchCV(pipeline, param_grid=param_grid, cv=3,
    #                      scoring='mean_squared_error', verbose=2, n_jobs=4)
    BOW_model = pipeline.fit(X_review, y)
    #print BOW_model.grid_scores_
    return BOW_model

def main():
    with gzip.open('yelp_reviews.json.gz', 'rb') as infile:
        f = [json.loads(line) for line in infile.readlines()]

    y = [i['stars'] for i in f]
    #X_train, X_test, y_train, y_test = cross_validation.train_test_split(f, y,
    #   train_size=.25, random_state=42)
    #BOW = BagOfWords(X_train, y_train)
    BOW = BagOfWords(f, y)
    print BOW.predict(["Love it!!!!! Love it!!!!!! love it!!!!!!! \
                          Who doesn't love Culver's!"])
    joblib.dump(BOW, 'BOW_model.pkl')
    
if __name__ == '__main__':
    main()
