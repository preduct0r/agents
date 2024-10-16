import re


review_analysis_message = """
Given a list of reviews your task is to extract two scores:
```
- food_score: the quality of food at the restaurant. This will be a score from 1-5.
- customer_service_score: the quality of customer service at the restaurant. This will be a score from 1-5.
```
Make this scores look for keywords in the reviews. Each review has keyword adjectives that correspond to the score that the restaurant should get for its food_score and customer_service_score. Here are the keywords the agent should look out for:
```
- Score 1 has one of these adjectives: awful, horrible, or disgusting.
- Score 2 has one of these adjectives: bad, unpleasant, or offensive.
- Score 3 has one of these adjectives: average, uninspiring, or forgettable.
- Score 4 has one of these adjectives: good, enjoyable, or satisfying.
- Score 5 has one of these adjectives: awesome, incredible, or amazing.
```
Each review will have exactly only two of these keywords (adjective describing food and adjective describing customer service), and the score N is only determined through the above listed keywords. No other factors go into score extraction.

Return answer in format, like in this example. It must be strictly JSON data without anything else
```
{"restaurant_name": "Applebee's", "food_scores": [1, 2, 3, 4, 5], "customer_service_scores": [1, 2, 3, 4, 5]}
```
"""


def get_review_dict():
    with open("lab01_release/restaurant-data.txt") as f:
            reviews = f.read().split("\n")
    review_dict = {}
    for review in reviews:
        rest_name = review.split(".")[0].lower()
        text = review.replace(review.split(".")[0] + ".", "")
        if rest_name in review_dict:
            review_dict[rest_name].append(text)
        else:
            review_dict[rest_name] = [text]
    return review_dict

def extract_content(text):
    pattern2 = r"^.*?(\{.*\}).*$"
    match = re.search(pattern2, text, re.DOTALL)
    return match.group(1) if match else text
