from typing import Dict, List
import sys
import os
import json
import numpy as np
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

import autogen
from autogen import ConversableAgent, AssistantAgent, UserProxyAgent
from autogen import register_function

import sys
sys.path.append("/home/den/projects/LLM/llm_agents_course/labs")
from lab01_release.utils import review_analysis_message, get_review_dict, extract_content

# Load environment variables from .env file
load_dotenv()

# Accessing the variables
openai_token = os.getenv('OPENAI_API_KEY')

llm_config = {"config_list": [{"model": "gpt-4o", "api_key": os.environ.get("OPENAI_API_KEY")}]}

llm_manager_config = {"config_list": [{"model": "gpt-4o", "api_key": os.environ.get("OPENAI_API_KEY")}]}

##############
# user_proxy = autogen.UserProxyAgent(
#     name="User_proxy",
#     system_message="A human admin.",
#     human_input_mode="TERMINATE",
# )
part1 = autogen.AssistantAgent(
    name="Louis_CK",
    system_message="You are a famous comedian",
    llm_config=llm_config,
)
part2 = autogen.AssistantAgent(
    name="George_Carlin",
    system_message="You are a famous comedian",
    llm_config=llm_config,
)
part3 = autogen.AssistantAgent(
    name="Lesha_Kvashonkin",
    system_message="You are a russian aspiring comedian",
    llm_config=llm_config,
)
part4 = autogen.AssistantAgent(
    name="Ilya_Sutskever",
    system_message="You are a neural network training specialist from openai",
    llm_config=llm_config,
)
groupchat = autogen.GroupChat(agents=[part1, part2, part3, part4], messages=[], send_introductions=False, max_round=25)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_manager_config)

##############
dt = (
    str(datetime.now().replace(microsecond=0))
    .replace(" ", "_")
    .replace(":", "_")
    .replace("-", "_")
)

with open(f"standup/results/{dt}.txt", "w") as f:
    sys.stdout = f
    ########### 
    part1.initiate_chat(
        manager, message="Lets write a jokes about artificial intelligence for stand up concert. We should decide in discussion which one of them is good enough"
    )