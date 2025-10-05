from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv()


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that generates clean and funny jokes."),
    ("human", "Tell me a joke about {topic}.")
])

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

output_parser = StrOutputParser()

# Prompt Template | Model or LLM | Parser
chain = prompt | model | output_parser

app = FastAPI(
    title="Joke GenAI",
    version="0.1"
)

# add_routes(
#     app,
#     chain,
#     path="/chat"
# )


class JokeRequest(BaseModel): 
    topic: str

@app.post("/chat")
async def generate_joke(request: JokeRequest): 
    try: 
        result = await chain.ainvoke({ "topic": request.topic })
        return { "joke": result }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {
        "message" : "welcome to JokeGenAI"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=9000)