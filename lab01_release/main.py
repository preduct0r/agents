from typing import Dict, List
from autogen import ConversableAgent, AssistantAgent
import sys
import os
import json
import numpy as np
from dotenv import load_dotenv

from lab01_release.utils import entrypoint_agent_system_message, review_analysis_system_message, get_review_dict

# Load environment variables from .env file
load_dotenv()

# Accessing the variables
openai_token = os.getenv('OPENAI_API_KEY')

review_dict = get_review_dict

def fetch_restaurant_data(restaurant_name: str) -> Dict[str, List[str]]:
    # TODO
    # This function takes in a restaurant name and returns the reviews for that restaurant. 
    # The output should be a dictionary with the key being the restaurant name and the value being a list of reviews for that restaurant.
    # The "data fetch agent" should have access to this function signature, and it should be able to suggest this as a function call. 
    # Example:
    # > fetch_restaurant_data("Applebee's")
    # {"Applebee's": ["The food at Applebee's was average, with nothing particularly standing out.", ...]}
    return review_dict[restaurant_name]

def check_task1_termination(message):
    if "content" in message:
        try:
            d = json.loads(message["content"])
            if len(d.keys()) == 1 and isinstance(d[d.keys()[0]], list):
                return True
        except:
            return False
    return False
        

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

def get_data_fetch_agent_prompt(restaurant_query: str) -> str:
    # TODO
    # It may help to organize messages/prompts within a function which returns a string. 
    # For example, you could use this function to return a prompt for the data fetch agent 
    # to use to fetch reviews for a specific restaurant.
    pass

# TODO: feel free to write as many additional functions as you'd like.

# Do not modify the signature of the "main" function.
def main(user_query: str):
    # example LLM config for the entrypoint agent
    llm_config = {"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API_KEY")}]}
    # the main entrypoint/supervisor agent
    entrypoint_agent = ConversableAgent("entrypoint_agent", 
                                        system_message=entrypoint_agent_system_message, 
                                        is_termination_msg=check_task1_termination,
                                        llm_config=llm_config, 
                                        max_consecutive_auto_reply=5)
    entrypoint_agent.register_for_llm(name="fetch_restaurant_data", description="Fetches the reviews for a specific restaurant.")(fetch_restaurant_data)
    entrypoint_agent.register_for_execution(name="fetch_restaurant_data")(fetch_restaurant_data)

    # TODO
    review_analysis_agent = AssistantAgent("review_analysis_agent", 
                                        system_message=review_analysis_system_message, 
                                        llm_config=llm_config,
                                        max_consecutive_auto_reply=5)
    
    scoring_agent = AssistantAgent("scoring_agent", 
                                        system_message=None, 
                                        llm_config=llm_config,
                                        max_consecutive_auto_reply=5)
    
    scoring_agent.register_for_llm(name="calculate_overall_score", description="Return overall score.")(fetch_restaurant_data)
    scoring_agent.register_for_execution(name="calculate_overall_score")(fetch_restaurant_data)
    # TODO
    # Fill in the argument to `initiate_chats` below, calling the correct agents sequentially.
    # If you decide to use another conversation pattern, feel free to disregard this code.
    
    # Uncomment once you initiate the chat with at least one agent.
    chat_results = entrypoint_agent.initiate_chats(
        [
            {
                "recipient": review_analysis_agent,
                "message": "",
                "max_turns": 3,
                "summary_method": "reflection_with_llm",
            },
            {
                "recipient": scoring_agent,
                "message": "",
                "max_turns": 3,
                "summary_method": "last_msg",
            },
        ]
    )
    
    
# DO NOT modify this code below.
if __name__ == "__main__":
    assert len(sys.argv) > 1, "Please ensure you include a query for some restaurant when executing main."
    main(sys.argv[1])