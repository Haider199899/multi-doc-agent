import requests
from pathlib import Path

from llama_index.core import (
    SimpleDirectoryReader
)

city_docs = {}

def download_data(title : str):
    response = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "extracts",
            # 'exintro': True,
            "explaintext": True,
        },
    ).json()

    page = next(iter(response["query"]["pages"].values()))
    wiki_text = page["extract"]

    data_path = Path("../data/files/")
    if not data_path.exists():
        Path.mkdir(data_path)
    data_path = data_path / f"{title}.txt"
    if(data_path.exists()):
       return data_path
    with open(data_path, "w") as fp:
        fp.write(wiki_text)
    return data_path


def load_data(data_path, wiki_title):
    city_docs[wiki_title] = SimpleDirectoryReader(
        input_files=[data_path]
    ).load_data()
    return city_docs[wiki_title]






    
