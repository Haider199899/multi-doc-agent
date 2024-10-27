from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core import VectorStoreIndex
from llama_index.core.objects import ObjectIndex
from llama_index.agent.openai import OpenAIAgent

# define tool for each document agent
all_tools = []

def create_parent_agent(wiki_titles,agents):
    for wiki_title in wiki_titles:
        wiki_summary = (
        f"This content contains Wikipedia articles about {wiki_title}. Use"
        f" this tool if you want to answer any questions about {wiki_title}.\n"
        )
        doc_tool = QueryEngineTool(
            query_engine=agents[wiki_title],
            metadata=ToolMetadata(
               name=f"tool_{wiki_title}",
               description=wiki_summary,
            ),
        )
        all_tools.append(doc_tool)
    
    obj_index = ObjectIndex.from_objects(
    all_tools,
    index_cls=VectorStoreIndex,
    )
    top_agent = OpenAIAgent.from_tools(
    tool_retriever=obj_index.as_retriever(similarity_top_k=3),
    system_prompt=""" \
                  You are an agent designed to answer queries about a set of given cities.
                    Please always use the tools provided to answer a question. Do not rely on prior knowledge.\

                """,
    verbose=True,
    )
    return top_agent