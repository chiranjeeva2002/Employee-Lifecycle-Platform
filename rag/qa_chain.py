from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from rag.ingest import get_vectorstore

HR_PROMPT = PromptTemplate(input_variables=["context","question"],template="""You are an HR assistant for our company.
Answer the employee's question ONLY based on the HR policy documents provided below.
If the answer is not in the documents, say "I don't have information about that in our HR policies."
Be clear, professional, and concise.
HR Policy Context:{context}
Employee Question:{question}                           
Answer:""")


def get_qa_chain():
    llm=Ollama(model="phi3")
    vectorstore=get_vectorstore()
    retriever=vectorstore.as_retriever(search_kwargs={"k":3})
    
    # Build the chain using LCEL (LangChain Expression Language)
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    qa_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | HR_PROMPT
        | llm
        | StrOutputParser()
    )
    
    return qa_chain, retriever

def ask_hr_question(question: str) ->dict:
    chain, retriever=get_qa_chain()
    answer=chain.invoke(question)
    
    # Get source documents
    source_docs = retriever.invoke(question)
    
    return {
        "question": question,
        "answer": answer,
        "sources": [
            doc.metadata.get("source","unknown")
            for doc in source_docs
        ]
    }