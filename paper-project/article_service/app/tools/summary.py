from article_service.app.consts import SUMMARY_CHUNK_SIZE, SUMMARY_CHUNK_OVERLAP, LLM_SETTING
from langchain.text_splitter import RecursiveCharacterTextSplitter
import article_service.app.global_variable as global_variable
from article_service.app.prompts import MAP_PROMPT_TEMPLATE, COMBINE_PROMPT_TEMPLATE
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import LLMChain
from langchain.tools import tool

# @tool("논문 전체 요약", return_direct=True)
# def summarize(query: str) -> str:
#     """이 함수는 논문 요약이 필요할 때 사용합니다."""

#     text_splitter = CharacterTextSplitter(chunk_size=SUMMARY_CHUNK_SIZE, chunk_overlap =SUMMARY_CHUNK_OVERLAP)
#     pages = text_splitter.split_text(global_variable.content)

#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=SUMMARY_CHUNK_SIZE, chunk_overlap = 0)
#     split_docs = text_splitter.create_documents(pages)

#     map_prompt = PromptTemplate(template=MAP_PROMPT_TEMPLATE, input_variables=["text"])
#     combine_prompt = PromptTemplate(template=COMBINE_PROMPT_TEMPLATE, input_variables=["text"])

#     print("=====================================", split_docs)

#     summarize_chain = load_summarize_chain(
#         llm = LLM_SETTING,
#         chain_type="map_reduce",
#         verbose=True,
#         map_prompt=map_prompt,
#         combine_prompt=combine_prompt,
#         # token_max=
#     )
#     return summarize_chain.run(split_docs)

async def summarize(content: str) -> str:

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=SUMMARY_CHUNK_SIZE, chunk_overlap = SUMMARY_CHUNK_OVERLAP)
    split_docs = text_splitter.create_documents([content])
    map_prompt = PromptTemplate(template=MAP_PROMPT_TEMPLATE, input_variables=["text"])

    # chunk가 1개인 경우 LLMChain 사용
    if len(split_docs) == 1:
        summarize_chain = LLMChain(prompt=map_prompt, llm=LLM_SETTING)
        input = content
    # chunk가 2개 이상인 경우 Map Reduce Chain 사용
    else :
        combine_prompt = PromptTemplate(template=COMBINE_PROMPT_TEMPLATE, input_variables=["text"])
        summarize_chain = load_summarize_chain(
            llm = LLM_SETTING,
            chain_type="map_reduce",
            verbose=True,
            map_prompt=map_prompt,
            combine_prompt=combine_prompt,
            token_max=15000
        )
        input = split_docs
    return await summarize_chain.arun(input)

async def reject_summarize():
    return "본문이 없는 기사입니다."
