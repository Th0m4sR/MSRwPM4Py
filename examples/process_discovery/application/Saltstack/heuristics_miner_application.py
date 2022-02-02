import pandas as pd

from process_discovery import evaluation
from process_discovery.algorithms import HeuristicsMiner, petri_net_to_svg

home_directory = "path/to/project_folder/"

# ------------------------ Apply the Correlation Miner on Pull Request logs ------------------------ #

log_df = pd.read_csv(home_directory + "datasets/Saltstack/Salt_pull_request_log.csv")
hm = HeuristicsMiner(log_df)

net, initial_marking, final_marking, pn_gviz, _, _ = hm.apply()
petri_net_to_svg(pn_gviz, home_directory + "models/process_discovery/stored_models/pull_request/Saltstack/hm_petri_net_Saltstack_pulls_pn.svg")

evaluation.determine_quality(hm.log, net, initial_marking, final_marking,
                             path=home_directory + "models/process_discovery/evaluations/pull_request/Saltstack/heuristics_miner_Saltstack_pulls_evaluation.csv",
                             additional_cols={'miner type': 'heuristics miner'})

# ------------------------ Do the same for Issue logs ------------------------ #

log_df = pd.read_csv(home_directory + "datasets/Saltstack/Salt_issue_log.csv")
hm = HeuristicsMiner(log_df)

net, initial_marking, final_marking, pn_gviz, _, _ = hm.apply()
petri_net_to_svg(pn_gviz, home_directory + "models/process_discovery/stored_models/issues/Saltstack/hm_petri_net_Saltstack_issues_pn.svg")

evaluation.determine_quality(hm.log, net, initial_marking, final_marking,
                             path=home_directory + "models/process_discovery/evaluations/issues/Saltstack/heuristics_miner_Saltstack_issues_evaluation.csv",
                             additional_cols={'miner type': 'heuristics miner'})
