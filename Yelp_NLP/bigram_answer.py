import gzip
import simplejson as json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.externals import joblib
from sklearn import cross_validation
from nltk.corpus import stopwords


def Bigram(X, y):
    X_review = [i['text'] for i in X]
    """ 
    # For finding hyperparameters:
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X_review, y,
                                        train_size=.25, random_state=42)
    pipeline = Pipeline([('vect', TfidfVectorizer(stop_words=stopwords.words('english'), 
                                    ngram_range=(1,2), min_df=50, max_df=40000, norm='l2',
                                    use_idf=True, sublinear_tf=True)),
                         ('clf', SGDRegressor(alpha=1e-09, power_t=1e-07
                                    ))])
    param_grid = {#'vect__min_df': (50, 200, 100),
                  #'vect__max_df': (30000,40000,50000)
                  'vect__max_features': (25000, 50000, 75000)
                  #'vect__norm': ('l2', 'l1')
                  #'vect__use_idf': (True, False)
                  #'vect__sublinear_tf': (True, False)
                  #'clf__alpha': (0.001, 0.00000001, 0.000000001),
                  #'clf__power_t': (1e-05, 1e-06, 1e-07)
                  #'clf__penalty': ('l1', 'l2', 'elasticnet')
                  }

    Bigram_cv = GridSearchCV(pipeline, param_grid=param_grid, cv=3,
                             scoring='mean_squared_error', verbose=2, n_jobs=4)
    Bigram_model = Bigram_cv.fit(X_train, y_train)
    print Bigram_model.grid_scores_
    print Bigram_model.best_params_
    return Bigram_model
    """
    # Actual run
    # max_df=10000, max_features=1000,10000 lowered score 
    vect = TfidfVectorizer(stop_words=stopwords.words('english'), 
                           ngram_range=(1,2), min_df=50, max_df=40000, norm='l2',
                           max_features=50000, use_idf=True, sublinear_tf=True)
    vect.fit(X_review)
    pipeline = Pipeline([('vect2', TfidfVectorizer(vocabulary=vect.vocabulary_,
                                                   ngram_range=(1,2), norm='l2',
                                                   use_idf=True, sublinear_tf=True)),
                         ('clf', SGDRegressor(alpha=1e-09, power_t=1e-07,
                                              penalty='l2'))])
    Bigram_model = pipeline.fit(X_review, y)

    joblib.dump(Bigram_model, 'Bigram_model_sgd.pkl')
     
    return Bigram_model
    
def main():
    with gzip.open('yelp_reviews.json.gz', 'rb') as infile:
        f = [json.loads(line) for line in infile.readlines()]

    y = [i['stars'] for i in f]
    BG = Bigram(f, y)

    print BG.predict(['Everything was great except for the burgers they are greasy and very charred compared to other stores.'])
    
if __name__ == '__main__':
    main()
