import glob

import pandas as pd

home_directory = "path/to/project_folder/"

path = home_directory + "models/process_discovery/evaluations/issues/Rails"
all_files = glob.glob(path + "/*.csv")
print([x.split('/')[-1] for x in all_files])
df = pd.concat([pd.read_csv(path) for path in all_files])
df = df.reset_index()
df.loc[9, 'miner type'] = 'IMd'
df.loc[10, 'miner type'] = 'IMf'
df.loc[11, 'miner type'] = 'inductive miner'
df = df.round(5)
df.to_csv(home_directory + "models/process_discovery/evaluations/issues/rails_issue_evals.csv", index=False)

path = home_directory + "models/process_discovery/evaluations/pull_request/Rails"
all_files.clear()
all_files = glob.glob(path + "/*.csv")
df = pd.concat([pd.read_csv(path) for path in all_files])
df = df.reset_index()
df.loc[9, 'miner type'] = 'IMd'
df.loc[10, 'miner type'] = 'IMf'
df.loc[11, 'miner type'] = 'inductive miner'
df = df.round(5)
df.to_csv(home_directory + "models/process_discovery/evaluations/pull_request/rails_pulls_evals.csv", index=False)
