from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
import os
from dotenv import load_dotenv
load_dotenv()

api_base_url = 'https://openrouter.ai/api/v1'

root_agent = Agent(
    model=LiteLlm(
        model='openrouter/deepseek/deepseek-v3.2',
        api_base=api_base_url,
        api_key=os.getenv('OPENROUTER_API_KEY'),
    ),
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
