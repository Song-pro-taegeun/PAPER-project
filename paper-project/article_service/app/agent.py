from article_service.api.user import UserRequest, UserResponse
from article_service.app.tools.summary import summary
from article_service.app.consts import LLM_SETTING
from langchain.agents import initialize_agent, AgentType
import article_service.app.global_variable as global_variable
from langchain.chains.conversation.memory import ConversationBufferWindowMemory



agent_executor = initialize_agent(
    tools=[summary],
    llm=LLM_SETTING,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=3,
    memory = ConversationBufferWindowMemory(memory_key='chat_history', k=5, return_messages=True),
    input_variables=["input", "chat_history", "agent_scratchpad"],
    # agent_kwargs={},
)

def run_langchain(chat: str, article: str) -> str:
    # if user_request.content is None:
    #     user_request.content = "empty"
    global_variable.change_content(article)
    llm_response = agent_executor.run(chat)

    return llm_response