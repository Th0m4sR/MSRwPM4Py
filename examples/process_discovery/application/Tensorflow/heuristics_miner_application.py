import pandas as pd

from process_discovery import evaluation
from process_discovery.algorithms import HeuristicsMiner, petri_net_to_svg

home_directory = "path/to/project_folder/"

# ------------------------ Apply the Correlation Miner on Pull Request logs ------------------------ #

log_df = pd.read_csv(home_directory + "datasets/Tensorflow/tensorflow_pull_request_log.csv")
hm = HeuristicsMiner(log_df)

pn, initial_marking, final_marking, pn_gviz, _, _ = hm.apply()
petri_net_to_svg(pn_gviz, home_directory + "models/process_discovery/stored_models/pull_request/tensorflow/hm_petri_net_tensorflow_pulls_pn.svg")

evaluation.determine_quality(hm.log, pn, initial_marking, final_marking,
                             path=home_directory + "models/process_discovery/evaluations/pull_request/tensorflow/heuristics_miner_tensorflow_pulls_evaluation.csv",
                             additional_cols={'miner type': 'heuristics miner'})

# ------------------------ Do the same for Issue logs ------------------------ #

log_df = pd.read_csv(home_directory + "datasets/Tensorflow/tensorflow_issue_log.csv")
hm = HeuristicsMiner(log_df)

pn, initial_marking, final_marking, pn_gviz, _, _ = hm.apply()
petri_net_to_svg(pn_gviz, home_directory + "models/process_discovery/stored_models/issues/tensorflow/hm_petri_net_tensorflow_issues_pn.svg")

evaluation.determine_quality(hm.log, pn, initial_marking, final_marking,
                             path=home_directory + "models/process_discovery/evaluations/issues/tensorflow/heuristics_miner_tensorflow_issues_evaluation.csv",
                             additional_cols={'miner type': 'heuristics miner'})
