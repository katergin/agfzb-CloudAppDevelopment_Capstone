import requests
import json

from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(
            url, 
            headers={'Content-Type': 'application/json'}, 
            params=kwargs
        )
    except Exception as e:
        # If any error occurs
        traceback.print_exc()
        print("Network exception occurred")
        print(f"Exception: {e}")
    status_code = response.status_code
    print(f"With status {status_code} ")
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
def post_request(url, payload, **kwargs):
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print(f"With status {status_code}")
    json_data = json.loads(response.text)
    return json_data

        
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
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        reviews = json_result['reviews']
        for review in reviews:
            if review["purchase"] == True:
                review_obj = DealerReview(
                    dealership = review["dealership"], 
                    purchase = review["purchase"], 
                    purchase_date = review["purchase_date"], 
                    car_make = review['car_make'], 
                    car_model = review['car_model'], 
                    car_year= review['car_year'], 
                    name = review["name"], 
                    review = review["review"], 
                    sentiment = "none")
            else:
                review_obj = DealerReview(
                    dealership = review["dealership"], 
                    purchase = review["purchase"], 
                    purchase_date = "none", 
                    car_make = "none", 
                    car_model = "none", 
                    car_year= "none", 
                    name = review["name"], 
                    review = review["review"], 
                    sentiment = "none")
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/c135db14-2f05-4ceb-b0c1-e20f4634614f"
    api_key = "2Ss24dHHwz3kupauOTkFswbW5DtdIgceqlGsK8g034Jl"
    authenticator = IAMAuthenticator(apikey=api_key)
    nlu = NaturalLanguageUnderstandingV1(
        version='2021-08-01',
        authenticator=authenticator
    )
    nlu.set_service_url(url)

    response = nlu.analyze(
        text=text,
        features=Features(sentiment=SentimentOptions(document=True)),
        language="en"
        ).get_result()

    print(json.dumps(response, indent=2))
    sentiment = response["sentiment"]["document"]["label"]
    print(f"sentiment: {sentiment}")
    return sentiment
