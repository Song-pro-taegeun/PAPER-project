from article_service.consts import SUMMARY_CHUNK_SIZE, SUMMARY_CHUNK_OVERLAP, LLM_SETTING
from article_service.prompts import MAP_PROMPT_TEMPLATE, COMBINE_PROMPT_TEMPLATE
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import LLMChain
from article_service.spliter import text_spliter


async def summarize(content: str) -> str:

    split_docs = text_spliter(content, SUMMARY_CHUNK_SIZE, SUMMARY_CHUNK_OVERLAP)
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
