import os
from llama_index.core import (
    VectorStoreIndex,
)
from llama_index.agent.openai import OpenAIAgent
from llama_index.core import load_index_from_storage, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from config.env import OPENAI_API_KEY
from llama_index.core import SummaryIndex
from llama_index.core.tools import QueryEngineTool, ToolMetadata

Settings.llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")

node_parser = SentenceSplitter()

# Build agents dictionary
child_agents = {}
query_engines = {}

# this is for the baseline
all_nodes = []

def create_each_doc_agent(wiki_title, doc) -> None:
    nodes = node_parser.get_nodes_from_documents(doc)
    all_nodes.extend(nodes)

    if not os.path.exists(f"../data/{wiki_title}"):
        # build vector index
        vector_index = VectorStoreIndex(nodes)
        vector_index.storage_context.persist(
            persist_dir=f"../data/{wiki_title}"
        )
    else:
        vector_index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=f"../data/{wiki_title}"),
        )
    # build summary index
    summary_index = SummaryIndex(nodes)
    # define query engines
    vector_query_engine = vector_index.as_query_engine(llm=Settings.llm)
    summary_query_engine = summary_index.as_query_engine(llm=Settings.llm)

    # define tools
    query_engine_tools = [
        QueryEngineTool(
            query_engine=vector_query_engine,
            metadata=ToolMetadata(
                name="vector_tool",
                description=(
                    "Useful for questions related to specific aspects of"
                    f" {wiki_title} (e.g. the history, arts and culture,"
                    " sports, demographics, or more)."
                ),
            ),
        ),
        QueryEngineTool(
            query_engine=summary_query_engine,
            metadata=ToolMetadata(
                name="summary_tool",
                description=(
                    "Useful for any requests that require a holistic summary"
                    f" of EVERYTHING about {wiki_title}. For questions about"
                    " more specific sections, please use the vector_tool."
                ),
            ),
        ),
    ]

    # build agent
    function_llm = OpenAI(model="gpt-4")
    agent = OpenAIAgent.from_tools(
        query_engine_tools,
        llm=function_llm,
        verbose=True,
        system_prompt=f"""\
         You are a specialized agent designed to answer queries about {wiki_title}.
         You must ALWAYS use at least one of the tools provided when answering a question; do NOT rely on prior knowledge.\
           """,
        )

    child_agents[wiki_title] = agent
    query_engines[wiki_title] = vector_index.as_query_engine(
        similarity_top_k=2
    )

def create_child_agents(wiki_titles,city_docs):
    for wiki_title in wiki_titles:
        create_each_doc_agent(wiki_title, city_docs[wiki_title])
    return query_engines, child_agents, all_nodes
