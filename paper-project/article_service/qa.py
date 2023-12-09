from article_service.consts import LLM_SETTING
from article_service.prompts import QA_PROMPT_TEMPLATE
from article_service.vector_store import get_vector_store
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

def qa(query:str) -> str:
    chroma_vector_store = get_vector_store()
    qa_prompt = PromptTemplate(template= QA_PROMPT_TEMPLATE, input_variables=["question","context"])
    retriever = chroma_vector_store.as_retriever(search_type='similarity', search_kwargs={'k':1})
    chain_type_kwargs={"prompt" : qa_prompt}
    qa_chain = RetrievalQA.from_chain_type(llm=LLM_SETTING,
                                           chain_type="stuff",
                                           retriever=retriever,
                                           chain_type_kwargs=chain_type_kwargs)
    
    return qa_chain.run(query)