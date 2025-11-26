# func_Kotler_RAG.py
# This file contains the logic for the Retrieval-Augmented Generation tool.

import os
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

# --- Placeholder Knowledge Base ---
# In a real application, this would be loaded from a file or database,
# e.g., the contents of Philip Kotler's "Marketing Management".
KOTLER_KB_TEXT = """
Marketing strategy is the fundamental goal of increasing sales and achieving a sustainable competitive advantage.
Marketing strategy includes 'all basic and long-term activities in the field of marketing that deal with the analysis
of the strategic initial situation of a company and the formulation, evaluation and selection of market-oriented strategies
and therefore contribute to the goals of the company and its marketing objectives.'

The 4Ps of marketing are Product, Price, Place, and Promotion. These are the key pillars of a marketing mix.
Product refers to the item or service being sold. Price refers to the amount a customer pays.
Place refers to the location where a product can be purchased. Promotion refers to all the activities
undertaken to make the product or service known to the user and trade.

Market segmentation is the process of dividing a broad consumer or business market, normally consisting of existing
and potential customers, into sub-groups of consumers (known as segments) based on some type of shared characteristics.
The most common criteria for segmentation include demographic, geographic, psychographic, and behavioral variables.
"""

# --- RAG Tool Initialization ---

# Define the path for the FAISS index
FAISS_INDEX_PATH = "kotler_index.faiss"

def get_rag_retriever():
    """
    Initializes the RAG retriever. If the FAISS index doesn't exist, it creates one.
    Returns a FAISS retriever object.
    """
    if not os.path.exists(FAISS_INDEX_PATH):
        print("FAISS index not found. Creating a new one...")
        # Split the text into manageable chunks
        text_splitter = CharacterTextSplitter(
            separator="\\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        texts = text_splitter.split_text(KOTLER_KB_TEXT)

        # Use a standard sentence-transformer model for embeddings
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        # Create the FAISS vector store and save it locally
        vectorstore = FAISS.from_texts(texts, embeddings)
        vectorstore.save_local(FAISS_INDEX_PATH)
        print(f"FAISS index created and saved to {FAISS_INDEX_PATH}")
    else:
        print(f"Loading existing FAISS index from {FAISS_INDEX_PATH}")
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

    return vectorstore.as_retriever()

def query_rag(question):
    """
    Performs a query against the RAG knowledge base.

    Args:
        question (str): The question to ask the RAG tool.

    Returns:
        str: The most relevant document snippet from the knowledge base.
    """
    try:
        retriever = get_rag_retriever()
        # The new standard way to run retrievers is with the `invoke` method.
        docs = retriever.invoke(question)

        if docs:
            # For simplicity, return the content of the most relevant document
            return docs[0].page_content
        else:
            return "No relevant information found in the knowledge base."
    except Exception as e:
        return f"An error occurred during the RAG query: {e}"

# --- Example Usage ---
if __name__ == '__main__':
    print("Initializing RAG tool for a test query...")
    # This will create the index on the first run
    test_question = "What are the 4Ps of marketing?"
    answer = query_rag(test_question)

    print(f"\\n--- Test Query ---")
    print(f"Question: {test_question}")
    print(f"Answer: {answer}")

    # Second query to test loading the existing index
    test_question_2 = "What is market segmentation?"
    answer_2 = query_rag(test_question_2)
    print(f"\\n--- Second Test Query ---")
    print(f"Question: {test_question_2}")
    print(f"Answer: {answer_2}")
