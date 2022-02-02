import pandas as pd

from process_discovery import evaluation
from process_discovery.algorithms import InductiveMiner, petri_net_to_svg, INDUCTIVE_MINER, INDUCTIVE_MINER_D, \
    INDUCTIVE_MINER_F

home_directory = "path/to/project_folder/"

# ------------------------ Apply the Correlation Miner on Pull Request logs ------------------------ #

print("Doing pull requests")
log_df = pd.read_csv(home_directory + "/datasets/Saltstack/salt_pull_request_log.csv")
im = InductiveMiner(log_df)

print("Inductive Miner")
variant = INDUCTIVE_MINER
net, initial_marking, final_marking, pn = im.apply(variant=variant)
petri_net_to_svg(pn, home_directory + "models/process_discovery/stored_models/pull_request/Saltstack/im_Saltstack_pulls_pn.svg")

evaluation.determine_quality(im.log, net, initial_marking, final_marking, include_soundness=False,
                             path=home_directory + "models/process_discovery/evaluations/pull_request/Saltstack/inductive_miner_Saltstack_pulls_evaluation.csv")

print("Inductive Miner Directly Follows")
variant = INDUCTIVE_MINER_D
net, initial_marking, final_marking, pn = im.apply(variant=variant)
petri_net_to_svg(pn, home_directory + "models/process_discovery/stored_models/pull_request/Saltstack/imd_Saltstack_pulls_pn.svg")

evaluation.determine_quality(im.log, net, initial_marking, final_marking, include_soundness=False,
                             path=home_directory + "models/process_discovery/evaluations/pull_request/Saltstack/inductive_miner_d_Saltstack_pulls_evaluation.csv")

print("Inductive Miner Infrequent")
variant = INDUCTIVE_MINER_F
net, initial_marking, final_marking, pn = im.apply(variant=variant)
petri_net_to_svg(pn, home_directory + "models/process_discovery/stored_models/pull_request/Saltstack/imf_Saltstack_pulls_pn.svg")

evaluation.determine_quality(im.log, net, initial_marking, final_marking, include_soundness=False,
                             path=home_directory + "models/process_discovery/evaluations/pull_request/Saltstack/inductive_miner_f_Saltstack_pulls_evaluation.csv")

# ------------------------ Do the same for Issue logs ------------------------ #

print("Doing issues")
log_df = pd.read_csv(home_directory + "/datasets/Saltstack/salt_issue_log.csv")
im = InductiveMiner(log_df)

print("Inductive Miner")
variant = INDUCTIVE_MINER
net, initial_marking, final_marking, pn = im.apply(variant=variant)
petri_net_to_svg(pn, home_directory + "models/process_discovery/stored_models/issues/Saltstack/im_Saltstack_issues_pn.svg")

evaluation.determine_quality(im.log, net, initial_marking, final_marking, include_soundness=False,
                             path=home_directory + "models/process_discovery/evaluations/issues/Saltstack/inductive_miner_Saltstack_issues_evaluation.csv")

print("Inductive Miner Directly Follows")
variant = INDUCTIVE_MINER_D
net, initial_marking, final_marking, pn = im.apply(variant=variant)
petri_net_to_svg(pn, home_directory + "models/process_discovery/stored_models/issues/Saltstack/imd_Saltstack_issues_pn.svg")

evaluation.determine_quality(im.log, net, initial_marking, final_marking, include_soundness=False,
                             path=home_directory + "models/process_discovery/evaluations/issues/Saltstack/inductive_miner_d_Saltstack_issues_evaluation.csv")

print("Inductive Miner Infrequent")
variant = INDUCTIVE_MINER_F
net, initial_marking, final_marking, pn = im.apply(variant=variant)
petri_net_to_svg(pn, home_directory + "models/process_discovery/stored_models/issues/Saltstack/imf_Saltstack_issues_pn.svg")

evaluation.determine_quality(im.log, net, initial_marking, final_marking, include_soundness=False,
                             path=home_directory + "models/process_discovery/evaluations/issues/Saltstack/inductive_miner_f_Saltstack_issues_evaluation.csv")
