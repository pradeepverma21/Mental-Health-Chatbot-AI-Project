import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request
import os
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from tools import tools
from prompt import prompt_template
from db import insert_mood_log

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=api_key
)

# Create agent and executor
agent = create_openai_functions_agent(
    llm=llm,
    prompt=prompt_template,
    tools=tools,
)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

# Flask app
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    mood, reason, suggestion, user_input = "", "", "", ""

    if request.method == "POST":
        user_input = request.form.get("user_input", "")

        try:
            result = agent_executor.invoke({"input": user_input})
            output = result.get("output", "")

            # Extract Mood, Reason, Suggestion
            mood_match = re.search(r'Mood:\s*(.*)', output)
            reason_match = re.search(r'Reason:\s*(.*)', output)
            suggestion_match = re.search(r'Suggestion:\s*(.*)', output)

            mood = mood_match.group(1).strip() if mood_match else "N/A"
            reason = reason_match.group(1).strip() if reason_match else "N/A"
            suggestion = suggestion_match.group(1).strip() if suggestion_match else "N/A"

            # Save to MySQL
            insert_mood_log(user_input, mood, reason, suggestion)

        except Exception as e:
            suggestion = f"Something went wrong: {e}"

    return render_template("chats.html", user_input=user_input, mood=mood, reason=reason, suggestion=suggestion)

@app.route("/home")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
