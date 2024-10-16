from typing import Dict, List
import sys
import os
import json
import numpy as np
from dotenv import load_dotenv

from autogen import ConversableAgent, AssistantAgent, UserProxyAgent
from autogen import register_function

import sys
sys.path.append("/home/den/projects/LLM/llm_agents_course/labs")
from lab01_release.utils import review_analysis_message, get_review_dict, extract_content

# Load environment variables from .env file
load_dotenv()

# Accessing the variables
openai_token = os.getenv('OPENAI_API_KEY')

review_dict = get_review_dict()



def fetch_restaurant_data(restaurant_name: str) -> Dict[str, List[str]]:
    # TODO
    # This function takes in a restaurant name and returns the reviews for that restaurant. 
    # The output should be a dictionary with the key being the restaurant name and the value being a list of reviews for that restaurant.
    # The "data fetch agent" should have access to this function signature, and it should be able to suggest this as a function call. 
    # Example:
    # > fetch_restaurant_data("Applebee's")
    # {"Applebee's": ["The food at Applebee's was average, with nothing particularly standing out.", ...]}    
    if restaurant_name.lower() in review_dict.keys():
        return review_dict[restaurant_name.strip().lower()]
    else:
        raise ValueError("Invalid operator")
        

def calculate_overall_score(restaurant_name: str, food_scores: List[int], customer_service_scores: List[int]) -> Dict[str, float]:
    # TODO
    # This function takes in a restaurant name, a list of food scores from 1-5, and a list of customer service scores from 1-5
    # The output should be a score between 0 and 10, which is computed as the following:
    # SUM(sqrt(food_scores[i]**2 * customer_service_scores[i]) * 1/(N * sqrt(125)) * 10
    # The above formula is a geometric mean of the scores, which penalizes food quality more than customer service. 
    # Example:
    # > calculate_overall_score("Applebee's", [1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    # {"Applebee's": 5.048}
    # NOTE: be sure to that the score includes AT LEAST 3  decimal places. The public tests will only read scores that have 
    # at least 3 decimal places.
    average_score = np.sum([np.sqrt(food_scores[i]**2 * customer_service_scores[i]) * 1/(len(food_scores) * np.sqrt(125)) * 10 for i in range(len(food_scores))])
    
    return {restaurant_name: round(average_score, 3)}

def get_average_score(js: str):
    json.loads(extract_content(js))
    return calculate_overall_score(js["restaurant_name"], js["food_scores"], js["customer_service_scores"])


# TODO: feel free to write as many additional functions as you'd like.

def check_json(data):
    try:
        json.loads(data)
        return True
    except:
        return False
    

# Do not modify the signature of the "main" function.
def main(user_query: str):
    # example LLM config for the entrypoint agent
    llm_config = {"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API_KEY")}]}
    # the main entrypoint/supervisor agent

    # TODO
    #############
    user_proxy = UserProxyAgent(
        name="user", 
        llm_config=False,
        # is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
    )
    retrieve_name_agent = AssistantAgent(
        name="get_name_agent",
        system_message="You are a helpful AI assistant. You help to retrieve necessary information from given query",
        llm_config=llm_config,
    )
    
    #############
    retrieve_reviews_agent = AssistantAgent(
        name="get_reviews_agent",
        system_message="You are a helpful AI assistant. You help with tool usage",
        llm_config=llm_config,
    )
    
    register_function(
        fetch_restaurant_data,
        caller=retrieve_reviews_agent,  # The assistant agent can suggest calls to the calculator.
        executor=user_proxy,  # The user proxy agent can execute the calculator calls.
        name="retrieval",  # By default, the function name is used as the tool name.
        description="get data from dictionary",  # A description of the tool.
    )
    
    #############
    reviews_analysis_agent = AssistantAgent("review_analysis_agent", 
        system_message="You are a helpful AI assistant. You help to analyze reviews",
        llm_config=llm_config,
    )
    
    #############
    scoring_agent = AssistantAgent("scoring_agent", 
        system_message="You are a helpful AI assistant", 
        llm_config=llm_config,
    )
    
    register_function(
        calculate_overall_score,
        caller=scoring_agent,  # The assistant agent can suggest calls to the calculator.
        executor=user_proxy,  # The user proxy agent can execute the calculator calls.
        name="average_score",  # By default, the function name is used as the tool name.
        description="get final score",  # A description of the tool.
    )
    
    
    
    # TODO
    # Fill in the argument to `initiate_chats` below, calling the correct agents sequentially.
    # If you decide to use another conversation pattern, feel free to disregard this code.
    
    # Uncomment once you initiate the chat with at least one agent.
    #############
    chat_results = user_proxy.initiate_chats([
            {
                "message": f"Return restaurant name from given query. **Query**: ```{user_query}```\n You must return only name, nothing else",
                "recipient": retrieve_name_agent,
                "summary_method": "last_msg",
                "max_turns": 1,
            },            
            {
                "message": f"Get all reviews for given restaurant name",
                "recipient": retrieve_reviews_agent,
                "summary_method": "last_msg",
                "max_turns": 2,
            },
            {
                "message": review_analysis_message,
                "recipient": reviews_analysis_agent,
                "summary_method": "last_msg",
                "max_turns": 2,
            },
            {
                "message": "Return average score. Strictly in JSON format",
                "recipient": scoring_agent,
                "summary_method": "last_msg",
                "max_turns": 2,
            }                             
        ]                                         
    )
    print()
    
    
# DO NOT modify this code below.
if __name__ == "__main__":
    assert len(sys.argv) > 1, "Please ensure you include a query for some restaurant when executing main."
    main(sys.argv[1])