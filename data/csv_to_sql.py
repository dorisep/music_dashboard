import pandas as pd
import glob
import os

files = "*.csv"

df = pd.concat(map(pd.read_csv, glob.iglob(files, recursive=True)))
