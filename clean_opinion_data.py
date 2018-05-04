import pandas as pd
import numpy as np
import sys


def get_judge_last_name(judge_name):
    last_name = judge_name.split(",")[0]
    last_name = last_name.split(" ")
    if last_name[-1] in ["ii", "iii", "iv", "vi", "jr"]:
        last_name = last_name[-2]
    else:
        last_name = last_name[-1]
    if len(last_name) == 1:
        return None
    if last_name == "by":
        return None
    return last_name

def get_judge_full_name(judge_name):
    full_name = judge_name.split(",")[0]
    full_name = " ".join(full_name.split(" ")[-3:])
    return full_name

def main():
    file_path = sys.argv[1]
    print(file_path)
    df = pd.read_csv(file_path, index_col=0)
    # df = df[["court_name", "opinion", "clean_judge"]][df["ifOne"] == 1]
    # df["district"] = df["court_name"].apply(lambda x: set(x.lower().split(",")[0].split(" ")) - set("united states bankruptcy court for in the of district ".split(" ")))
    df = df[df["court_name"].apply(lambda x: "panel" not in x)]

    df["judge"] = df["clean_judge"].apply(lambda x: get_judge_last_name(x))
    df.dropna(inplace=True)
    df["full_name"] = df["clean_judge"].apply(lambda x: get_judge_full_name(x))
    df.to_csv(file_path)

if __name__ == "__main__":
    main()
