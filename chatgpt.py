import os
import sys
from flask import Flask, request,render_template
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
import openai
from dotenv import load_dotenv, set_key, find_dotenv

app = Flask(__name__)
import constants

os.environ["OPENAI_API_KEY"] = constants.openai_api_key

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

query = None

if PERSIST and os.path.exists("persist"):
    print("Reusing index...\n")
    vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
    index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
    # loader = TextLoader("data/data.txt") # Use this line if you only need data.txt
    loader = DirectoryLoader("data/")
    if PERSIST:
        index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
    else:
        index = VectorstoreIndexCreator().from_loaders([loader])

chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

chat_history = []

@app.route('/', methods=['GET', 'POST'])
def chat():
    global query
    if request.method == 'POST':
        query = request.form['query']
    if not query:
        return render_template('index.html', response=None)
    if query in ['quit', 'q', 'exit']:
        sys.exit()
    result = chain({"question": query, "chat_history": chat_history})
    chat_history.append((query, result['answer']))
    query = None
    return result['answer']

if __name__ == '__main__':
    app.run(debug=True)
