from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain.schema import Document
from typing import List, Any
from pydantic import Field

class HierarchicalCategoryRetriever(BaseRetriever):
    vector_store: Any = Field(description="Vector store for document retrieval")

    class Config:
        arbitrary_types_allowed = True

    def get_relevant_documents(self, query: str) -> List[Document]:
        # Initial retrieval based on the query
        docs = self.vector_store.similarity_search(query, k=5)
        
        # Extract all unique categories from the retrieved documents
        categories = set()
        for doc in docs:
            categories.update(doc.metadata.get('categories', '').split(' > '))
        
        # Retrieve additional documents for each category and its parents
        additional_docs = []
        for category in categories:
            category_docs = self.vector_store.similarity_search(f"Section: {category}", k=3)
            additional_docs.extend(category_docs)
        
        # Combine and remove duplicates
        all_docs = docs + additional_docs
        unique_docs = list({doc.page_content: doc for doc in all_docs}.values())
        
        # Sort documents by relevance (assuming more specific categories are more relevant)
        sorted_docs = sorted(unique_docs, key=lambda x: len(x.metadata['categories'].split(' > ')), reverse=True)
        
        return sorted_docs[:10]  # Return top 10 most relevant documents

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        return self.get_relevant_documents(query)

def create_qa_chain(vector_store):
    # Temperature 0 for more accurate answers
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    
    custom_retriever = HierarchicalCategoryRetriever(vector_store=vector_store)
    
    template = """You are an AI assistant answering questions about a food consumption report.
    Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    
    When answering questions about categories, consider all subcategories as part of that category.
    For example, if asked about "drinks" or "beverages", consider information about all types of drinks like "juice" and "water".
    Similarly, if asked about "food", consider information about all types of food like "pizza" and "tomato soup".
    
    When asked about quantities or amounts for a higher-level category, sum up the values from all subcategories.
    For example, if asked "How many drinks were consumed?", add up the consumption of all types of drinks.
    
    Always show your reasoning and calculations when deriving information from subcategories.
    
    {context}
    
    Question: {question}
    Detailed answer:"""
    
    qa_prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=custom_retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": qa_prompt}
    )
    return qa_chain

def answer_question(qa_chain, question):
    result = qa_chain.invoke({"query": question})
    return result["result"], result["source_documents"]


# Usage
# qa_chain = create_qa_chain(vector_store)
# answer, sources = answer_question(qa_chain, "How many pizzas did Andy buy in 2022?")