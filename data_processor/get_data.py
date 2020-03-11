# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 11:58:08 2019

@author: subrata
"""
import os
import pandas as pd
import glob

def merge_csv_to_json(infile_path, outfil_path):
    all_files = glob.glob(infile_path)
    files = []
    for filename in all_files:
        df = pd.read_csv(filename, delimiter='\t', index_col=False, header=0)
        files.append(df)
    dframe = pd.concat(files, axis=0, ignore_index=True)
    dframe = dframe.drop_duplicates()
    dframe = dframe[['AF', 'TI', 'DI']]
    dframe.columns =  ["Authors", "Title", "DOI"]
    dframe.to_json(outfil_path, orient="table", index=False)


if __name__ == "__main__":
    print("==> Merging CSV files and generating a json file")
    data_dir = "data"
    csv_dir = "raw_data"
    data_path = os.path.join(os.path.dirname(__file__), "..", data_dir)
    csv_path = os.path.join(data_path, csv_dir)
    infile_path = os.path.join(csv_path, '*.txt')
    outfil_path = os.path.join(data_path, 'papers.json')
    merge_csv_to_json(infile_path, outfil_path)
    print("==> done!")