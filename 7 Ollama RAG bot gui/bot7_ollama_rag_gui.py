import os
import requests
import json
from pathlib import Path
import PyPDF2
model_name = 'qwen3:0.6b' # https://qwenlm.github.io/blog/qwen3/
# model_name = 'deepseek-r1:1.5b', 
# model_name = 'llama3.2:1b', 

class SimpleRAG:
    def __init__(self, ollama_url="http://localhost:11434", model=model_name): # deepseek-r1, llama3
        self.ollama_url = ollama_url
        self.model = model
        self.documents = []
        self.load_documents()
    
    def load_documents(self):
        """Load all PDF files from data folder"""
        data_folder = Path("../2 RAG bot/data")
        if not data_folder.exists():
            print("Creating data folder...")
            data_folder.mkdir()
            return
        
        for file_path in data_folder.glob("*.pdf"):
            try:
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    content = ""
                    for page in pdf_reader.pages:
                        content += page.extract_text() + "\n"
                    
                    self.documents.append({
                        'name': file_path.name,
                        'content': content
                    })
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        
        print(f"Loaded {len(self.documents)} documents")
    
    def find_relevant(self, question, top_k=2):
        """Simple keyword-based document retrieval"""
        keywords = question.lower().split()
        scored_docs = []
        
        for doc in self.documents:
            score = sum(1 for word in keywords if word in doc['content'].lower())
            if score > 0:
                scored_docs.append((doc, score))
        
        # Sort by score and return top_k
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in scored_docs[:top_k]]
    




    #############  Chat with Ollama #############
    def generate_response(self, prompt):
        """Generate response using Ollama"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                ### See model config options: ollama show <model name>
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "top_k": 20,
                        "top_p": 0.9,
                        "thinking": False,
                        # "num_predict": 200 # output CTX window (ollama)
                    },
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()['response']
            else:
                return f"Error: {response.status_code}"
                
        except Exception as e:
            return f"Error connecting to Ollama: {e}"
    
    def chat(self, question):
        """Main chat function"""
        if not self.documents:
            return "No documents loaded. Add .pdf files to the 'data' folder."
        
        # Find relevant documents
        relevant_docs = self.find_relevant(question)
        
        if not relevant_docs:
            return "No relevant documents found for your question."
        
        # Build context
        context = "\n\n".join([doc['content'] for doc in relevant_docs])
        sources = [doc['name'] for doc in relevant_docs]
        
        # Create prompt
        prompt = f"""Context from documents:
{context}

Question: {question}

Answer user questions in few words based on the context above.:"""
        
        # Generate response
        response = self.generate_response(prompt)
        
        return f"{response}\n\nSources: {', '.join(sources)}"

def main():
    # Initialize RAG system
    rag = SimpleRAG()
    
    print("Simple RAG Chat (type 'quit' to exit)")
    print("-" * 40)
    
    while True:
        question = input("\nYou: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            break
        
        if not question:
            continue
        
        print("Assistant:", rag.chat(question + '/no_think'))

if __name__ == "__main__":
    main()