
from flask import Flask, request, jsonify
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from flask_cors import CORS
import os

from src.prompt import system_prompt
from src.helper import download_embeddings


load_dotenv()

# Set env Variables
PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
HUGGINGFACE_TOKEN=os.environ.get('HUGGINGFACE_TOKEN')

os.environ["PINECONE_API_KEY"]=PINECONE_API_KEY
os.environ["HUGGINGFACE_TOKEN"]=HUGGINGFACE_TOKEN


# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow requests from frontend (CORS)



embeddings= download_embeddings()
index_name="medical-bot"

#Load Existing index and retriever
docsearch = PineconeVectorStore.from_existing_index(
    embedding=embeddings,
    index_name=index_name
)

retriever=docsearch.as_retriever(search_type="similarity",search_kwargs={'k':3})



#Loading LLM
HUGGINGFACE_REPO_ID="mistralai/Mistral-7B-Instruct-v0.3"
# print(HUGGINGFACE_TOKEN)

def load_llm(huggingface_repo_id):
    llm=HuggingFaceEndpoint(
        repo_id=huggingface_repo_id,
        task="text-generation",
        temperature=0.5,
        max_new_tokens=512,
        huggingfacehub_api_token=os.environ["HUGGINGFACE_TOKEN"]
    )
    return llm


# Custom Prompt Setup
def set_custom_prompt(custom_prompt_template):
    prompt=PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])
    return prompt


#Build the RetrievalQA Chain
qa_chain=RetrievalQA.from_chain_type(
    llm=load_llm(HUGGINGFACE_REPO_ID),
    chain_type="stuff",
    retriever=docsearch.as_retriever(search_type="similarity",search_kwargs={'k':3}),
    return_source_documents=True,
    chain_type_kwargs={'prompt':set_custom_prompt(system_prompt)}
)


# Define Route to handle Chatbot
@app.route("/chat", methods=["POST","GET"])
def chat():
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    try:
        result = qa_chain.invoke({"query": user_query})
        return jsonify({
            "query": user_query,
            "response": result["result"],
            "sources": [doc.metadata for doc in result["source_documents"]]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return "Medical Chatbot Backend is running."


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=8000)