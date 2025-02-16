from langchain_openai import ChatOpenAI
from browser_use import Agent, BrowserConfig, Browser
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from dotenv import load_dotenv
import asyncio
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Configure browser settings
browser_config = BrowserConfig(
    headless=False,  # Set to True for headless mode
    disable_security=True
)

# Define browser context configuration
context_config = BrowserContextConfig(
    wait_for_network_idle_page_load_time=3.0,
    browser_window_size={'width': 1280, 'height': 1100},
    locale='en-US',
    highlight_elements=True,
    viewport_expansion=500,
)

# Initialize browser and context
browser = Browser(config=browser_config)
context = BrowserContext(browser=browser, config=context_config)

# Initialize the AI model
llm = ChatOpenAI(model="gpt-4o")

# Define the task for the AI agent
task = "Find the cheapest nonstop flight from Dubai to COK (Cochin) in economy class for tomorrow for one passenger."

async def main():
    agent = Agent(
        browser_context=context,  # Use context instead of config
        task=task,
        llm=llm,
    )
    result = await agent.run()
    print("Cheapest Flight Details:", result)

# Run the asynchronous function
asyncio.run(main())