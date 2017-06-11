import gzip
import simplejson as json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.externals import joblib
from sklearn import cross_validation
from nltk.corpus import stopwords


def Normalized(X, y):
    X_review = [i['text'] for i in X]
    pipeline = Pipeline([
        ('vect', TfidfVectorizer(stop_words=stopwords.words('english'),
                                 min_df=150, max_df=.7, norm='l2', 
                                 use_idf=False, sublinear_tf=True)),
        ('clf', LinearRegression())
    ])

    #param_grid = {#'vect__min_df': (50, 100, 150),
    #              #'vect__max_df': (0.3, 0.4, 0.5)
    #              #'vect__norm': ('l2', 'l1')
    #              #'vect__use_idf': (True, False)
    #              'vect__sublinear_tf': (True, False)
    #              }

    #TFIDF_cv = GridSearchCV(pipeline, param_grid=param_grid, cv=3,
    #                      scoring='mean_squared_error', verbose=2, n_jobs=4)
    #TFIDF_model = TFIDF_cv.fit(X_review, y)
    #print TFIDF_model.grid_scores_
    TFIDF_model = pipeline.fit(X_review, y)
    return TFIDF_model

def main():
    with gzip.open('yelp_reviews.json.gz', 'rb') as infile:
        f = [json.loads(line) for line in infile.readlines()]

    y = [i['stars'] for i in f]
    #X_train, X_test, y_train, y_test = cross_validation.train_test_split(f, y,
    #   train_size=.25, random_state=42)
    #TFIDF = Normalized(X_train, y_train)
    TFIDF = Normalized(f, y)
    print TFIDF.predict(["Love it!!!!! Love it!!!!!! love it!!!!!!! \
                          Who doesn't love Culver's!"])
    joblib.dump(TFIDF, 'TFIDF_model.pkl')
    
if __name__ == '__main__':
    main()
