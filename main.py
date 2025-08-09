import os
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from prompt import prompt_template
from tools import tools
from web_app.db import insert_mood_log  # ✅ Import MySQL logging function

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=api_key
)

# Create the agent (without output_parser)
agent = create_openai_functions_agent(
    llm=llm,
    prompt=prompt_template,
    tools=tools,
)

# Set up the executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Start the interactive bot
if __name__ == "__main__":
    print("🧠 Mental Health Check-in Bot (Gemini API Mode)")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye! Take care of yourself 💙")
            break

        try:
            response = agent_executor.invoke({"input": user_input})
            output = response.get("output", "")

            # Extract Mood, Reason, Suggestion using regex
            mood_match = re.search(r'Mood:\s*(.*)', output)
            reason_match = re.search(r'Reason:\s*(.*)', output)
            suggestion_match = re.search(r'Suggestion:\s*(.*)', output)

            # Clean output display
            mood = mood_match.group(1).strip() if mood_match else 'N/A'
            reason = reason_match.group(1).strip() if reason_match else 'N/A'
            suggestion = suggestion_match.group(1).strip() if suggestion_match else 'N/A'

            print("\nBot Response:")
            print(f"Mood: {mood}")
            print(f"Reason: {reason}")
            print(f"Suggestion: {suggestion}\n")

            # ✅ Insert into MySQL
            if mood != 'N/A' and reason != 'N/A' and suggestion != 'N/A':
                insert_mood_log(user_input, mood, reason, suggestion)

        except Exception as e:
            print("Something went wrong:", e)
