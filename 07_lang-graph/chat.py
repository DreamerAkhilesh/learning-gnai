from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage


# 1️⃣ Define State
class State(TypedDict):
    messages: Annotated[list, add_messages]


# 2️⃣ Initialize Graph
graph_builder = StateGraph(State)


# 3️⃣ Node 1 — Chatbot
def chatbot(state: State) -> State:
    last_message = state["messages"][-1].content

    return {
        "messages": [
            AIMessage(content=f"Chatbot says: You said '{last_message}'")
        ]
    }


# 4️⃣ Node 2 — Sentiment Analyzer
def sentiment_analyzer(state: State) -> State:
    last_user_message = state["messages"][0].content.lower()

    if "happy" in last_user_message:
        sentiment = "Positive 😊"
    elif "sad" in last_user_message:
        sentiment = "Negative 😢"
    else:
        sentiment = "Neutral 😐"

    return {
        "messages": [
            AIMessage(content=f"Sentiment detected: {sentiment}")
        ]
    }


# 5️⃣ Add Nodes
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sentiment", sentiment_analyzer)


# 6️⃣ Add Edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "sentiment")
graph_builder.add_edge("sentiment", END)


# 7️⃣ Compile Graph
graph = graph_builder.compile()


# 8️⃣ Run Graph
initial_state = {
    "messages": [HumanMessage(content="I am very happy today!")]
}

result = graph.invoke(initial_state)

for msg in result["messages"]:
    print(msg.content)