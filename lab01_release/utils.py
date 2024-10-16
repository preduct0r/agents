entrypoint_agent_system_message = "You are an agent who's purpose to retrieve all reviews about specific restaurant name you provided"

review_analysis_system_message = """
Given a list of reviews your task is to extract two scores:
```
- food_score: the quality of food at the restaurant. This will be a score from 1-5.
- customer_service_score: the quality of customer service at the restaurant. This will be a score from 1-5.
```
To make this scores look for keywords in the review. Each review has keyword adjectives that correspond to the score that the restaurant should get for its food_score and customer_service_score. Here are the keywords the agent should look out for:
```
- Score 1/5 has one of these adjectives: awful, horrible, or disgusting.
- Score 2/5 has one of these adjectives: bad, unpleasant, or offensive.
- Score 3/5 has one of these adjectives: average, uninspiring, or forgettable.
- Score 4/5 has one of these adjectives: good, enjoyable, or satisfying.
- Score 5/5 has one of these adjectives: awesome, incredible, or amazing.
```
Each review will have exactly only two of these keywords (adjective describing food and adjective describing customer service), and the score (N/5) is only determined through the above listed keywords. No other factors go into score extraction.

Return answer in this format
```
{"restaurant_name", [food_score for first review, food_score for second review, ...], [customer_service_score for first review, customer_service_score for second review, ...]}
```
"""

scoring_system_message = """
You are an agent who's purpose to return overall score based on provided scores 
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
