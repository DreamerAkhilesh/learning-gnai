from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage

class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

def chatbot(state: State) -> State:
    return {
        "messages": [
            AIMessage(content="Hi! This is a message from chatbot")
        ]
    }


graph_builder.add_node("chatbot", chatbot)


graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
