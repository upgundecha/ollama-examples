import ollama
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever

pdf_doc_path = "./data/AI_Agent_Basics.pdf"
model = "llama3.2"

if pdf_doc_path:
    loader = UnstructuredPDFLoader(file_path = pdf_doc_path)
    data = loader.load()
    print("Loaded data from PDF file.")
else:
    print("No PDF file path provided.")

content = data[0].page_content
print("Content loaded from PDF:", content[0:100])

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
chunks = text_splitter.split_documents(data) 
print("Text chunks created.")

# print("Number of chunks:", len(chunks))
# print("First chunk:", chunks[0])

ollama.pull("nomic-embed-text")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
    collection_name="ollama-rag",
)

llm = ChatOllama(model=model)

QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""
        You are an AI assistant. Your task is to generate five
        different versions of the given user question to retrieve relevant documents from
        a vector database. By generating multiple perspectives on the user question, your
        goal is to help the user overcome some of the limitations of the distance-based
        similarity search. Provide these alternative questions separated by newlines.
        Original question: {question} 
        """,
)

retriever = MultiQueryRetriever.from_llm(
    vectorstore.as_retriever(), llm, prompt=QUERY_PROMPT
)

prompt_template = """Answer the question based ONLY on the following context:
{context}
Question: {question}
"""
prompt = ChatPromptTemplate.from_template(prompt_template)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

response = chain.invoke(input=("What is the main topic of the document?"))
print("Response from the chain:", response)

response = chain.invoke(input=("What is VertexAI agents?"))
print("Response from the chain:", response)


# ollama.delete("nomic-embed-text")


