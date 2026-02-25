# langraph has three major components : node, edges and state
# first lets create a state

from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph

class State(TypedDict):
    messages : Annotated[list, add_messages]


graph_builder = StateGraph(State) 

def chatbot (state : State) :
    return {"message" : ["Hi! This is a message from chatbot"]} 
    # will take the previous state
    # will get appended the messages to the previous state

graph_builder.add_node("Chat-bot", chatbot)