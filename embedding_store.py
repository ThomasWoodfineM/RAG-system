import os
import pandas as pd
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

os.environ["GOOGLE_API_KEY"] = open("gemini_api_key.txt", "r").read()

def create_vector_store(structured_data):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    texts = []
    metadatas = []

    def process_section(section):
        section_path = ' > '.join(section['categories'])
        
        for item in section['content']:
            if isinstance(item, str):
                text = f"Section: {section_path}\nContent: {item}"
                texts.append(text)
                metadatas.append({
                    "source": "markdown",
                    "section": section['title'],
                    "level": section['level'],
                    "type": "text",
                    "categories": section_path
                })
            elif isinstance(item, pd.DataFrame):
                table_text = f"Section: {section_path}\nTable:\n{item.to_string(index=False)}"
                texts.append(table_text)
                metadatas.append({
                    "source": "markdown",
                    "section": section['title'],
                    "level": section['level'],
                    "type": "table",
                    "categories": section_path
                })

        for subsection in section['subsections']:
            process_section(subsection)

    process_section(structured_data)

    vector_store = Chroma.from_texts(texts, embeddings, metadatas=metadatas)
    return vector_store


def print_vector_store(vector_store):
    ids = vector_store.get()['ids']
    
    print("Vector Store Contents:")
    print("----------------------")
    
    for id in ids:
        results = vector_store.get([id])
        
        print(f"ID: {id}")
        print(f"Text: {results['documents'][0]}")
        print(f"Metadata: {results['metadatas'][0]}")
        print("----------------------")
