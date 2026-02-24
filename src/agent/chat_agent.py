from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langsmith import traceable
from rag.generation_model import llm_client
from agent.tools import query_knowledge_base
from prompts.agent_prompt import AGENT_SYSTEM_PROMPT

@traceable(name="get_conversational_agent")
def get_conversational_agent() -> AgentExecutor:
    tools = [query_knowledge_base]
    prompt = ChatPromptTemplate.from_messages([
        ("system", AGENT_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    agent = create_tool_calling_agent(llm_client, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor = get_conversational_agent()
