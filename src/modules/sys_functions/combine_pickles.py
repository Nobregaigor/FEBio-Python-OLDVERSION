
from find_files_in_folder import search_dirs
import pandas as pd

runs_directory = "D:\\Igor\\Research_USF\\University of South Florida\\Mao, Wenbin - Igor\\Febio-Models\\Active-Models\\PAQ\\Gamma-5-2\\runs"

pickles_paths = search_dirs(runs_directory, ".pickle")

df = pd.read_pickle(pickles_paths[0])
print(df)
# for i, pp in enumerate(pickles_paths):
#     print(pp)
#     if i == 0:
#         df = pd.read_pickle(pp)
#     else:
#         new_df = pd.read_pickle(pp)
#         print("new df:")
#         print(new_df[0:2])
#         df = pd.concat_data([df, new_df])