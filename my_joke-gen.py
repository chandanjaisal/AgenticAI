from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langserver import add_routes
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a funny assistant that tells jokes."),
    ("human", "{topic}")
])

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

parser = StrOutputParser()
#prompt template is first | then LLM | Parser 
chain = prompt | llm | parser
app = FastAPI(
    title="Joke Generation API",
    description="An API to generate jokes on a given topic using Google Gemini.",
    version="1.0.0"
)
add_routes(app, chain,path="/chat")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Joke Generation API!"}

# The add_routes function is assumed to be defined in langserver.py
# It should add the necessary routes to the FastAPI app to handle requests and responses.
# Make sure to replace 'your_google_api_key' with your actual Google API key.
# The GOOGLE_API_KEY is now fetched from the environment variable for better security.

# To run the app, use the command: uvicorn joke-gen:app --reload
# Ensure you have uvicorn installed: pip install uvicorn
# The app will be accessible at http://localhost:9000/chat