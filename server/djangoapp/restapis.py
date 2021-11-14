import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions, EntitiesOptions, KeywordsOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    try:
        if 'api_key' in kwargs:
            authenticator = IAMAuthenticator(kwargs["api_key"])
            natural_language_understanding = NaturalLanguageUnderstandingV1(
                version=kwargs["version"],
                authenticator=authenticator
            )
            natural_language_understanding.set_service_url(url)
            response = natural_language_understanding.analyze(
                text=kwargs["text"],
                features=Features(
                    entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
                    keywords=KeywordsOptions(emotion=True, sentiment=True, limit=2)
                ),
                language="en"
            ).get_result()
            json_data = json.dumps(response, indent=2)
        else:
            response = requests.get(
                url=url,
                params=kwargs, 
                headers={'Content-Type': 'application/json'}
            )
            json_data = json.loads(response.text)
    except Exception as e:
        # If any error occurs
        print("Network exception occurred")
        print(f"Exception: {e}")
    return json_data


# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    json_data = json.dumps(json_payload, indent=4)
    print(f"{json_data}")
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, params=kwargs, json=json_data)
    except Exception as e:
        # If any error occurs
        print("Network exception occurred")
        print(f"Exception: {e}")
    print(f"With status {response.status_code}")
    print(f"Response: {response.text}")

        
# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer["address"], 
                city=dealer["city"], 
                full_name=dealer["full_name"], 
                id=dealer["id"], 
                lat=dealer["lat"], 
                long=dealer["long"], 
                short_name=dealer["short_name"], 
                st=dealer["st"], 
                zip=dealer["zip"])
            results.append(dealer_obj)
    return results


# Create a get_dealer_by_state method
def get_dealer_by_state(url, state):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state=state)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id 
# from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request() with specified arguments
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Parse JSON results into a DealerView object list
        reviews = json_result['reviews']
        for review in reviews:
            try:
                review_obj = DealerReview(
                    dealership = review["dealership"], 
                    purchase=review["purchase"], 
                    purchase_date = review["purchase_date"], 
                    car_make = review['car_make'], 
                    car_model = review['car_model'], 
                    car_year= review['car_year'], 
                    name = review["name"], 
                    review = review["review"], 
                    sentiment= "none")
            except:
                review_obj = DealerReview(
                    dealership = review["dealership"], 
                    purchase=review["purchase"], 
                    purchase_date = "none", 
                    car_make = "none", 
                    car_model = "none", 
                    car_year= "none", 
                    name = review["name"], 
                    review = review["review"], 
                    sentiment= "none")
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)                  
            results.append(review_obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/f646a96c-5571-4cc2-9db0-a7b0f2917804/"
    api_key = "6iGRq0XAZZTdWIKO2HOENAj-t_7vLlhmhXUjXubi1dIG"
    version = "2021-03-25"
    features = ["sentiment"]
    language = "en"
    return_analyzed_text = False
    # Call get_request() with specified arguments
    result = get_request(
        url=url,
        api_key=api_key,
        text=text, 
        version=version,
        features=features,
        language=language,
        return_analyzed_text=return_analyzed_text
    )
    # Get the returned sentiment label such as Positive or Negative
    return result
