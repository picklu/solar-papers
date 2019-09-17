# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 11:58:08 2019

@author: subrata
"""
import os
import json
import pandas as pd

current_location = os.path.dirname(__file__)
csv_folders = ["dsscs", "prscs"]


def csv_to_df(folder):
    """ clean and convert csv files to pandas data frame
    """
    csv_files = []
    folder_path = os.path.join(current_location, "..","data", folder)
    files  = os.listdir(folder_path)
    for file in files:
        if file.endswith("recs.csv"):
            csv_files.append(file)
            
    df = pd.DataFrame(columns=['AU', 'TI', 'DI'])

    for i, f in enumerate(csv_files):       
        infile = os.path.join(folder_path, f)
        subdf = pd.read_csv(infile)
        subdf = subdf.dropna(axis= 0, subset=['AU', 'TI', 'DI'])
        subdf = subdf[['AU', 'TI', 'DI']]
        df = pd.concat([df, subdf], ignore_index=True)

    df.columns = ["Authors", "Title", "DOI"]
    
    return df


def df_to_json(folder):
    """ save pandas data frame to json file
    """
    df = csv_to_df(folder)
    json_path = os.path.join(current_location, "..", "data")
    outfile = os.path.join(json_path, f"{folder}_papers.json")
    df.to_json(path_or_buf=outfile, orient="table", index=False)


if __name__ == "__main__":
    for folder in csv_folders:
        print(f"==> Converting files in {folder}")
        df_to_json(folder)
    print("==> done!")