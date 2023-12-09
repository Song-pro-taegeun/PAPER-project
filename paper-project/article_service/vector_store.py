from langchain.vectorstores import Chroma
from article_service.consts import EMBEDDINGS, QA_CHUNK_OVERLAP, QA_CHUNK_SIZE
from article_service.spliter import text_spliter

chroma_vector_store = Chroma(embedding_function=EMBEDDINGS)

def init_chroma_vector_store():
    global chroma_vector_store
    chroma_vector_store = Chroma(embedding_function=EMBEDDINGS)

async def insert_vector_store(content: str):
    split_docs = text_spliter(content,QA_CHUNK_SIZE,QA_CHUNK_OVERLAP)
    chroma_vector_store.add_documents(split_docs)
    
def get_vector_store():
    return chroma_vector_store