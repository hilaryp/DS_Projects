# Use data from ML miniproject to figure out which reviews are for restaurants
import gzip
import pickle
import simplejson as json

def get_IDs():
    with gzip.open('../ml_src/data.json.gz', 'rb') as infile:
        f = [json.loads(line) for line in infile.readlines()] 
    
    IDs = [record['business_id'] for record in f 
            if 'Restaurants' in record['categories']]
    return IDs

def match_IDs(ID_list):
    with gzip.open('./yelp_reviews.json.gz', 'rb') as infile:
        f = [json.loads(line) for line in infile.readlines()]

    restrev = [rev for rev in f if rev['business_id'] in ID_list]
    print restrev[0]
    return restrev

def main():
    IDs = get_IDs()
    rest_reviews = match_IDs(IDs)    
    
    with open('restaurant_reviews.pkl', 'wb') as outfile:
        pickle.dump(rest_reviews, outfile)

if __name__ == '__main__':
    main()
