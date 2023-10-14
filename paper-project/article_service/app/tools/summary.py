from article_service.app.consts import SUMMARY_CHUNK_SIZE, SUMMARY_CHUNK_OVERLAP, LLM_SETTING
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
import article_service.app.global_variable as global_variable
from article_service.app.prompts import MAP_PROMPT_TEMPLATE, COMBINE_PROMPT_TEMPLATE
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.tools import tool

@tool("논문 전체 요약", return_direct=True)
def summary(query: str) -> str:
    """이 함수는 논문 요약이 필요할 때 사용합니다."""

    text_splitter = CharacterTextSplitter(chunk_size=SUMMARY_CHUNK_SIZE, chunk_overlap =SUMMARY_CHUNK_OVERLAP)
    pages = text_splitter.split_text(global_variable.content)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=SUMMARY_CHUNK_SIZE, chunk_overlap = 0)
    split_docs = text_splitter.create_documents(pages)

    map_prompt = PromptTemplate(template=MAP_PROMPT_TEMPLATE, input_variables=["text"])
    combine_prompt = PromptTemplate(template=COMBINE_PROMPT_TEMPLATE, input_variables=["text"])

    print("=====================================", split_docs)

    summarize_chain = load_summarize_chain(
        llm = LLM_SETTING,
        chain_type="map_reduce",
        verbose=True,
        map_prompt=map_prompt,
        combine_prompt=combine_prompt,
        # token_max=
    )
    return summarize_chain.run(split_docs)

