import autogen
from autogen import UserProxyAgent, AssistantAgent
from config import llama_config
from agent_prompts import content_prompt, priority_prompt, response_prompt
from langchain_core.output_parsers import JsonOutputParser

from utils import detect_spam, is_internal_email
import json

# Define Agents
content_agent = AssistantAgent(
    name="ContentAgent",
    system_message=content_prompt,
    llm_config=llama_config,
)

priority_agent = AssistantAgent(
    name="PriorityAgent",
    system_message=priority_prompt,
    llm_config=llama_config,
)

response_agent = AssistantAgent(
    name="ResponseAgent",
    system_message=response_prompt,
    llm_config=llama_config,
)

# Register utility functions
content_agent.register_for_execution()(is_internal_email)
priority_agent.register_for_execution()(detect_spam)

# Define User Proxy
user_proxy = UserProxyAgent(
    name="UserAgent",
    system_message="You are the user providing email content for analysis.",
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False}
)

# Define State Transition
def state_transition(last_speaker, groupchat):
    if last_speaker is user_proxy:
        return content_agent
    elif last_speaker is content_agent:
        return priority_agent
    elif last_speaker is priority_agent:
        return response_agent
    return None

# Group Chat Setup
groupchat = autogen.GroupChat(
    agents=[user_proxy, content_agent, priority_agent, response_agent],
    messages=[],
    max_round=4,
    speaker_selection_method=state_transition,
)

groupchat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llama_config)


# Main Email Processing Function
def process_email(sender, subject, body, user_email, additional_info):
    """
    Process email using Llama agents.
    """
    email_message = f"""
    Sender: {sender}
    Subject: {subject}
    Body: {body}
    User email: {user_email}
    Additional Info: {additional_info}
    """
    user_proxy.initiate_chat(groupchat_manager, message=email_message)
    # print(groupchat.messages[1])
    # print(groupchat.messages[3])

    # Extract messages
    raw_messages = groupchat.messages

    def sanitize_and_parse_json(message):
        """
        Replace invalid values like 'None' with valid JSON equivalents and parse.
        """
        try:
            return json.loads(message)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing message: {message}, Error: {e}")
            return {}

    # Parse each agent's response
    content_analysis = sanitize_and_parse_json(raw_messages[1]["content"])
    priority_decision = sanitize_and_parse_json(raw_messages[2]["content"])
    response_action = sanitize_and_parse_json(raw_messages[3]["content"])

    print(response_action)
    print(response_action["action"])
    print("2")
    return {
        "content_analysis": content_analysis,
        "priority_decision": priority_decision,
        "response_action": response_action,
    }
