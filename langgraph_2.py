from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send


# ==========================================
# 1. Custom Reducer
# ==========================================

def merge_documents(existing, new):
    return existing + new


# ==========================================
# 2. Main State Schema
# ==========================================

class Document(TypedDict):
    id: int
    content: str


class Metadata(TypedDict):
    user_id: str
    source: str


class State(TypedDict):
    question: str
    documents: list[Document]

    processed_documents: Annotated[
        list[str],
        merge_documents
    ]

    answer: str

    metadata: Metadata


# ==========================================
# 3. Document Subgraph State
# ==========================================

class DocumentState(TypedDict):
    document: str
    cleaned: str
    summary: str


# ==========================================
# 4. Subgraph Nodes
# ==========================================

def clean_document(state: DocumentState):

    return {
        "cleaned": state["document"].strip()
    }


def summarize_document(state: DocumentState):

    return {
        "summary": f"Summary: {state['cleaned']}"
    }


# ==========================================
# 5. Build Document Subgraph
# ==========================================

document_builder = StateGraph(DocumentState)

document_builder.add_node(
    "clean",
    clean_document
)

document_builder.add_node(
    "summarize",
    summarize_document
)

document_builder.add_edge(
    START,
    "clean"
)

document_builder.add_edge(
    "clean",
    "summarize"
)

document_builder.add_edge(
    "summarize",
    END
)

document_graph = document_builder.compile()


# ==========================================
# 6. Parallel Processing
# ==========================================

def process_documents(state: State):

    return [
        Send(
            "process_document",
            {
                "document": document["content"]
            }
        )
        for document in state["documents"]
    ]


# ==========================================
# 7. Process Individual Document
# ==========================================

def process_document(state):

    result = document_graph.invoke({
        "document": state["document"],
        "cleaned": "",
        "summary": ""
    })

    return {
        "processed_documents": [
            result["summary"]
        ]
    }


# ==========================================
# 8. Generate Final Answer
# ==========================================

def generate_answer(state: State):

    documents = state["processed_documents"]

    return {
        "answer": (
            f"Processed {len(documents)} documents.\n"
            f"Results: {documents}"
        )
    }


# ==========================================
# 9. Build Main Graph
# ==========================================

builder = StateGraph(State)

builder.add_node(
    "process_documents",
    process_documents
)

builder.add_node(
    "process_document",
    process_document
)

builder.add_node(
    "generate",
    generate_answer
)


# ==========================================
# 10. Edges
# ==========================================

builder.add_edge(
    START,
    "process_documents"
)

builder.add_conditional_edges( "process_documents", process_documents)

builder.add_edge(
    "process_document",
    "generate"
)

builder.add_edge(
    "generate",
    END
)


# ==========================================
# 11. Compile
# ==========================================

graph = builder.compile()