import json
from pathlib import Path

import fire
from bs4 import BeautifulSoup
from tqdm import tqdm

from smart.settings import DATAPATH, HTMLPATH

test_file = HTMLPATH / "03-conditional.html"


def next_element(elem):
    while elem is not None:
        # Find next element, skip NavigableString objects
        elem = elem.next_sibling
        if hasattr(elem, "name"):
            return elem


def get_pages_by_h2(h2tags):
    pages = []
    for h2tag in h2tags:
        page = [str(h2tag)]
        elem = next_element(h2tag)
        while elem and elem.name != "h2":
            page.append(str(elem))
            elem = next_element(elem)
        pages.append("\n".join(page))
    return pages


def extract(output_file="data/output.json"):
    p = HTMLPATH.glob("**/*.html")
    files = [x for x in p if x.is_file()]
    output = {}
    for f in tqdm(files):
        file_name = f.name[:-5]
        html_doc = f.open()
        soup = BeautifulSoup(html_doc, "html.parser")
        title = soup.find("h1").getText()
        h2tags = soup.find_all("h2")
        pages = get_pages_by_h2(h2tags)
        pages = [BeautifulSoup(page, "html.parser") for page in pages]
        output[file_name] = {"title": title, "content": []}

        for page in pages:
            code = [ele.getText() for ele in page.find_all("pre", {"class": "python"})]
            text = [ele.getText() for ele in page.find_all("p")]
            output[file_name]["content"].append(
                {"Topic": page.find("h2").getText(), "code": code, "text": text, "keyphrases" : [], "Arxiv Paper" : []}
            )
    output_file = Path(output_file)
    json.dump(output, output_file.open("w"), indent=2)


fire.Fire(extract)
