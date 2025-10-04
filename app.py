from langchain_google_genai import ChatGoogleGenerativeAI #to connect with Gemini
from langchain.prompts import ChatPromptTemplate #to create prompts
from langchain.schema.output_parser import StrOutputParser #to parse the output

def main():

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key="AIzaSyASdtyNIG80nXd6iNEv-USnLaMxURQNx0k",
        temperature=0.7
    )
    
    #if temperature is 1 or near 1, the output will be very hallucination for creative work 
    #if temperature is 0 or near 0, the output will be very accurate
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that helps people find information."),
        ("human", "{question}")
    ])

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({"question": "What is the capital of India?"})
    
    print(response)

if __name__ == "__main__":
   main()