from data_processor import parse_and_process_markdown, print_parsed_markdown
from embedding_store import create_vector_store, print_vector_store
from rag_system import create_qa_chain, answer_question

def main():
    print("Loading and processing data...")
    data = parse_and_process_markdown('report-2.md')

    # print_parsed_markdown(processed_data)
    
    print("Creating vector store...")
    vector_store = create_vector_store(data)

    # print_vector_store(vector_store)
    
    print("Initializing QA system...")
    qa_chain = create_qa_chain(vector_store)
    
    while True:
        question = input("\nEnter your question (or 'q' to exit): ")
        if question.lower() == 'q':
            break
        if not question:
            print("Please enter a valid question.")
            continue
        
        print("\n\nProcessing...")
        answer, sources = answer_question(qa_chain, question)
        
        print("\n\nSources:")
        for i, doc in enumerate(sources, 1):
            print(f"{i}. {doc.page_content}...")
        
        print("\n\nFinal Prompt:")
        print(qa_chain.combine_documents_chain.llm_chain.prompt.format(
            context="\n".join([doc.page_content for doc in sources]),
            question=question
        ))
        print(f"\n\nAnswer: {answer}")

if __name__ == "__main__":
    main()