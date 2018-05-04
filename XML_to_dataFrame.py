import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import os

zip_name = "6406"
list_of_file = os.listdir(zip_name + "/" + zip_name + "/")
print(len(list_of_file))

def get_judge(file_path):
    with open(zip_name + "/" + zip_name + "/"+file_path, "r") as f:
        lines = f.readlines()
    xml=[]
    for i in lines:
        if len(i) > 120:
            xml += [i]
    court_names = []
    judge_el = []
    xml_path = []
    xml_id = []
    opinions = []
    for i in range(len(xml)):
        root = ET.fromstring(xml[i])
        opinion_el=""
        ifJudge = False
        for elem in root.iter(tag = 'judges'):
            judge_el += [elem.text]
            xml_path += [file_path]
            xml_id += [i]
            ifJudge = True
        if ifJudge:
            for elem in root.iter(tag = 'courtName'):
                court_names += [elem.text]
        if ifJudge:
            for elem in root.iter(tag = 'anchor'):
                try:
                    opinion_el+= elem.tail + " "
                except:
                    continue
        if opinion_el != "":
            opinions += [opinion_el]

    return(xml_path, xml_id, court_names, judge_el, opinions)

def clean_judges(judge):
    import re
    judge_el = judge
    if isinstance(judge_el, str):
        judge_el = judge_el.lower().strip(", .")
        if judge_el in ["before", "hon", "the honorable", "honorable", "", "hon."]:
            return None
        for x in ["^the ", "bankruptcy", "bankrupcy", "barkruptcy", "bankruptct", "judges", "judge", "district", "chief", "united",
                  "unite", "stated","states", "statet",
                  "state", "u.s", "hon\.", "^hon ", "honorable", "court", "of", "kansas"]:
            judge_el = re.sub(x, "", judge_el).strip(", .")
        judge_el = judge_el.replace(",  ,", ",")
        judge_el = judge_el.replace(".", "")
        if judge_el == "":
            judge_el = None
    else:
        return None
    return judge_el

xml_paths = []; xml_ids = []; court_names = []; judges = []; opinions = []
for file_ in list_of_file:
    try:
        xml_path, xml_id, court_name, judge, opinion = get_judge(file_)
        if not ((len(xml_path) == len(judge)) & (len(judge) == len(opinion))):
            print(len(path), len(judge), len(opinion))
        else:
            xml_paths += xml_path
            xml_ids += xml_id
            court_names += court_name
            judges += judge
            opinions += opinion

    except:
        continue

data = [[a, b, c] for a,b,c in zip(court_names, judges, opinions)]
df = pd.DataFrame(data, columns=["court_name", "judge", "opinion"])

df["clean_judge"] = df["judge"].apply(clean_judges)
df["notClear"] = df["clean_judge"].apply(lambda x: ("before" in x)*1 if isinstance(x, str) else 0)
df["ifNone"] = df["clean_judge"].apply(lambda x: (x is None)*1)
df["ifOne"] = df["clean_judge"].apply(lambda x: 1*((" and " not in x) and ("before" not in x)) if isinstance(x, str) else 0)

df.to_csv("file_summary_"+zip_name+".csv")
