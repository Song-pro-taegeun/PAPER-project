from langchain.chat_models import ChatOpenAI

# OPENAI_API_KEY = "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"
OPENAI_API_KEY = "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"
TEMPERATURE = 0
LLM_NAME = "gpt-3.5-turbo-16k"

SUMMARY_CHUNK_SIZE = 15000
SUMMARY_CHUNK_OVERLAP = 1500

LLM_SETTING=ChatOpenAI(
        openai_api_key = OPENAI_API_KEY,
        temperature = TEMPERATURE,
        model_name = LLM_NAME
    )