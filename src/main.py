from llama_index.core import VectorStoreIndex
import os
import sys
from pathlib import Path
current_directory = Path(__file__).resolve().parent
sys.path.append(str(current_directory.parent))

from data.load import download_data,load_data

from agents.child_agents import create_child_agents
from agents.parent_agent import create_parent_agent

wiki_titles = [
    "Toronto",
    "Seattle",
    "Chicago",
    "Boston",
    "Houston",
    "Tokyo",
    "Berlin",
    "Lisbon",
    "Paris",
    "London",
    "Atlanta",
    "Munich",
    "Shanghai",
    "Beijing",
    "Copenhagen",
    "Moscow",
    "Cairo",
    "Karachi",
]
# Download and load data
city_docs = {}
is_files_exist = False
files = os.path.abspath("./files")
doc_paths = [os.path.join(files,file) for file in os.listdir(files)]
if len(doc_paths):
    is_files_exist = True
    
# Check does files are already downloaded
if not is_files_exist or len(wiki_titles) != len(doc_paths):
   for title in wiki_titles:
       doc_path = download_data(title)
       city_docs[title] = load_data(doc_path, title)
else:
    for doc_path,title in zip(doc_paths,wiki_titles):
        city_docs[title] = load_data(doc_path, title)


query_engines, child_agents, all_nodes = create_child_agents(wiki_titles, city_docs)
parent_agent  = create_parent_agent(wiki_titles, child_agents)

base_index = VectorStoreIndex(all_nodes)
base_query_engine = base_index.as_query_engine(similarity_top_k=4)

response = parent_agent.query(
    "Tell the demographics of Houston, and then compare that with the"
    " demographics of Chicago"
)
print(response)