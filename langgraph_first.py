from typing import TypedDict
from langgraph.graph import StateGraph,END,START


# Define state  Schema
class State(TypedDict):
    question:str
    category:list
    answer:str


#Define Nodes

def classify_question(state:State):

   question=state['question']

   if len(question.split())<=5:
    category='simple'
   else:
     category="detailed"

   return {"category":category}

def simple_answer(state:State):
    question=state["question"]
    return{
        "answer":f"simiple answer to question: {question} in 2 lines"
    }

def detailed_answer(state:State):
    question=state["question"]
    return{
        "answer":f"detailed answer to question: {question} in 2 lines"
    }
def route_question(state: State):

    if state["category"] == "simple":
        return "simple"

    return "detailed"

#initialize StateGraph

builder=StateGraph(State)

builder.add_node("classify", classify_question)
builder.add_node("simple", simple_answer)
builder.add_node("detailed", detailed_answer)
# builder.add_node("routing",route_question)

builder.add_edge(START,"classify")
builder.add_conditional_edges(
    "classify",
     route_question,
    {
        "simple":"simple",
        "detailed":"detailed",
    }
)
builder.add_edge("simple",END)
builder.add_edge("detailed",END)

graph=builder.compile()

result=graph.invoke({
    "question":"what is LangGraph and why we use it?",
    "category":"",
    "answer":""
})

print(result)