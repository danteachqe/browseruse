import asyncio
import os
from langchain_openai import ChatOpenAI
from browser_use import Agent, BrowserConfig, Browser
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Configure browser settings
browser_config = BrowserConfig(
    headless=True,  # Run in headless mode
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
task = "On the base page of www.blazedemo.com, create a page object model compatible with Selenium and Java for all the elements of the page, follow coding best practices around automated testing. Make sure to give me just java code, no comments."

async def main():
    agent = Agent(
        browser_context=context,  # Use context instead of config
        task=task,
        llm=llm,
    )
    result = await agent.run()

    # Extract the text response from AgentHistoryList
    extracted_text = result.to_text() if hasattr(result, "to_text") else str(result)

    # Specify the file to save the results
    output_file = "Pom.txt"

    # Write the extracted text to the file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(extracted_text)

    print(f"Results saved to {output_file}")

# Run the asynchronous function
asyncio.run(main())
