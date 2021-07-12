import json
from pathlib import Path

import fire
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from smart.settings import DATAPATH, HTMLPATH

test_file = HTMLPATH / "03-conditional.html"

df = pd.read_csv("map_concepts_activities_topics_Python_MasteryGrids_latest_course.csv")


def get_parsed_text(code):
    data = {"code": code, "mode": "simple"}
    response = requests.post("http://acos.cs.hut.fi/python-parser", data=data)
    try :
        output = [v for k, v in response.json()["lines"].items()][0]
        return output
    except:
        return []


def get_smart_content(code_types):
    output = []
    for t in code_types:
        matched_content = df[df["component_name"] == t]
        for i, row in matched_content.iterrows():
            output.append({"url": row["url"], "topic_name": row["topic_name"]})
    return {"Matched Smart Content": output}


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
            all_code = [ele.getText() for ele in page.find_all("pre", {"class": "python"})]
            text = [ele.getText() for ele in page.find_all("p")]
            code_segment = []
            if all_code:
                for code in all_code:
                    codelines = code.split("\n")
                    execcode = codelines
                    outputcode = []
                    if not(code.find(">>>")==-1):
                        execcode = [line[4:] for line in codelines if line[:3] == ">>>"]
                        outputcode = [line for line in codelines if line[:3] != ">>>"]
                    execcode = "\n".join(execcode)
                    outputcode = "\n".join(outputcode)
                    if execcode:
                        code_types = get_parsed_text(execcode)
                        matched_content = get_smart_content(code_types)
                        code_segment.append({
                            "execcode": execcode,
                            "matched_content": matched_content,
                        })

            output[file_name]["content"].append(
                {
                    "Topic": page.find("h2").getText(),
                    "code_segment": code_segment,
                    "text": text,
                    "code" : all_code
                }
            )
    output_file = Path(output_file)
    json.dump(output, output_file.open("w"), indent=2)


fire.Fire(extract)
