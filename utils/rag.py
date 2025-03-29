import os
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import AzureOpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed

class RAG:
    def __init__(self):
        self.client = AzureOpenAI(
            azure_endpoint = os.getenv("AZURE_OPENAI_API_ENDPOINT"),
            api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
            api_version = os.getenv("AZURE_OPENAI_API_VERSION"),
        )
        self.embedding_model = 'gpt-4o'

    # RAG main function
    def generate_context(self, content, query, k=10, chunk_size = 512 , chunk_overlap = 256):
        chunks = self.split_text(content, chunk_size, chunk_overlap)
        most_similar_chunks = self.find_most_similar_chunks(query, chunks, k)
        context = "\n".join(most_similar_chunks)
        return context

    # RAG Helper functions
    def split_text(self, content, chunk_size=512, chunk_overlap=256):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_text(content)
        return chunks

    def embed_texts(self, texts):
        def embed_query(text):
            text = text.replace("\n", " ")
            print(self.client.chat.completions.create(
                model="text-embedding-ada-002",
                messages=[
                    {"role": "system", 'content': ''},
                    {"role": "user", "content": text}
                ],
            ))
            print(self.client.embeddings.create(input=[text], model='gpt-4o', encoding_format='float'))
            embedding = self.client.embeddings.create(input = [text], model=self.embedding_model).data[0].embedding
            print(embedding)    
            return embedding

        embeddings = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(embed_query, text): text for text in texts}
            for future in as_completed(futures):
                print(future.result())
                input()
                embeddings.append(future.result())
        
        return np.array(embeddings)

    def find_most_similar_chunks(self, query, chunks, k=10):
        query_embedding = self.embed_texts([query])[0]
        chunk_embeddings = self.embed_texts(chunks)

        similarities = self.calculate_cosine_similarity(query_embedding, chunk_embeddings)

        top_k_indices = similarities.argsort()[-k:][::-1]
        most_similar_chunks = [chunks[i] for i in top_k_indices]
        return most_similar_chunks
    
    def calculate_cosine_similarity(self, embedding, embeddings):
        dot_product = np.dot(embeddings, embedding)
        norm_embedding = np.linalg.norm(embedding)
        norms_embeddings = np.linalg.norm(embeddings, axis=1)
        similarities = dot_product / (norms_embeddings * norm_embedding)
        return similarities
    
    def cosine_similarity(self, vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    