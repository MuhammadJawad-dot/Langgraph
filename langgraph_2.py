from tenacity import stop
from typing import TypedDict,Annotated
class DocumentState(TypedDict):
    document:str
    cleaned:str
    summary:str
def clean_document(state:DocumentState):
    return{
        "cleaned":state["document"].strip()
    }
def summarize_document(state:DocumentState):
    return{
        "summary":f"{state['cleaned']} is summarized in 50 words"
    }
class Document(TypedDict):
  id:int
  content:str

class Metadata(TypedDict):
    user_id:str
    source:str

def merge_documents(existing,new):
    return existing + new

class State(TypedDict):
    question:str
    documents:list[Document]
    processed_documents:Annotated[list[str],merge_documents]
    answer:str
    errors:list[str]
    metadata:Metadata
   