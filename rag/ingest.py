from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
import os
HR_DOCS_FOLDER= "hr_policies"
CHROMA_DB_PATH="chroma_db"

def load_documents():
    docs=[]
    for filename in os.listdir(HR_DOCS_FOLDER):
        filepath=os.path.join(HR_DOCS_FOLDER, filename)
        if filename.endswith(".pdf"):
            loader=PyPDFLoader(filepath)
            docs.extend(loader.load())
        elif filename.endswith(".docx"):
            loader=Docx2txtLoader(filepath)
            docs.extend(loader.load())

    return docs

def ingest_documents():
    docs=load_documents()
    if not docs:
        raise ValueError("No documents found in hr_policies folder")
    splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    chunks=splitter.split_documents(docs)
    embeddings=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore=Chroma.from_documents(documents=chunks,embedding=embeddings,persist_directory=CHROMA_DB_PATH)
    return len(chunks)


def get_vectorstore():
    embeddings=SentenceTransformerEmbeddings(model_name="all-MiniLm-l6-V2")
    return Chroma(persist_directory=CHROMA_DB_PATH,embedding_function=embeddings)
