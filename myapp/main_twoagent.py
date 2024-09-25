import os
import logging
from datetime import datetime
from autogen import AssistantAgent, UserProxyAgent
from openai import OpenAI
import pprint
import traceback

# ------------------------------
# Logging Configuration
# ------------------------------

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure the execution logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/execution_log.txt")
    ]
)
logger = logging.getLogger("execution_logger")

# ------------------------------
# API Key Loading
# ------------------------------

def load_api_key():
    """Load OpenAI API key from environment variable or file."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        try:
            with open('openai_key.txt', 'r', encoding='utf-8') as f:
                api_key = f.read().strip()
        except FileNotFoundError:
            logger.error("OpenAI API key not found. Please set the 'OPENAI_API_KEY' environment variable or provide 'openai_key.txt'.")
            exit(1)
        except Exception as e:
            logger.error(f"An error occurred while reading the API key: {e}")
            exit(1)
    
    # Adjusted API Key Validation for Custom Models
    if not (api_key.startswith("sk-") and len(api_key) > 20):
        logger.warning("The API key specified may not be a standard OpenAI format; ensure it's correct for your custom model.")
    
    return api_key

# Load the API key
api_key = load_api_key()
logger.info(f"Using OpenAI API Key: {api_key[:5]}***")  # Log only the first 5 characters for security

# ------------------------------
# Configuration
# ------------------------------

# LLM Configuration
llm_config = {
    "model": "gpt-4o",  # Ensure this matches your custom model's identifier
    "api_key": api_key,
    "temperature": 0.5
}

# Code Execution Configuration
code_execution_config = {
    "timeout": 60,  # Timeout for each code execution in seconds.
    "use_docker": True  # Explicitly set to True to use Docker (default)
}

# ------------------------------
# Agent Definitions
# ------------------------------

# Developer Agent
developer_agent = AssistantAgent(
    name="Developer",
    llm_config=llm_config,
    system_message=(
        "You are an autonomous developer tasked with creating simple Python programs "
        "that will run in the terminal. "
        "Write the code step by step, and adjust based on feedback from the tester. "
        "Provide code in executable Python code blocks. Do not include explanations within the code blocks. "
        "Take special care to exhaustively create tests for the tester to run, attempting to encapsulate all desired functionality."
        "Do not include any time-wasting pleasentries like 'Hello!', 'Have a nice day!', 'Goodbye!' or related statements."
        "Do not respond to 'TERMINATE' at all."
    ),
    human_input_mode="NEVER",
    code_execution_config=False,  # Developer does not execute code
    #is_termination_msg=lambda msg: "TERMINATE" in msg["content"].lower(),
)

# Tester Agent
tester_agent = UserProxyAgent(
    name="Tester",
    llm_config=llm_config,
    system_message=(
        "You are an autonomous tester with Python code execution capabilities. "
        "When you receive code, extract it, execute it, and report any errors or issues back to the developer. "
        "Provide detailed error messages and a comprehensive summary of the output, highlighting how it differs from the expected behavior. "
        "If the code execution does not produce any output within 60 seconds, terminate the execution and inform the developer about the timeout. "
        "You can also provide suggestions for improvements or additional functionality if applicable. "
        "When the calculator works correctly, has no further errors, and you do not see any functionality to add further, "
        "Do not include any time-wasting pleasentries like 'Hello!', 'Have a nice day!', 'Goodbye!' or related statements."
        "You will respond with the termination message 'TERMINATE'."
    ),
    human_input_mode="NEVER",
    code_execution_config=code_execution_config,  # Tester can execute code inside Docker
    is_termination_msg=lambda msg: "terminate" in msg["content"].lower(),
)

# ------------------------------
# Start the Conversation
# ------------------------------

def start_conversation():
    try:
        # Initiate the chat between Tester and Developer agents
        chat_result = tester_agent.initiate_chat(
            developer_agent,
            message=(
                "I would like you to create an arithmetic calculator that can process any arithmetic formula consisting of digits and the operators +, -, /, *. "
                "The calculator should take a string input representing the formula and return the computed result. "
                "Instead of using input(), define the formula within the code for testing purposes. "
                "You will now output your code:"
            ),
            summary_method="reflection_with_llm",
            max_turns=30  # Reduced from 30 to prevent excessive turns
        )
        
        # Print the summary of the conversation
        print("----- Chat Summary -----")
        print(chat_result.summary)
        print("------------------------")
        
        # Optionally, print the full chat history
        print("----- Chat History -----")
        pprint.pprint(chat_result.chat_history)
        print("------------------------")
        
        # Print the cost of the chat
        print("----- Chat Cost -----")
        pprint.pprint(chat_result.cost)
        print("---------------------")
        
        # Analyze chat history for timeout indications
        for message in chat_result.chat_history:
            content = message.get("content", "").lower()
            if "timeout" in content or "execution timed out" in content:
                print("----- Timeout Detected -----")
                print("A code execution timed out. Please review the Developer Agent's code for potential issues.")
                print("----------------------------")
                break
                
    except Exception as e:
        logger.error(f"An error occurred during the chat: {e}")
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    start_conversation()
