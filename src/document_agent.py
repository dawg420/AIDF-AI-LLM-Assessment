# src/document_agent.py
import PyPDF2
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

class DocumentAgent:
    def __init__(self, llm, prompt_template):
        self.llm = llm
        self.prompt_template = prompt_template

    def read_pdf(self, pdf_path):
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def retrieve_information(self, document):
        # Split the document into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_text(document)
        
        # Convert splits to Document objects
        documents = [Document(page_content=split) for split in splits]
        
        # Initialize Chroma vector store
        vectorstore = Chroma.from_documents(documents=documents, embedding=OpenAIEmbeddings())
        
        # Retrieve relevant snippets
        retriever = vectorstore.as_retriever()
        retrieved_docs = retriever.get_relevant_documents(document)
        formatted_docs = self.format_docs(retrieved_docs)
        
        combined_document = document + "\n\nRetrieved Information:\n" + formatted_docs
        prompt = self.prompt_template.format(document=combined_document)
        
        # Generate response using the combined document
        response = self.llm.invoke(prompt, max_tokens=4096, stop=None)
        print(f'Generated response:\n {response.content}')
        return response.content

    def extract_nodes_and_edges(self, document):
        response = self.retrieve_information(document)
        try:
            response_json = json.loads(response)
            nodes = response_json.get("nodes", [])
            edges = response_json.get("edges", [])
            
            # Validate nodes
            node_names = {node['properties']['name'] for node in nodes}
            
            # Filter out invalid edges
            valid_edges = [
                edge for edge in edges
                if edge['node1'] in node_names and edge['node2'] in node_names
            ]
            
            return nodes, valid_edges
        except json.JSONDecodeError as e:
            print("Error decoding JSON response:", e)
            print("Raw response:", response)
            return [], []
