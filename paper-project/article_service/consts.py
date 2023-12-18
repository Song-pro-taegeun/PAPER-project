from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings

OPENAI_API_KEY = "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"
TEMPERATURE = 0
LLM_NAME = "gpt-3.5-turbo-16k"

LLM_SETTING=ChatOpenAI(
        openai_api_key = OPENAI_API_KEY,
        temperature = TEMPERATURE,
        model_name = LLM_NAME
    )

EMBEDDINGS = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

SUMMARY_CHUNK_SIZE = 15000
SUMMARY_CHUNK_OVERLAP = 1500
QA_CHUNK_SIZE = 5000
QA_CHUNK_OVERLAP = 500

