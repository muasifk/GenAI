

# conda activate llm-env
# conda create -n llm-env
# pip install google-genai
# pip install python-dotenv
# pip install PyMuPDF                  # pdf parser
# pip install faiss-cpu                # Meta's library for similarity search and clustering of dense vectors
# pip install sentence-transformers    # Python framework for sentence, text and image embeddings

#### PDF extraction libs:
# PyPDF2: text, limited image (no table)
# PyMuPDF: strong text, strong images, custom (not built in) table 
# PDFMiner: text, no image and table (complex to use)
# Tabula-py: tables, limited text (no image)
# Camelot: text, tables (cumbersome)




from dotenv import load_dotenv
import os
import numpy as np
from google import genai
from google.genai import types
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import faiss
load_dotenv('keys.env')  # Load environment variables from .env file
api_key = os.getenv('GOOGLE_API_KEY')



DATA_DIR = "data"
EMBED_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
client = genai.Client(api_key=api_key)




def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    # print(f"Reading {len(doc)} pages from {pdf_path}")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def load_documents(data_dir):
    return "\n".join(
        extract_text_from_pdf(os.path.join(data_dir, f))
        for f in os.listdir(data_dir)
        if f.endswith(".pdf"))


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i+chunk_size])
    # print('\n A sample chunk \n', chunks[0],'\n')
    return chunks


def embed_chunks(chunks):
    embeddings = EMBED_MODEL.encode(chunks)
    # print('Show embeddings \n', embeddings[0], '\n')
    return np.array(embeddings)


def build_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    # print('Show Index \n', index, '\n')
    return index

def retrieve_chunks(query, chunks, index, embedding_model, top_k=3):
    '''
    Retrieve Relevant Chunks for a Query
    '''
    query_vec = embedding_model.encode([query])
    distances, indices = index.search(np.array(query_vec), top_k)
    return [chunks[i] for i in indices[0]]


def generate_response(query, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks)
    prompt = f"""You are an assistant that answers questions based on the user's documents.
    Context:{context}
    Question: {query}
    Answer:"""
    response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
            # system_instruction='you are a story teller for kids under 5 years old',
            max_output_tokens= 300,
            # top_k= 2,
            # top_p= 0.5,
            temperature= 0.5,
            #   response_mime_type= 'application/json',
            stop_sequences= ['\n'],
            seed=42,
            safety_settings= [types.SafetySetting(
                    category='HARM_CATEGORY_HATE_SPEECH',
                    threshold='BLOCK_ONLY_HIGH'),]
            ),)
    return response.text


### My RAG bot here
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    # ---------- Preprocess Once ----------
    raw_text   = load_documents(DATA_DIR)
    chunks     = chunk_text(raw_text)
    embeddings = embed_chunks(chunks)
    index      = build_index(embeddings)
    
    print("RAG chatbot ready. Ask your questions (type 'exit' to quit):")
    while True:
        print()
        prompt = input("You > ")
        if prompt.lower() == "exit":
            break
        context_chunks = retrieve_chunks(prompt, chunks, index, EMBED_MODEL)
        answer = generate_response(prompt, context_chunks)
        print("\nAnswer:", answer)