from langchain.text_splitter import RecursiveCharacterTextSplitter

def text_spliter(content: str, chunk_size, chunk_overlap) -> str:

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap = chunk_overlap)
    split_docs = text_splitter.create_documents([content])

    return split_docs